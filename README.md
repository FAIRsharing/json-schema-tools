
[![Build Status](https://travis-ci.org/FAIRsharing/jsonldschema.svg?branch=master)](https://travis-ci.org/FAIRsharing/jsonldschema)
[![Coverage Status](https://coveralls.io/repos/github/FAIRsharing/jsonldschema/badge.svg?branch=master)](https://coveralls.io/github/FAIRsharing/jsonldschema?branch=master)
[![Documentation Status](https://readthedocs.org/projects/jsonldschema/badge/?version=latest)](https://jsonldschema.readthedocs.io/en/latest/?badge=latest)


#### Navigation
- [Introduction](#machine-actionable-metadata-models)
1) [Setting up](#setting-up)
2) [Exploring existing JSON schemas in the browser](#exploring-an-existing-set-of-schemas) (requires the jsonschema documenter)
3) [Comparing JSON schemas in the browser](#compare-schemas) (requires the compare-and-view tool)
4) [Merging JSON schemas](#merge-schemas)
5) [Creating new JSON-LD context files or extend existing ones](#create-new-context-files)
6) [Identifying circularity in a set of JSON schemas](#optional-identify-circularity-in-schemas) (requires jsoncycles tool)
7) [A worked example: Importing MiFlowCyt instances](#import-and-validate-miflowcyt-dataset) (dataset) as JSON-LD and validating them against relevant JSON schema set (requires an API key)
8) [Presentations](#presentations)
9) [License](#license)
10) [Contact](#contact)


## Machine Actionable Metadata Models
One of the most common formats to exchange data over the web is the **JavaScript Object Notation** (**JSON**). It is a popular open-standard that can be used to represent data instances and also to represent syntactic constraints a given object should comply with. These syntactic constraints can be represented as **JSON schemas**. The **JSON-Schema** specification informs about the properties of an object. Among those, one may find names, 
descriptions, values, cardinality and so on.
<br/> The specification provides a powerful mechanism (the ```$ref``` keyword) to create links between schemas called references. An easy to understand example is the relationship between an ```Organization``` and a ```Person``` through 
the ```employee``` property. In some rare cases, an employee could also be another organization or even both at the 
 same time (a single self-employed person hired as a service provider through his own company). JSON-Schema supports these types of relationships through the use of the ```anyOf```, ```oneOf``` and ```allOf``` keywords.
<br/> These references give the ability to create very complex oriented graphs (possibly cyclic ones, where each
vertex is a _schema_ and each edge a _relationship between two schemas_. In this documentation we will refer to these interconnected structures as **networks**.

Networks allow to represent very dense sets of objects which may become difficult to follow when the numbers of properties and relationships reaches certain thresholds.
<br/>Adding to the complexity, semantic constraints should also be taken into consideration for machine readability. This extra layer creates an even more complex specification to deal with.

#### Separating syntactic and semantic layers:
![alt text](assets/separation_of_concerns.png "Figure 1: Separation of semantic and syntactic concerns")

In order to cope with both the semantic and syntactic concerns, the semantic layer was separated from the schemas and included in context files following the **JSON-LD** specification. Each schema is bound to a set of context 
files (through mapping files) that deliver the ontology term identifiers for each of the schema properties. 
<br/> This allows to reuse or extend existing schemas or networks easily with new vocabulary terms and to have different mappings to ontologies living side by side, for different purposes and different communities.

This repository provides a python3 toolkit that helps users create, compare, merge and explore schemas and their associated context files. It thus provides the means to 
increase the existing pool of **machine** and **human readable models** that describe the **syntactic** and **semantic constraints** of an object **metadata**.
<br/> This is an essential functionality, in the context of data **Findability**, **Accessibility**, **Integrability** and **Reusablity** ([FAIR](https://doi.org/10.1038/sdata.2016.18)) 
especially when considering the representation of minimal information checklists, which are often textual artefacts lacking machine readability. 


#### Inputs
The input networks used in the toolkit's tests are the following:
- Minimum Information About Cell Assays: **[MIACA](https://github.com/FAIRsharing/mircat/tree/master/miaca)** 
- Minimum Information About Cell Migration Experiments: **[MIACME](https://github.com/FAIRsharing/mircat/tree/master/miacme)**
- Data Tag Suite: **DATS** [schemas](https://github.com/datatagsuite/schema) and [context](https://github.com/datatagsuite/context)
- Minimum Information About Flow Cytometry Experiments: **[MiFlowCyt](https://github.com/FAIRsharing/mircat/tree/master/miflowcyt)**



## 1. Setting Up:

First, you will need to set up a virtual environment, then import the code and install dependencies:
```
virtualenv venv
source venv/bin/activate
git clone https://github.com/FAIRsharing/jsonldschema.git
cd jsonldschema
pip install -r requirements.txt
```

If you plan on using either the [CEDAR](https://metadatacenter.org/) exporter or the MiFlowCyt importer, you will also need to provide your API keys through 
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

Integration tests are located under ```/tests/integration```. They rely on API calls and are therefore excluded from the continuous integration builds.


## 2. Exploring existing JSON schemas:

### Use case:
When exploring or looking at extending a set of schemas, whether you are a community trying to create their own specifications or a data producer trying to comply with a model,
you need to understand the information that is being represented. This usually means a lot of navigation between the interconnected schemas
and context files within a network. 
<br/>For instance, understanding the knowledge of a single property involves opening the corresponding schema file, locating the field and identifying its optional references to other structures. 
You also need to locate the corresponding context files, open them, locate the term and search for its ontology identifier in a lookup service. And you need to repeat that process for each field of each reference within that field,
and, optionally, for each vocabulary system you need to deal with. This is tedious, time consuming and error prone process.
<br/> We have written a Javascript client-side application, the [JSON-Schema Documenter](https://github.com/FAIRsharing/JSONschema-documenter), that does all that for you and 
displays the fully resolved network directly in the browser.

The Documenter will allow you to:
- explore the detailed properties of each schema;
- verify that each field is correctly tagged with a resolvable ontology term identifier (e.g.: the ```name``` field of a ```Person``` object is labelled with ```http://purl.obolibrary.org/obo/IAO_0000590``` 
which resolves to ```written name```) and, thus, the correctness of your context files;
- identify and navigate through the bi-directional relationships between the different schemas;
- identify reusable components created by other communities to ensure that you don't reinvent the wheel.


### Usage
If your schemas live remotely and are accessible through a URL, you may use the [online tool](https://fairsharing.github.io/JSONschema-documenter/) directly by providing your main 
schema URL as a parameter to the tool URL. To do that, add ```?schema_url=yourURL``` at the end of the tool.
<br/> For instance, to view the MIACA network, the URL would be ```https://fairsharing.github.io/JSONschema-documenter?schema_url=https://w3id.org/mircat/miacme/schema/miacme_schema.json```

If you also want to add the semantic constraints pulled from the associated context files, you will have to provide a mapping file containing those references. These can actually be generated 
for you using the ```schema2context.generate_context_mapping()``` class method (see [documentation](https://jsonldschema.readthedocs.io/en/latest/utils/schemaUtilities.html#schema2context.generate_context_mapping)). 
You can then upload the resulting mapping file (e.g. on GitHub) and provide its URL as an additional parameter to the JSONSchema-documenter. 
<br/> For MIACA, we would have the following: ```https://fairsharing.github.io/JSONschema-documenter/?schema_url=https://w3id.org/mircat/miacme/schema/miacme_schema.json&context_mapping_url=https://w3id.org/mircat/miacme/schema_context_mapping.json```.

If the schemas live only locally (which is usually the case during development), you may clone the JSON-Schema documenter repository and, optionally,
put it under a web server (such as Apache or Nginx). It will then behave in the same way as the online service does but will only resolve local networks.
<br/>For instance, if the application is served through port 8000, your URL will be:
 ```localhost:8000/JSONschema-documenter?schema_url=path/to/main/schema.json&context_mapping_url=path/to/context/mapping/file.json```
<br/> We recommend using the ```schemas/``` directory at the root of the application for that purpose.

#### Screenshots of the MIACA network loaded in the jsonschema online documenter:
![alt text](assets/documenter_miaca.png "Figure 2: JSON-schema Documenter loaded with MIACA schema")


## 3. Comparing JSON schemas

### Use case:
Comparing schemas can be particularly useful if you intend on creating **metadata that must comply with several models** or to **identify
overlaps with existing networks** when creating or extending sets of schemas.
<br/> The key point to understand before comparing schemas or networks is that the comparisons are solely based on ontology labels found
in the [JSON-LD context](http://niem.github.io/json/reference/json-ld/context/) files. This implies that:
1) Fields and objects without semantic values will never match to anything and will be ignored. To verify if all fields are correctly tagged with an ontology term, 
see above [Exploring an existing set of schemas](#exploring-an-existing-set-of-schemas).
2) Syntactic constraints are ignored when comparing: **only the semantic constraints are being considered**.
3) Comparisons should be ran within the same semantic contexts: For instance, comparing a schema.org context versus a OBO markup will very likely lead to no results.

This Python tool will assist you with running the comparison process, which will generate an output file containing the comparison results. To visualise the results, you will need to use a second Javascript application, the [compare-and-view](https://github.com/FAIRsharing/JSONschema-compare-and-view) tool.
<br/> A particularity of this tool is that it relies on the Ontology Lookup Service ([OLS](https://www.ebi.ac.uk/ols/index)) API to resolve the machine readable identifiers into human readable strings. For instance
```NCBITaxon_9606``` is also shown as ```homo sapiens``` when displaying the ```source``` of a ```planned process``` in the context of MIACA and MIACME (see figure [below](#screenshots-of-the-miaca-network-loaded-in-the-jsonschema-online-documenter)).
<br/> This is key to understand the definition held by each property. The property names, which can be found in the schemas, are human readable representations and do not carry the meaning of the property. That meaning is resolved
using the ontology identifiers found in the context files. Thus, properties with the same name may not represent the same thing and properties with different names could actually mean the same thing. For instance, both MIACA and MIACME have a 
```planned process``` representation that have different names (```project``` for MIACA and ```investigation``` for MIACME).
<br/> This is the main reason why the comparison align schemas and properties based on the ontology terms and not on the object names.


### Usage:
In order to run a comparison between two networks, you will have to use the [```FullDiffGenerator``` or  ```FullSemDiff```classes](https://jsonldschema.readthedocs.io/en/latest/semDiff/semDiffIndex.html)
based on your use case. Optionally, you can also run a schema comparison with the [```EntityCoverage```](https://jsonldschema.readthedocs.io/en/latest/semDiff/semanticComparator.html) class if you are working on a specific schema and don't want to resolve the full network.
<br> The comparison process is not very intensive but may require to resolve all schemas in the two given networks. This process 
can be long depending on the number and size of the schemas and the properties of the server delivering them.


#### Screenshots of the comparison display between MIACA and MIACME
![alt text](assets/comparator.png "Figure 3: Comparison between MIACA and MIACME")


## 4. Merging JSON schemas

### Use case:
Merging is the logical extension of the comparison functions. It will help you **import properties** and **schemas** from one network to another without
manually processing each single item or without creating references to external networks out of your control and, thus, can change at any point in time.
<br/> Manual merges can be very easy if the schema you need to reuse is simple and do not have any reference. Just copy paste the schema file and its context files.
If the schema has references, though, you will be required to either remove these references or copy all nested children and their context.
<br/> You may want to let the code do that for you in that case.

The way the merge is implemented relies on the output of the comparison. If two schemas are labelled with the same ontology identifier
they can be merged. The algorithm will pull all fields and their references from the second schema and recursively add them to the first if they are not already there. If will also change all names and identifiers as required.
<br/> The most important consequence is that the merge order will have a high impact on the final output: merging B into A or A into B will not generate the same result.
 
The combination of the comparison and merge functions make a very good tool to verify your output. Running a first comparison, merging and running secondary comparison with the two merge inputs allows to verify the integrity of the output and that it matches the desired result.

### Usage:
Coming up soon, please refer to the documentation.

If you are creating a network and wish to import a schema, you need to create the base file, stripped of property fields, and add it to your network through the corresponding reference.
 Identify the ontology term that this object will be labelled with (it needs to be the same as the schema you want to import from) 
 and add it to the corresponding context file. When running the merge, the object, its references and their respective context files will be added to the output.
 <br/> Note: the input is never modified, a third network is created for you instead.

## 5. Creating new JSON-LD context files or extend existing ones

### Use case:
This functionality is extremely important to **allow different communities** that agreed on syntactic constraints (JSON schemas) **to use different ontologies** (thus, distinct semantic constraints) in the JSON-LD context files. This enables, for instance, to have
```DCAT```, ```schema.org``` and ```OBO``` markups describing the same schemas. 
<br/>This is also key when one wants to comply with the syntactic constraints of a schema
but can not use (or disagrees with) the proposed ontology terms. Rather than creating a new network from scratch, an easier and more reusable solution is to extend the existing one.
<br />The code will assist you into creating the context files, pre-populated with the desired ontology prefixes and URL, and the corresponding mapping files.
<br> Unfortunately, in the absence of more advanced solutions (AI or otherwise), the library cannot guess ontology terms. Thus, users will have to perform ontology terms and identifiers lookup themselves and manually add them
to the corresponding field in the corresponding context files that have been created for that purpose.

### Usage:
Coming up soon, please refer to [documentation](https://jsonldschema.readthedocs.io/en/latest/utils/schemaUtilities.html).


## 6. (Optional) Identify circularity in schemas

### Use case:
As touched upon in the introduction, some networks and schemas, due to the ability to reference each others, may become fairly complex and harbour circularity. Besides being harder to navigate for human beings,
such occurrences may also create algorithmic issues including endless loops, recursive caps and so on. In very rare cases, it could even lead to a crash of the target host by triggering an uncaught endless loop.
It is therefore a good thing to check for circularity in JSON schema networks and be aware of those.
<br/> This library component, using First Depth Search approach, will identify circularity between schemas in a network and return them as an array.

### Usage:
Please refer to [JSON-Cycles](https://github.com/FAIRsharing/jsonCycles) and the following [jupyter notebook](https://github.com/FAIRsharing/jsonCycles/blob/master/notebooks/Finding_jsonCycles.ipynb).


## 7. Import and validate MiFlowCyt dataset

### Use case:
The purpose of this section is to showcase how the code works and how the various functionalities can be used.
**(This code will not be relevant to developers or data providers trying to create their own set of schemas.)**

Using the JSON-Documenter, the JSON-schema comparator and the JSON-LD context file assistance, the ```Minimum Information About Flow Cytometry Experiments checklist``` was expressed as JSON-Schemas and tagged with ontology terms from [OBO foundry](http://www.obofoundry.org/).
<br/> The code in the module is a client implementation of the Flow Repository API, which delivers ```MiFlowCyt``` datasets in XML format.
<br/> The XML data is progressively transformed to a simple JSON into which are injected the properties required by the JSON-LD specifications.
<br/> The output is then syntactically validated against the corresponding MiFlowCyt schemas and, if valid, pushed to a FireBase real-time database (see [figure 4](#valid-miflowcyt-json-ld-instance-extracted-and-transformed-from-flow-repository)).

#### Valid MiFlowCyt JSON-LD instance extracted and transformed from Flow Repository and added to a FireBase real-time database:
![alt text](assets/miflowcyt_firebase_export.png "Figure 4: MiFlowcyt in Firebase")

### Usage:
Coming up soon, please refer to the [documentation](https://jsonldschema.readthedocs.io/en/latest/validation/validationUsage.html).


# Presentations 

- BOSC 2019 - details to follow
- [Machine Actionable Metadata Models: JSONLD-Schema and JSON-Schema documenter](https://doi.org/10.5281/zenodo.2558716) by Gonzalez-Beltran and Batista, Research Software London & South East Workshop, 7th February 2019, London, UK
- [FAIR metadata standards](https://doi.org/10.6084/m9.figshare.7206518.v1), by Gonzalez-Beltran, Rocca-Serra and Sansone at the Inaugural Workshop on Metadata for Machines, GO-FAIR initiative, 15th October 2018, Leiden, Netherlands



## License
This code is provided under [BSD 3-Clause License](https://github.com/FAIRsharing/jsonldschema/blob/master/LICENSE.md)

## Contact

- [Dominique Batista](http://github.com/terazus)
- [Philippe Rocca-Serra](https://github.com/proccaserra)

