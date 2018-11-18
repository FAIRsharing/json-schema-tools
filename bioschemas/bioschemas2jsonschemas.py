import requests
from json import dumps
from copy import deepcopy
from yaml import load, scanner
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class BioschemasConverter:
    """ A class that will transform a given Bioschemas yaml into a set of JSON schemas

    :param schema_url: URL to the yaml file
    :type schema_url: basestring
    """

    def __init__(self, schema_url, base_item, processed_schemas):
        self.base_url = schema_url
        self.raw_data = self.get_schema(base_item)
        self.processed_schema = processed_schemas
        self.output = self.convert()

    def get_schema(self, schema_name):
        """ Get the python variable from the given URL by parsing the yaml string

        :return: a dictionary deserialized from the yaml string
        """
        try:
            schema_response = requests.get(self.base_url + schema_name)
            if schema_response.status_code != 404:
                return load(schema_response.text, Loader=Loader)
            else:
                raise FileNotFoundError("There is a problem with your input data, cannot parse yaml data")
        except scanner.ScannerError:
            raise FileNotFoundError("There is a problem with your input data, cannot parse yaml data")

    @staticmethod
    def base_schema_attributes():
        """ Return the base attributes needed to build a JSON schema

        :return: the base dictionary needed for the conversion to JSON schema
        """
        schema = {
            "@id": None,
            "$schema": "http://json-schema.org/draft-04/schema#",
            "type": "object",
            "additionalProperties": False,
            "required":  [],
            "properties": {
                "@context": {
                    "description": "The JSON-LD context",
                    "anyOf": [
                        {
                            "type": "string"
                        },
                        {
                            "type": "object"
                        },
                        {
                            "type": "array"
                        }
                    ]
                },
                "@id": {
                    "description": "The JSON-LD identifier",
                    "type": "string",
                    "format": "uri"
                },
                "@type": {
                    "description": "The JSON-LD type",
                    "type": "string",
                }
            }
        }
        return schema

    def convert(self):
        """ Realize the conversion

        :return:
        """
        output_schema = deepcopy(self.base_schema_attributes())
        base_types = {
            "Text": {
                "type": "string",
            },
            "URL": {
                "type": "string",
                "format": "uri"
            },
            "Boolean": {
                "type": "boolean"
            },
            "Number": {
                "type": "integer"
            },
            "Date": {
                "type": "string",
                "format": "date-time"
            },
            "DateTime": {
                "type": "string",
                "format": "date-time"
            }
        }

        if "spec_info" in self.raw_data.keys():
            output_schema["title"] = self.raw_data["spec_info"]["title"]
            output_schema["description"] = self.raw_data["spec_info"]["description"]
            output_schema["properties"]["@type"]["enum"] = [self.raw_data["spec_info"]["title"]]

        if "mapping" in self.raw_data.keys():
            fields = self.raw_data["mapping"]
            for field in fields:

                output_schema['properties'][field['property']] = {}
                output_schema['properties'][field['property']]['description'] = field['bsc_description'] if field['bsc_description'] != "" else field['description']

                # Process fields with only one type
                if len(field["expected_types"]) == 1:

                    # Process standard fields
                    for base_type in base_types.keys():
                        if base_type in field["expected_types"]:
                            if field['cardinality'] == "MANY":
                                output_schema['properties'][field['property']]["type"] = "array"
                                output_schema['properties'][field['property']]["items"] = base_types[base_type]
                            else:
                                output_schema['properties'][field['property']] = base_types[base_type]

                    for base_type in field["expected_types"]:
                        if base_type not in base_types:
                            schema_url = self.base_url + field["expected_types"][0] + "%20specification.yaml"
                            if schema_url not in self.processed_schema:
                                self.processed_schema.append(schema_url)
                                try:
                                    sub_schema = BioschemasConverter(self.base_url, field["expected_types"][0] + "%20specification.yaml", self.processed_schema)
                                except FileNotFoundError:
                                    sub_schema = False

                                if sub_schema:
                                    if 'definitions' not in output_schema.keys():
                                        output_schema['definitions'] = {}
                                    output_schema['definitions'][base_type] = sub_schema.output

                                    if field['cardinality'] == "MANY":
                                        output_schema['properties'][field['property']]["type"] = "array"
                                        output_schema['properties'][field['property']]["items"] = {
                                            "$ref": "#/definitions/" + base_type
                                        }

                                    else:
                                        output_schema['properties'][field['property']]["type"] = "object"
                                        output_schema['properties'][field['property']]['$ref'] = "#/definitions/" + base_type

                # Process fields with more than one type
                elif len(field["expected_types"]) > 1:

                    # type array
                    if field['cardinality'] == "MANY":
                        output_schema['properties'][field['property']]["type"] = "array"
                        output_schema['properties'][field['property']]["items"] = {
                            "anyOf": []
                        }
                        for base_type in base_types.keys():
                            if base_type in field['expected_types'] and base_types[base_type] not in output_schema['properties'][field['property']]["items"]['anyOf']:
                                output_schema['properties'][field['property']]["items"]['anyOf'].append(base_types[base_type])

                        # TODO: process object fields

                    # Only one value allowed
                    else:
                        output_schema['properties'][field['property']]['anyOf'] = []
                        for base_type in base_types.keys():
                            if base_type in field['expected_types'] and base_types[base_type] not in output_schema['properties'][field['property']]['anyOf']:
                                output_schema['properties'][field['property']]['anyOf'].append(base_types[base_type])

                        # TODO: Process object fields

                # Add required field to root['required']
                if field["marginality"] == "Minimum":
                    output_schema['required'].append(field['property'])

        return output_schema


if __name__ == '__main__':
    url = "https://raw.githubusercontent.com/BioSchemas/bioschemas-goweb/master/build/example/"
    converter = BioschemasConverter(url, "DataCatalog%20specification.yaml", [url+"DataCatalog%20specification.yaml"])
    test = dict(converter.output)
    print(dumps(test, indent=4))

