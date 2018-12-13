import unittest
import os
from utils.schema2context import create_network_context, prepare_input, create_and_save_contexts


class TestSchema2Context(unittest.TestCase):

    def test_create_context_network1(self):
        url = "https://w3id.org/mircat/miaca/schema/miaca_schema.json"

        base = {
            "sdo": "https://schema.org",
            "obo": "http://purl.obolibrary.org/obo/"
        }

        mapping = prepare_input(url,
                                "MIACA")

        create_network_context(mapping, base)

    def test_create_and_save_contexts_1(self):
        url = "https://w3id.org/mircat/miacme/schema/miacme_schema.json"

        base = {
            "sdo": "https://schema.org",
            "obo": "http://purl.obolibrary.org/obo/"
        }

        mapping = prepare_input(url,
                                "MIACME")

        output_directory = os.path.join(os.path.dirname(__file__), "../data/contexts")

        context = create_and_save_contexts(mapping, base, output_directory)
        print(context)


    def test_create_and_save_contexts_2(self):
        url = "https://w3id.org/mircat/miflowcyt/schema/miflowcyt_schema.json"

        base = {
            "sdo": "https://schema.org",
            "obo": "http://purl.obolibrary.org/obo/"
        }

        mapping = prepare_input(url,
                                "MiFlowCyt")

        output_directory = os.path.join(os.path.dirname(__file__), "../data/contexts")

        context = create_and_save_contexts(mapping, base, output_directory)
        print(context)