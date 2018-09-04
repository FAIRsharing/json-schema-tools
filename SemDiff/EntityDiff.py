class EntityCoverage:
    """
    This class compute the coverage of entities (schemas) among two networks (set of schemas) by comparing the semantic
    base type of each schema.
    :param networks_array: an array containing the two networks to compare
    """

    def __init__(self, networks_array):
        network1 = self.__process_network(networks_array[0])
        network2 = self.__process_network(networks_array[1])
        coverage = self.__compute_coverage(network1, network2)
        self.covered_entities = coverage[0]
        self.total_entities = coverage[1]
        self.matched_entities = coverage[2]

    @staticmethod
    def __process_network(network):
        """
        Private method that retrieve the base type of each entity for later comparison
        :param network: a dictionary of schemas and their context
        :return network_output: a dictionary of schemas and their base type retrieved from the context
        """
        network_output = {}
        for schema in network:
            schema_name = schema.replace("_schema.json", "").capitalize()
            schema_type = None
            schema_context = network[schema]
            if schema_name in schema_context.keys():
                schema_type = schema_context[schema_name]
            network_output[schema_name] = schema_type
        return network_output

    @staticmethod
    def __compute_coverage(network_a, network_b):
        """
        Private method that compute the coverage between two networks
        :param network_a: the output of __process_network for the first network
        :param network_b: the output of __process_network for the second network
        :return output: an array containing the twined entities, the number of processed entities and the number of twins
        """
        coverage = {}
        total_items = 0
        matched_items = 0

        for schema in network_a:
            total_items += 1
            context_type = network_a[schema]
            matched = False

            if context_type is not None:

                for schema2 in network_b:
                    context_type2 = network_b[schema2]

                    if context_type == context_type2:
                        matched = True
                        if schema in coverage.keys():
                            coverage[schema].append(schema2)
                        else:
                            coverage[schema] = [schema2]

            if matched is False:
                coverage[schema] = None
            else:
                matched_items += 1

        output = [coverage, total_items, matched_items]
        return output


if __name__ == '__main__':

    DATS_data = {
        "person_schema.json": {
            "sdo": "https://schema.org/",
            "Person": "sdo:Person",
            "identifier": "sdo:identifier",
            "firstName": "sdo:givenName",
            "lastName": "sdo:familyName",
            "fullName": "sdo:name",
            "email": "sdo:email",
            "affiliations": "sdo:affiliation",
            "roles": "sdo:roleName"
        },
        "identifier_info_schema.json": {
            "sdo": "https://schema.org/",
            "Identifier": "sdo:Thing",
            "identifier": "sdo:identifier",
            "identifierSource": {
                "@id": "sdo:Property",
                "@type": "sdo:Text"
            }
        }
    }

    MIACA_data = {
        "source_schema.json": {
            "sdo": "https://schema.org/",
            "Source": "sdo:Person",
            "identifier": "sdo:identifier",
            "firstName": "sdo:givenName",
            "lastName": "sdo:familyName",
            "fullName": "sdo:name",
            "email": "sdo:email",
            "affiliations": "sdo:affiliation",
            "roles": "sdo:roleName"
        },
        "identifier_info_schema.json": {
            "sdo": "https://schema.org/",
            "Identifier_info": "sdo:Thing",
            "identifier": "sdo:identifier",
            "identifierSource": {
                "@id": "sdo:Property",
                "@type": "sdo:Text"
            }
        }
    }

    networks = [DATS_data, MIACA_data]
    entity_coverage = EntityCoverage(networks)
    print(entity_coverage.covered_entities)
    print('Coverage: ' + str((entity_coverage.matched_entities/entity_coverage.total_entities)*100) + '%')
