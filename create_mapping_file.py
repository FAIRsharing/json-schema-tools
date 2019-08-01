from utils import schema2context
from os import listdir
import os
from os.path import isfile, join
import json

schema_dir_path = "../DATS/dats-tools/json-schemas/"
regex = {"/schema": "/context/obo", "_schema": "_obo_context", "json": "json-ld"}
try:

    files = [f for f in listdir(schema_dir_path) if isfile(join(schema_dir_path, f))]

    for schema_filename in files:
        schema_path = os.path.join(schema_dir_path, schema_filename)
        print(schema_filename)

    schema_uri = str(join(schema_dir_path, "dataset_schema.json"))
    print("url:", schema_uri)

    mapping_object = ""
    try:
        # mapping_object = schema2context.generate_context_mapping_dict(schema_uri, regex, "DATS")
        mapping_object = schema2context.generate_context_mapping_dict("https://w3id.org/dats/schema/dataset_schema.json"
                                                                      , regex, "DATS")
    except Exception as e:
        print("There is a problem here:", e)

    mapping_as_file = "dats_context2schema_mapping.json"
    with open(mapping_as_file, 'w', encoding='utf-8') as f:
        json.dump(mapping_object, f, ensure_ascii=False, indent=4)

except IOError as ioe:
    print("There is a problem There:", ioe)
