from semDiff.fullDiff import FullSemDiff
from json import dump
import os

network1 = {
    "name": "DATS",
    "schemas": {
      "person_schema.json": {
        "id": "https://w3id.org/dats/schema/person_schema.json",
        "$schema": "http://json-schema.org/draft-04/schema",
        "title": "DATS person schema",
        "description": "A human being",
        "type": "object",
        "properties": {
          "@context": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "object"
              }
            ]
          },
          "@id": {"type": "string", "format": "uri"},
          "@type": {"type": "string", "enum": ["Person"]},
          "identifier": {
            "description": "Primary identifier for the person.",
            "$ref": "identifier_info_schema.json#"
          },
          "alternateIdentifiers": {
              "description": "Alternate identifiers for the person.",
              "type": "array",
              "items": {
                "$ref": "alternate_identifier_info_schema.json#"
              }
          },
          "relatedIdentifiers": {
              "description": "Related identifiers for the person.",
              "type": "array",
              "items": {
                "$ref": "related_identifier_info_schema.json#"
              }
            },
          "fullName": {
              "description": "The first name, any middle names, and surname of a person.",
              "type":  "string"
            },
          "firstName": {
              "description": "The given name of the person.",
              "type":  "string"
            },
          "middleInitial": {
              "description": "The first letter of the person's middle name.",
              "type":  "string"
            },
          "lastName": {
              "description": "The person's family name.",
              "type": "string"
            },
          "email": {
              "description": "An electronic mail address for the person.",
              "type": "string",
              "format": "email"
            },
          "affiliations": {
              "description": "The organizations to which the person is associated with.",
              "type": "array",
              "items": {
                "$ref": "organization_schema.json#"
              }
            },
          "roles": {
              "description": "The roles assumed by a person, ideally from a controlled vocabulary/ontology.",
              "type": "array",
              "items": {
                "$ref" : "annotation_schema.json#"
              }
            },
          "extraProperties": {
              "description": "Extra properties that do not fit in the previous specified attributes. ",
              "type": "array",
              "items": {
                "$ref" : "category_values_pair_schema.json#"
              }
          }
        },
        "additionalProperties": False
      },
      "identifier_info_schema": {
        "id": "https://w3id.org/dats/schema/identifier_info_schema.json",
        "$schema": "http://json-schema.org/draft-04/schema",
        "title": "DATS identifier information schema",
        "description": "Information about the primary identifier.",
        "type": "object",
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
            "type": "string", "format": "uri"
          },
          "@type": {
            "description": "The JSON-LD type",
            "type": "string", "enum": [ "Identifier" ]},
          "identifier": {
            "description": "A code uniquely identifying an entity locally to a system or globally.",
            "type": "string"
          },
          "identifierSource": {
            "description": "The identifier source represents information about the organisation/"
                           "namespace responsible for minting the identifiers. "
                           "It must be provided if the identifier is provided.",
            "type" : "string"
          }
        },
        "additionalProperties": False
      }
    },
    "contexts": {
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
}
network2 = {
    "name": "MIACA",
    "schemas": {
      "source_schema.json": {
        "id": "https://w3id.org/MIRcat/miaca/source_schema.json",
        "$schema": "http://json-schema.org/draft-04/schema",
        "title": "MIACA Source - corresponding to a person and their organization",
        "description": "Contact details of researcher/person/laboratory/institution in charge of "
                       "the project -Used to describe the contact details of the scientist "
                       "- corresponds to MIACA XSD sourceType",
        "type": "object",
        "properties": {
          "@context": {
            "description": "The  JSON-LD context.",
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "object"
              }
            ]
          },
          "@type": {
            "description": "The JSON-LD type",
            "type": "string",
            "format": "uri"
          },
          "ID": {
            "type": "string"
          },
          "name": {
            "description": "name of the researcher working on the project.",
            "type": "string",
            "minLength": 1
          },
          "institution": {
            "description": "name of the institution/affiliation the researcher is working at",
            "type": "string",
            "minLength": 1
          },
          "department": {
            "description": "department in the institution",
            "type": "string",
            "minLength": 1
          },
          "address": {
            "description": "address of the institution",
            "type": "string",
            "minLength": 1
          },
          "city": {
            "description": "city the institution is placed",
            "type": "string",
            "minLength": 1
          },
          "country": {
            "description": "country the city is placed",
            "type": "string",
            "minLength": 1
          },
          "email": {
            "description": "email of the researcher",
            "type": "string",
            "minLength": 1
          }
        },
        "required": ["ID",
                     "name", "institution", "department", "address", "city", "country", "email"]
      }
    },
    "contexts": {
        "source_schema.json": {
            "sdo": "https://schema.org/",
            "Source": "sdo:Person",
            "ID":  {
              "@id": "sdo:identifier",
              "@type": "sdo:Text"
            },
            "name": {
              "@id": "sdo:name",
              "@type": "sdo:Text"
            },
            "institution": {
              "@id": "sdo:affiliation",
              "@type": "sdo:Organization"
            },
            "department": {
              "@id": "sdo:department",
              "@type": "sdo:Text"
            },
            "address":  {
              "@id": "sdo:address",
              "@type": "sdo:Text"
            },
            "city":  {
              "@id": "sdo:department",
              "@type": "sdo:Organization"
            },
            "country":  {
              "@id": "sdo:addressCountry",
              "@type": "sdo:Country"
            },
            "email":  {
              "@id": "sdo:email",
              "@type": "sdo:Text"
            }
          },
    }
}

networks_contexts = [network1["contexts"], network2["contexts"]]
full_diff = FullSemDiff(networks_contexts, network1["schemas"], network2["schemas"])

output = {
    "network1": network1,
    "network2": network2,
    "overlaps": full_diff.twins
}

file_name = network1["name"] + '_VS_' + network2["name"] + '_overlaps.json'
file_full_path = os.path.join(os.path.dirname(__file__), 'fullDiffOutput/' + file_name)

with open(file_full_path, 'w') as outfile:
    dump(output, outfile)
outfile.close()
