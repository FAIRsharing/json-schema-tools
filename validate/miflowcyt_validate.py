from requests import request
from xmljson import parker
from xml.etree.ElementTree import fromstring
from json import dump, load
import os
from jsonbender import bend, OptionalS, S
from validate.jsonschema_validator import validate_instance


def grab_user_content(client_identifier):
    """
    Grab all content for a given user ID as an XML and outputs it as a JSON
    :param client_identifier: the user ID
    :return: the dictionary containing the XML
    """
    full_url = "http://flowrepository.org/list?client=" + client_identifier
    response = request("GET", full_url)
    return parker.data((fromstring(response.text)))


def get_user_content_id(client_identifier):
    """
    Return all IDs found in the user content XML
    :param client_identifier: the user content ID
    :return: a list of all IDs there were identified in the variable returned by the API
    """
    ids = []
    user_data = grab_user_content(client_identifier)

    for experiment in user_data['public-experiments']['experiment']:
        ids.append(experiment['id'])

    return ids


def grab_experiment_from_api(client_identifier, item_identifier):
    """
    Retrieve the experiment metadata and return it as a python object
    :param client_identifier: the client identifier (apiKey)
    :param item_identifier: the item identifier that should be retrieved
    :return: the python object obtained from the XML
    """

    full_url = "http://flowrepository.org/list/" + item_identifier + "?client=" + client_identifier
    response = request("GET", full_url)
    return parker.data((fromstring(response.text)))["public-experiments"]["experiment"]


def load_schema(base_schema_name, network):
    """
    Load the set of schemas dependencies from the base given schema
    :param base_schema_name: the name of the schema to load
    :param network: the dictionary to add the loaded schemas
    :return network: the dictionary that contains the loaded schemas
    """

    base_path = ".././tests/data/MiFlowCyt/"
    base_schema_path = os.path.join(os.path.dirname(__file__), base_path + base_schema_name)
    with open(base_schema_path) as schema_input:
        schema_data = load(schema_input)
    schema_input.close()

    network[base_schema_name] = schema_data

    for field in schema_data["properties"]:

        # TODO: add use case for anyOf, oneOf and items
        if '$ref' in schema_data["properties"][field]:
            test = schema_data["properties"][field]["$ref"].rsplit('/', 1)[-1]
            network = load_schema(test, network)

    return network


def transform_json(instance, schema, mapping):
    """
    :param instance: an instance JSON which doesn't necesarilly follow the JSON schema
    :param schema: a JSON schema which will be used as base for the transformation - might not be needed
    :param mapping: a dictionary with the mapping between the original JSON fields and fields from the JSON schema
    :return: the transformed JSON following the JSON schema structure
    """
    ignored_keys = ["@id", "@type", "@context"]

    total_fields = 0
    matched_field = 0
    matched_fields = []

    for field in schema['properties']:
        if field not in ignored_keys:

            total_fields += 1
            if field in mapping:
                processing_field = mapping[field]
            else:
                processing_field = field

            if processing_field in instance:
                matched_field += 1
                matched_fields.append((field, processing_field))

    print("Matched: " + str(matched_field) + " out of " + str(total_fields))
    return matched_fields


def validate_instance_from_file(instance, item_id, schema_name):
    file_name = item_id + '.json'
    file_full_path = os.path.join(os.path.dirname(__file__),
                                  "../tests/data/MiFlowCyt/" + file_name)

    with open(file_full_path, 'w') as outfile:
        dump(instance, outfile)
    outfile.close()

    errors = validate_instance(os.path.join(os.path.dirname(__file__), "../tests/data/MiFlowCyt/"),
                               schema_name,
                               os.path.join(os.path.dirname(__file__), "../tests/data/MiFlowCyt/"),
                               file_name,
                               1,
                               {})


if __name__ == '__main__':
    base_schema = "experiment_schema.json"

    config_file = os.path.join(os.path.dirname(__file__), ".././tests/test_config.json")
    with open(config_file) as config:
        clientID = load(config)['flowrepo_userID']
    config.close()

    MAPPING = {
        'date': S('experiment-dates'),
        'primaryContact': S('primary-researcher'),
        'qualityControlMeasures': S('quality-control-measures'),
        'conclusions': S('conclusion'),
        'organization': OptionalS('organizations'),
        'purpose': S('purpose'),
        'keywords': S('keywords'),
        'experimentVariables': OptionalS('experimentVariables'),
        'other': OptionalS('other')
    }

    content_ids = get_user_content_id(clientID)
    for i in range(10):
        exp_content = grab_experiment_from_api(clientID, content_ids[i])
        result = bend(MAPPING, exp_content)
        if result['organization'] == "\n   ":
            result['organization'] = {}

        validate_instance_from_file(result, content_ids[i], base_schema)
