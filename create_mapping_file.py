from utils.schema2context import generate_context_mapping_dict as generate_context
import json


if __name__ == '__main__':
    regex = {
        "/schema": "/context/obo",
        "_schema": "_obo_context",
        "json": "json-ld"
    }

    try:
        mapping_object = generate_context("https://w3id.org/dats/schema/dataset_schema.json",
                                          regex,
                                          "DATS")[0]
        mapping_as_file = "dats_context_mapping.json"
        with open(mapping_as_file, 'w', encoding='utf-8') as f:
            json.dump(mapping_object, f, ensure_ascii=False, indent=4)

    except IOError as ioe:
        print("There is a problem There:", ioe)
