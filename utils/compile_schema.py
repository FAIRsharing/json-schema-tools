import json
from copy import deepcopy as copy
from jsonschema.validators import RefResolver

ignored_keys = ["@id", "@type", "@context"]
iterables = ['anyOf', 'oneOf', 'allOf']


def get_name(schema_url):
    name = schema_url.split("/")[-1].replace("#", '')
    return name


def resolve_schema_references(schema, loaded_schemas, schema_url=None, refs=None):
    """
    Resolves and replaces json-schema $refs with the appropriate dict.

    Recursively walks the given schema dict, converting every instance
    of $ref in a 'properties' structure with a resolved dict.

    This modifies the input schema and also returns it.

    Arguments:
        schema:
            the schema dict
        loaded_schemas:
            a recursive dictionary that stores the path of already loaded schemas to prevent
            circularity issues
        refs:
            a dict of <string, dict> which forms a store of referenced schemata
        schema_url
            the URL of the schema

    Returns:
        schema
    """

    refs = refs or {}
    if schema_url:
        return _resolve_schema_references(schema,
                                          RefResolver(schema_url, schema, store=refs),
                                          loaded_schemas,
                                          '#')
    else:
        return _resolve_schema_references(schema,
                                          RefResolver("", schema, store=refs),
                                          loaded_schemas,
                                          '#')


def _resolve_schema_references(schema, resolver, loaded_schemas, object_path):
    """

    :param schema:
    :param resolver:
    :param loaded_schemas:
    :param object_path: a string containing the path of the current level inside the document
    :return:
    """

    if SchemaKey.ref in schema:

        if schema['$ref'][0] != '#':
            reference_path = schema.pop(SchemaKey.ref, None)
            resolved = resolver.resolve(reference_path)[1]

            if get_name(resolved['id']) not in loaded_schemas:
                print(get_name(resolved['id']))
                loaded_schemas[get_name(resolved['id'])] = object_path
                schema.update(resolved)
                return _resolve_schema_references(schema, resolver, loaded_schemas, object_path)

            else:
                res = {"$ref": loaded_schemas[get_name(resolved['id'])]}
                schema.update(res)

    if SchemaKey.properties in schema:
        for k, val in schema[SchemaKey.properties].items():
            current_path = object_path + '/properties/'+k
            schema[SchemaKey.properties][k] = _resolve_schema_references(val,
                                                                         resolver,
                                                                         loaded_schemas,
                                                                         current_path)

    if SchemaKey.definitions in schema:
        for k, val in schema[SchemaKey.definitions].items():
            current_path = object_path + '/definitions/' + k
            schema[SchemaKey.definitions][k] = _resolve_schema_references(val,
                                                                          resolver,
                                                                          loaded_schemas,
                                                                          current_path)

    for pattern in SchemaKey.sub_patterns:
        i = 0
        if pattern in schema:
            for val in schema[pattern]:
                iterator = str(copy(i))
                current_path = object_path + '/' + pattern + '/' + iterator
                schema[pattern][i] = _resolve_schema_references(val,
                                                                resolver,
                                                                loaded_schemas,
                                                                current_path)
                i += 1

    if SchemaKey.items in schema:
        current_path = object_path + '/items'
        schema[SchemaKey.items] = _resolve_schema_references(schema[SchemaKey.items],
                                                             resolver,
                                                             loaded_schemas,
                                                             current_path)

    return schema


class SchemaKey:
    ref = "$ref"
    items = "items"
    properties = "properties"
    definitions = 'definitions'
    pattern_properties = "patternProperties"
    sub_patterns = ['anyOf', 'oneOf', 'allOf']


if __name__ == '__main__':
    processed_schemas = {}
    schemaURL = 'https://w3id.org/dats/schema/study_schema.json#'
    schema_name = get_name(schemaURL)

    processed_schemas[get_name(schemaURL)] = '#'

    data = resolve_schema_references(resolve_reference(schemaURL), processed_schemas, schemaURL)

    with open('../tests/data/compile_test.json', 'w') as output_file:
        json.dump(data, output_file, indent=4)



