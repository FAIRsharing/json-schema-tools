import unittest
import os
from utils.schema2context import (
    create_network_context,
    prepare_input,
    create_and_save_contexts,
    generate_context_mapping_dict,
    generate_labels_from_contexts,
    json
)


class TestSchema2Context(unittest.TestCase):
    input = dict({
        "MIACME": {
            "schema_url": "https://w3id.org/mircat/miacme/schema/miacme_schema.json"
        },
        "MIACA": {
            "schema_url": "https://w3id.org/mircat/miaca/schema/miaca_schema.json"
        },
        "MIFlowCyt": {
            "schema_url": "https://w3id.org/mircat/miflowcyt/schema/miflowcyt_schema.json"
        }
    })

    base = {
        "sdo": "https://schema.org",
        "obo": "http://purl.obolibrary.org/obo/"
    }

    regexes = {
        "/schema": "/context/obo",
        "_schema": "_obo_context",
        "json": "jsonld"
    }

    def test_create_context_network(self):
        for key in self.input:
            mapping = prepare_input(self.input[key]["schema_url"], key)
            create_network_context(mapping, self.base)

    def test_create_and_save_contexts(self):
        for key in self.input:
            mapping = prepare_input(self.input[key]["schema_url"], key)
            output_directory = os.path.join(os.path.dirname(__file__), "../data/contexts")
            context = create_and_save_contexts(mapping, self.base, output_directory)
            self.assertTrue(context)

    def test_generate_mapping_dict(self):
        for key in self.input:
            mapping, errors = generate_context_mapping_dict(
                self.input[key]["schema_url"],
                self.regexes, key)
            print(json.dumps(mapping, indent=4))
            print(errors)
            self.assertTrue(mapping["networkName"] == key)

    def test_generate_labels_from_contexts_1(self):
        labels = {}
        contexts = {
            "cell_line_obo_context.jsonld": {
                "@context": {
                    "obo": "http://purl.obolibrary.org/obo/",
                    "CellLine": "obo:CLO_0000031",
                    "@language": "en",
                    "ID": "obo:IAO_0000578",
                    "lineQC": "obo:ERO_0001219",
                    "validation": "obo:ERO_0002025",
                    "cellLineName": "obo:IAO_0000590",
                    "modifications": "obo:CLO_0000004",
                    "passageNo": "obo:EFO_0007061",
                    "cellSource": "obo:CL_0000000"
                }
            }
        }
        generate_labels_from_contexts(contexts, labels)
        print(labels)

    def test_generate_labels_from_contexts_2(self):
        labels = {}
        contexts = {
            "@context": {
                "obo": "http://purl.obolibrary.org/obo/",
                "bao": "http://www.bioassayontology.org/bao#",
                "ImagingCondition": "obo:FBbi_root_00000000",
                "@language": "en",
                "timeSeriesInterval": "obo:IAO_0000584",
                "imageSequenceType": "obo:NCIT_C69268",
                "pixels": "obo:NCIT_C48367",
                "observationPeriod": "obo:NCIT_C25616",
                "numericalAperture": "obo:NCIT_C44175",
                "observationPeriodUnit": "obo:UO_0000003",
                "objectiveLens": "obo:ERO_0000453",
                "modality": "obo:FBbi_00000222",
                "channelDefinition": "bao:BAO_0000184",
                "timeSeriesIntervalUnit": "obo:UO_0000003"
            }
        }
        generate_labels_from_contexts(contexts, labels)
        print(labels)
