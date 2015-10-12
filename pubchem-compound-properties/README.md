My attempt to solve following problem posted on StackOverflow:
http://stackoverflow.com/questions/32634430/r-parse-json-xml-exported-compound-properties-from-pubchem/

The main limitation is that to extract all data, each file must be parsed and processed two times. This is not a problem for few molecules, but might impact performance considerably on larger samples.

Also, the code here expects to have PubChem's XML files already available in working directory. Names of files are not names that PubChem will provide by default. In real world you would probably have to write routines to download files before processing them.
