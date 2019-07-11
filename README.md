
[![Build Status](https://travis-ci.org/FAIRsharing/jsonldschema.svg?branch=master)](https://travis-ci.org/FAIRsharing/jsonldschema)
[![Coverage Status](https://coveralls.io/repos/github/FAIRsharing/jsonldschema/badge.svg?branch=master)](https://coveralls.io/github/FAIRsharing/jsonldschema?branch=master)
[![Documentation Status](https://readthedocs.org/projects/jsonldschema/badge/?version=latest)](https://jsonldschema.readthedocs.io/en/latest/?badge=latest)


## Machine Actionable Metadata Models
One of the most common format to exchange data over the web is the **JavaScript Object Notation** (**JSON**). It's a popular open-standard
that can be used to represent data and metadata instances and the constrains that should be applied to describe these object (also called **schemas**).
<br/> Schemas are built using the **JSON-Schema** standard which informs about the syntactic constrains of an object: properties name, 
description, allowed values, cardinality, references to other schemas, ect ....
<br/>They are **highly interconnected** and can even contain circularity. This allows to represent very complex structures (called networks in this documentation), which, however, may become
hardly human readable. To emphasise this phenomena, semantic constrains for machine readability that should also be taken into consideration create an even more complex specification.

#### Separating syntactic and semantic layers:
![alt text](assets/separation_of_concerns.png "Separation of semantic and syntactic concerns")

In order to cope with the semantic and syntactic constrains, the semantic layer was separated from the schemas and included in context files inspired by the **JSON-LD** specification. Each schema is bound to a set of context 
files (through mapping files) that deliver the ontology tags describing the object and its properties. This allows to easily extend an existing schema or network with new vocabulary terms and to have different vocabulary systems 
living side by side.

The purpose of this repository is to provide a python 3 toolkit that help users create, compare, merge and export these schemas and their associated context files in order to 
increase the existing pool of **machine** and **human readable models** that represent **syntactic** and **semantic constrains of metadata**.
<br/> This is very important, especially in the context of data **Findability**, **Accessibility**, **Integrability** and **Reusablity** ([FAIR](https://www.nature.com/articles/sdata201618)) 
where a lot of representations are still too verbose and lack machine readable formats. 


#### Inputs
The input schema networks used to create the toolkit can be found as follow:
- Minimum Information About Cell Assays: **[MIACA](https://github.com/FAIRsharing/mircat/tree/master/miaca)** 
- Minimum Information About Cell Migration Experiments: **[MIACME](https://github.com/FAIRsharing/mircat/tree/master/miacme)**
- Data Tag Suite: **DATS** [schemas](https://github.com/datatagsuite/schema) and [context](https://github.com/datatagsuite/context)
- Minimum Information About Flow Cytometry Experiments: **[MiFlowCyt](https://github.com/FAIRsharing/mircat/tree/master/miflowcyt)**


#### Navigation

1) [Setting up](#setting-up)
1) [Explore existing schemas in the browser](#exploring-an-existing-set-of-schemas) (requires the jsonschema documenter)
2) Compare schemas in the browser (requires the compare-and-view tool)
3) Merge schemas
4) Create new context files or extend existing ones
5) Export schemas in the CEDAR application
6) Import MiFlowCyt instances (dataset) as JSON-LD and validate them against the proper schema set (requires an API key)
7) Identify circularity in existing set of schemas (using yet another python library)


## Setting Up:

First, you will need a virtual environment, import the code and install dependencies:
```
virtualenv venv
source venv/bin/activate
git clone https://github.com/FAIRsharing/jsonldschema.git
cd jsonldschema
pip install -r requirements.txt
```

If you plan on using either the CEDAR exporter or the MiFlowCyt importer, you will need to provide your API keys through 
a configuration file and, optionally run the integration tests.
- make a copy of the ```/tests/test_config.json.sample``` file and open the copy:

```bash
cp /tests/test_config.json.sample /tests/test_config.json
```

You will need to provide:
- your staging and production CEDAR API keys (include the key string in the corresponding attribute)
- an existing and valid CEDAR folder ID on which you can read/write content on the production server
- an existing and valid CEDAR template ID on which you can read/write content on the production server
- a valid user ID which will become the author of created content (UUID on your CEDAR user profile page, https://cedar.metadatacenter.org/profile)
- a valid [Flow Repository](https://flowrepository.org/) API key.

Integration tests are located under ```/tests/integration```. They rely on API calls and are excluded from the continuous integration builds.


## Exploring an existing set of schemas:

### Use-cases
When you extend or explore set of schemas, whether you are a community trying to create their own specifications, or a data producer trying to comply with a model,
you need to understand the information that is being represented. This usually means a lot of navigation between the interconnected schemas
and context files within that network. For instance, understanding the knowledge of a single property involves opening the corresponding schema file, locating the field and identifying its optional references to other structures. 
You also need to locate the corresponding context files, open them, locate the term and search for it's ontology identifier in a lookup service. And you need to repeat that process for each field of each reference within that field,
and, optionally for each vocabulary system.
<br/> We have written a javascript client side application, the [JSON-Schema Documenter](https://github.com/FAIRsharing/JSONschema-documenter), that does all that for you and 
display the fully resolved network directly in the browser.

The Documenter will allow you to:
- explore the detailed properties of each schema;
- verify that each field is correctly tagged with a resolvable ontology term identifier (e.g.: the ```name``` field of a ```Person``` object is labelled with ```http://purl.obolibrary.org/obo/IAO_0000590``` 
which resolves to ```written name```);
- navigate through bi-directional relationships between the different schemas (parent <-> child);
- identify the reusable components created by other communities so you don't have to reinvent the wheel.


### Usage
If your schemas are living remotely and are accessible through a URL, you can use the [online tool](https://fairsharing.github.io/JSONschema-documenter/) directly by providing your main 
schema URL as a parameter to the tool URL. To do that, add ```?schema_url=yourURL``` at the end of the tool.
<br/> For instance, to view the MIACA network the URL would be ```https://fairsharing.github.io/JSONschema-documenter?schema_url=https://w3id.org/mircat/miacme/schema/miacme_schema.json```

If you also want to add the semantic constrains pulled from the associated context files, you will have to provide a mapping file containing these references that can be generated 
for you using the ```schema2context.generate_context_mapping()``` class method (see [documentation](https://jsonldschema.readthedocs.io/en/latest/utils/schemaUtilities.html#schema2context.generate_context_mapping)). 
You can then upload that mapping file (on github for instance) and provide its URL  as another parameter to the documenter. 
<br/> For MIACA, we would have the following ```https://fairsharing.github.io/JSONschema-documenter/?schema_url=https://w3id.org/mircat/miacme/schema/miacme_schema.json&context_mapping_url=https://w3id.org/mircat/miacme/schema_context_mapping.json```.

If the schemas are living locally only (which is usually the case during development), you can clone the JSON-Schema documenter repository and, optionally,
put it under a web server (such as Apache, Nginx, ...). It will then behave the same way the online service does but can resolve local networks.
<br/>For instance, if the application is deserved through port 8000, your url would be:
 ```localhost:8000/JSONschema-documenter?schema_url=path/to/main/schema.json&context_mapping_url=path/to/context/mapping/file.json```
<br/> We recommend using the ```schemas/``` directory at the root of the application for that purpose.

#### Screenshots of the MIACA network loaded in the jsonschema online documenter:
![alt text](assets/documenter_miaca.png "Documenter loaded with MIACA schema")


## Compare schemas

### Use-cases
Comparing schemas can be particularly useful if you intend on creating **metadata that comply with several models** or to **identify
overlaps with existing networks** when creating or extending set of schemas.
<br/> The key point to understand before comparing schemas or networks is that the comparisons are solely based on ontology labels found
in context files. This implies that:
1) Fields and objects without semantic values will never match anything and will be ignored. To verify if all fields are correctly tagged with an ontology term, 
see above [Exploring an existing set of schemas](#exploring-an-existing-set-of-schemas).
2) Syntactic constrains are ignored when comparing: only the semantic constrains are being considered.
3) Comparisons should be ran within the same contexts: using a schema.org on the one hand, versus a obo markup on the other, will very likely lead to no results.

The python tool will assist you into running the comparison process which will generate an output file containing the comparison results. However, 
to visualize the results, you will need to use a second javascript application, the [compare-and-view](https://github.com/FAIRsharing/JSONschema-compare-and-view) tool.
<br/> A particularity of this tool is that it relies on the Ontology Lookup Service ([OLS](https://www.ebi.ac.uk/ols/index)) API to resolve the machine readable identifier into human readable strings. For instance
```NCBITaxon_9606``` is also shown as ```homo sapien``` when displaying a ```planned process source``` in the context of MIACA and MIACME (see figure [below](#screenshots-of-the-miaca-network-loaded-in-the-jsonschema-online-documenter)).


### Usage
In order to run a comparison between two networks you will have to use the ```FullDiffGenerator``` or  ```FullSemDiff```classes (see [documentation](https://jsonldschema.readthedocs.io/en/latest/semDiff/semDiffIndex.html))
based on your use case. Optionally, you can also run a schema comparison with the ```EntityCoverage``` class 
(see [documentation](https://jsonldschema.readthedocs.io/en/latest/semDiff/semanticComparator.html))
if you are working on a specific schema and don't want to resolve the full networks.
<br> The comparison process is not very intensive but may require to resolve all schemas in the two given networks. This process 
can be long depending on the number and size of the schemas and the properties of the server delivering them.

<br/> These three class will generate a variable containing all overlapping fields and/or schemas, which is not very useful as such.

#### Screenshots of the comparison display between MIACA and MIACME
![alt text](assets/comparator.png "Comparison between MIACA and MIACME")

## Merge schemas

### Use-cases
Useful to import fields from another network.
Keep in mind: merge order A in B is not B in A.

### Usage
...


## Create new context files

### Use-cases
For communities who found a schemas network that describes their needs but consider that the ontology used are not relevant, the easiest route is to extend
rather than recreate. The functionality provided here will help you into generating new context and mapping files so that you can add as many ontology terms as you need.

### Usage
...


## Export schemas in the CEDAR application

### Use-cases
...

### Usage
...


## Import and validate MiFlowCyt dataset

### Use-cases
...

### Usage
...


## (Optional) Identify circularity in schemas

### Use-cases
...

### Usage
...


## License
This code is provided under [BSD 3-Clause License](https://github.com/FAIRsharing/jsonldschema/blob/master/LICENSE.md)

## Contact

- [Alejandra Gonzalez-Beltran](http://github.com/agbeltran)
- [Dominique Batista](http://github.com/terazus)


