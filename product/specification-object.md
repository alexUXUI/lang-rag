Specification Objects for MVP Release

Version 2.0.0 Active
Data Model for MVP Release of Requirements Management Targeted
December 2024
Change Date Author(s)
Requirements Management Milestone 1 Release [Targeted June 2024]
Document Created April 26, 2024 Denis Postanogov, Marina Chernyshevich
Document reviewed and updated April 29, 2024 Denis Postanogov,
Marina Chernyshevich, Andrei Krutsko, Viachaslau
Murashka, PAVEL HANCHAROU, Oleg Tarazevich, Alexandre
Mikhalev, Ignat Naumovich, Vadim Stankevitch
Update per Issue 567003: "uid" renamed
to “id”
May 1, 2024 Ignat Naumovich
Added “Data Lineage/Object Identities”
section to clarify the “id” attribute
May 2, 2024 Ignat Naumovich
Requirements Management MVP Release [Targeted December 2024]
Created new version 2.0.0 of the
document as copy of Specification
Objects - Milestone 1.docx – now in
‘Revised’ state
August 27, 2024 Denis Postanogov
Added section “Object’s Positional Index”.
Added property “index” to provide reading
order as needed by Senso.
August 27, 2024 Denis Postanogov, Andrei Krutsko, Siarhei Krauchanka
Added property “context” to make
specification objects compliant with the
needs of Senso
August 30, 2024 Denis Postanogov
Provided definitions of Type of
Specification Object, Specification Table,
Specification Table Row, and
Specification Figure.
September 5, 2024 Denis Postanogov
Added section “3 Specification Document
Metadata”
September 25, 2024 Denis Postanogov
Added term “Metadata” in “Terminology”
section
September 25, 2024 Denis Postanogov
Field “filename” excluded from
Specification Document Metadata
payload.
October 10, 2024 Denis Postanogov
Added “Object’s Context” section. October 10, 2024 Denis Postanogov
Added “rows” field for Specification Table
payload to support ReqIF table rendering
in XHTML.
October 14, 2024 Denis Postanogov
1 Contents
2 Terminology .......................................................................................................... 2
3 Specification Document Metadata.......................................................................... 4
4 Types of Specification Objects ................................................................................ 4
4.1 Specification Clause ........................................................................................ 4
4.2 Specification Statement ................................................................................... 6
4.3 Specification Table .......................................................................................... 84.4 Specification Table Row ................................................................................. 10
4.5 Specification Figure ....................................................................................... 11
5 Data Lineage and Purpose .................................................................................... 12
5.1 Text Normalization ......................................................................................... 12
5.2 Source of Title Text ......................................................................................... 13
5.3 Source of Content Text ................................................................................... 13
5.4 Source of Content Regions ............................................................................. 13
5.5 Source of Entities .......................................................................................... 13
5.6 Object Identities ............................................................................................ 14
5.7 Object’s Positional Index ................................................................................ 14
5.8 Object’s Context ............................................................................................ 15
6 Objects Representation on UI (Milestone 1) ........................................................... 16
6.1 Object Snippets in Topics Tree ........................................................................ 16
6.2 Object Representation on the Document Pages ............................................... 16
6.3 Object Details View ....................................................................................... 17
6.4 Examples of Objects Representation ............................................................... 17
6.4.1 Specification Clause View Example .......................................................... 17
6.4.2 Specification Table View Example ............................................................. 18
6.4.3 Specification Figure View Example ............................................................ 19
7 References ......................................................................................................... 19
8 Issues to Resolve ................................................................................................. 20
2 Terminology
Specification object A structured object of a specific format corresponding to
one of the supported types, extracted from a specification
document, and representing an element of requirements
engineering domain that is suitable for requirements
management processes.Specification objects can correspond to individual work
items stored in PLM systems (e.g. Polarion, Codebeamer,
Doors, etc.).
A specification object describes a condition or capability
that a system, product, or component must possess to
achieve a specific objective or fulfill a stakeholder need.
They serve as the foundation for the design, development,
and evaluation of engineering systems, guiding the entire
lifecycle of the project from conception to deployment.
Specification document A document represented as a file of one of the supported
formats (PDF), which has a content of requirements
engineering domain, including:
• Industry standards
• Internal engineering specifications
Paragraph A composite element of a document that exposes clear set
of visual features that make it stand out as a single
sequence of textual content (e.g., separated from other
paragraphs with a hard-break newline).
DocStruct extracts paragraphs from documents with the
purpose of providing input blocks of text for
semantic/syntactic/linguistic analysis, in which a basic text
normalization has been performed (de-hyphenation, font
character codes normalization, etc.).
Span A fragment of document’s text, corresponding to
rectangular region on a page, and consisting of equally
styled characters that are positioned in the same line
without major whitespace gaps or graphical breakers.
DocStruct extracts spans from document so that they can
be used as building blocks for paragraphs, and bear styling
(font family, font size) and positional information
(rectangular region on the page) in the document.
Metadata A structured information that describes and provides
context for data object such as a document. In the context
of an engineering specification, metadata includes specific
fields and corresponding values that represent key
attributes of the document.3 Specification Document Metadata
When externally provided metadata for a specification document is unavailable, it
becomes critical to obtain this information through automatic detection within the
document body. This ensures that essential metadata is not overlooked, enabling proper
classification, retrieval, and management of the document. The automated extraction of
metadata compensates for the absence of external metadata sources, ensuring the
integrity and accessibility of the document's key attributes.
The Decomposition Service leverages machine learning models and natural language
processing algorithms to automatically detect and extract metadata fields from the
document text. Provided that the input document is of the engineering specification type,
the service identifies specific relevant fields such as the specification title, authors, and
date, document number and revision tag.
{
"type": string = "document",
"pageCount": integer, # number of pages in the document
"languages": OPT [
# list of languages recognized in the document ordered in descending mode by proportion of the language in document, and represented as
ISO 639-3 code, e.g. ["eng", "deu"]
string
],
"specificationMetadata": OPT {
# metadata fields automatically extracted from a specification document
"title": OPT string, # recognized title of document
"documentNumber": OPT string, # recognized specification document number
"authors": OPT [
# list of recognized document authors
string
],
"revisionTag": OPT string, # recognized revision tag of a specification document
"date": OPT string # date in "YYYY-MM-DD" format recognized in the document; can represent publication date or other types of dates from
information fields
}
}
4 Types of Specification Objects
A Type of Specification Object is a distinct category of a content unit within a specification
document, identified by its format, level of granularity, and function. Each type represents a
particular form, such as a Clause, Statement, Table, Table Row, or Figure, that
encapsulates meaningful technical or directive content related to the document's purpose
and requirements.
4.1 Specification Clause
A Specification Clause is a specification object of paragraph level, i.e., it fully contains one
or more paragraphs (sometimes with numerical identifiers), having a purpose to unite textsentences that together express a single idea or unit of information. In ideal scenario, a
specification clause consists of a group of sentences that sets the conditions, outcomes
and recommendations around one specific problem.
Specification Clauses are extracted from most of the document’s content excluding the
document parts that serve meta-information, such as document title and document
information blocks, and Table of Contents.
Specification Clause Payload
{
"type": string = "clause",
"id": string, # non-persistent ID of the object. It may or may not be unique in the CINT perimeter. Consumer of the API must admit it should not
be stored in data storages
"index": integer, # relative position index of the object in the text flow of document
"content": {
# Main content of the Specification Clause object
"text": string, # Normalized text of the object: hyphenation is resolved, paragraph spans are joined with space, paragraphs are delimited
with NEWLINE character (\n); table cells are delimited with TAB character (\t) for Table and TableRow content text
"regions": [
# Location of the text on the document's page(s) defined by rectangular regions
{
"page": integer, # Number of the document's page, on which the object's region is located; starts from 1
"rect": [X1: number, Y1: number, X2: number, Y2: number] # coordinates of the corner points ((X1,Y1) is top-left corner and
(X2,Y2) is bottom-right corner) of the bounding rectangle around the object's text span in the document, provided as 4 floating
numbers in ratio units relative to the width and height of the page
"angle": OPT number (default: 0) # angle of rotation of the object's bounding rectangle around its center, applied to horizontal
text, in degree units
}
]
},
"context": {
# Context of the object in the document structure
"parents": [
# List of parents of the object in the hierarchical document structure ordered from top to bottom
{
"text": string, # Text of the parent context element
"role": string = "heading" | "caption" | "ancestor" | "number" # Role of the parent in relation to the object
}
],
"section": {
# Closest parent section of the object
"title": string # Title of the section
}
},
"entities": [
# List of associated named entities extracted from object's text
{
"class": string = "equipment" | "material" | "parameter" | "reference", # Named entity class
"text": string, # Normalized text of the entity extracted from the source text: singular form, standard letter-case
"source": string = "content" | "title", # Source field of the object, from text of which the entity has been extracted
"offsets": [
# Offsets for highlighting of the entity in the source text to be used for highlighting in the text snippet
{
"start": integer, # Start offset of the entity in the source text
"length": integer # Quantity of characters in the source text that belong to the entity; NOTE: entity 'metal' can have offset
length 6 corresponding to 'metals' in the text
}
],
"groups": [string] # Categorization groups for building the multi-level entity tree
}
],
"path": [# Path to the object in the document's content, including titles of sections and tables, to which the object belongs, ordered top to bottom
{
"text": string # Heading or caption of the path object
}
]
}
4.2 Specification Statement
Specification statement is a specification object of a sentence level, contained in the
clauses from the document sections that provide specification language, thus excluding
such sections as Table of Contents, References, Glossary and Terminology, Change Log,
Acknowledgements, etc.
Statement-type specification objects differ by their directive power (specification).
Decomposition Services (Rune) provides so-called Condensed Classification of statement
objects by setting the value of their “specification” property, according to the Table 3.2.1
below – column “Condensed Classification of Statements by Specification”.
NOTE: Property name “specification” is not ideal. Initial working title was “severity” but after
discussions with the product team, it was decided to rename it to “specification”. The name
can change in future and be provided proper communication.
Table 3.2.1. Classification of Statements by Specification
Language Condensed Classification
of Statements by
Specification
Fine-Grained
Classification of
Statements by
Specification
*NOT USED*
SHALL, MUST, HAVE TO, NEEDED,
REQUIRED, MANDATORY, OBLIGATORY,
COMPULSORY, NECESSARY,
INDISPENSABLE, IMPERATIVE, VITAL,
CRUCIAL, ESSENTIAL, CRITICAL, ALL-
IMPORTANT, SHALL ONLY, etc.
Requirement
Statements mandating
specific actions, features, or
qualities that must be present
or adhered to within a system.
Requirement
Statements mandating
specific actions, features, or
qualities that must be present
or adhered to within a system.
SHALL NOT, MUST NOT, PROHIBITED, NOT
PERMITTED, NOT ALLOWED, SHALL
AVOID, NOT ACCEPTABLE,
UNACCEPTABLE, etc.
Prohibition
Statements explicitly
forbidding certain actions,
features, or behaviors within a
system.
Prohibition
Statements explicitly
forbidding certain actions,
features, or behaviors within a
system.
SHOULD, RECOMMENDED, SUGGESTED,
EXPECTED, DESIRED, PREFERRED, MAY
BE REQUIRED, CAN BE REQUIRED, TAKE
CARE, etc.
Guidance
Statements providing direction
or advice regarding actions,
features, or behaviors within a
system, encompassing
recommendations,
restrictions, permissions, and
rejections to guide
Recommendation
Statements suggesting
preferred or advisable actions,
features, or behaviors within a
system.
SHOULD NOT, NOT RECOMMENDED, NOT
EXPECTED, UNDESIRABLE, CAN ONLY,
etc.
Restriction
Statements advising against or
limiting certain actions,development and usage
effectively.
features, or behaviors within a
system.
CAN, MAY, ACCEPTED, ACCEPTABLE,
APPLICABLE, etc.
Permission
Statements granting
authorization or allowance for
specific actions, features, or
behaviors within a system.
CANNOT, CAN NOT, MAY NOT, etc. Rejection
Statements indicating the
impossibility or non-allowance
of certain actions, features, or
behaviors within a system.
IS, ARE, IS NOT, ARE NOT, WILL, WILL NOT,
COULD, COULD NOT, MIGHT, MIGHT NOT,
etc.
Info
Statements providing factual
information or descriptions
about the system, its
components, or its
functionalities, without
implying requirements or
restrictions.
Info
Statements providing factual
information or descriptions
about the system, its
components, or its
functionalities, without
implying requirements or
restrictions.
Specification Statement Payload
The following payload shall be provided to Denali team for the purpose of viewing the
specification objects in Document Viewer, forming snippets in Topics Tree (left panel) and
providing object’s details when object is clicked (right panel).
{
"type": string = "statement",
"id": string, # non-persistent ID of the object. It may or may not be unique in the CINT perimeter. Consumer of the API must admit it should not
be stored in data storages
"index": integer, # relative position index of the object in the text flow of document
"content": {
# Content of the Specification Statement object
"text": string, # Normalized text of the object: hyphenation is resolved, paragraph spans are joined with space, paragraphs are delimited
with NEWLINE character (\n); table cells are delimited with TAB character (\t) for Table and TableRow content text
"regions": [
# Location of the text on the document's page(s) defined by rectangular regions
{
"page": integer, # Number of the document's page, on which the object's region is located; starts from 1
"rect": [X1: number, Y1: number, X2: number, Y2: number] # coordinates of the corner points ((X1,Y1) is top-left corner and
(X2,Y2) is bottom-right corner) of the bounding rectangle around the object's text span in the document, provided as 4 floating
numbers in ratio units relative to the width and height of the page
"angle": OPT number (default: 0) # angle of rotation of the object's bounding rectangle around its center, applied to horizontal
text, in degree units
}
]
},
"context": {
# Context of the object in the document structure
"parents": [
# List of parents of the object in the hierarchical document structure ordered from top to bottom
{
"text": string, # Text of the parent context element
"role": string = "heading" | "caption" | "ancestor" | "number" # Role of the parent in relation to the object
}
],"section": {
# Closest parent section of the object
"title": string # Title of the section
}
},
"entities": [
# List of associated named entities extracted from object's text
{
"class": string = "equipment" | "material" | "parameter" | "reference", # Named entity class
"text": string, # Normalized text of the entity extracted from the source text: singular form, standard letter-case
"source": string = "content" | "title", # Source field of the object, from text of which the entity has been extracted
"offsets": [
# Offsets for highlighting of the entity in the source text to be used for highlighting in the text snippet
{
"start": integer, # Start offset of the entity in the source text
"length": integer # Quantity of characters in the source text that belong to the entity; NOTE: entity 'metal' can have offset
length 6 corresponding to 'metals' in the text
}
],
"groups": [string] # Categorization groups for building the multi-level entity tree
}
],
"specification": string = "requirement" | "guidance" | "info" | "prohibition", # The specification category of the statement (e.g. SHALL-
sentences have "requirement" specification category)
"path": [
# Path to the object in the document's content, including titles of sections and tables, to which the object belongs, ordered top to bottom
{
"text": string # Heading or caption of the path object
}
]
}
4.3 Specification Table
A Specification Table is a specification object representing an individual element having
table formatting within a specification document. In general, tables encapsulate detailed,
formatted information critical to the understanding of the engineering requirements.
Specification Table objects are automatically extracted from the document by detecting
tables in PDF files, which may sometimes lead to errors in complex scenarios, such as
tables spanning multiple pages, irregular layouts, or nested tables. Specification Table
objects are extracted from document sections that provide specification content,
excluding meta-information sections such as References, Glossary, and
Acknowledgments.
Specification Table Payload
The following payload shall be provided to Denali team for the purpose of viewing the
specification objects in Document Viewer, forming snippets in Topics Tree (left panel) and
providing object’s details when object is clicked (right panel).
{
"type": string = "table",
"id": string, # non-persistent ID of the object. It may or may not be unique in the CINT perimeter. Consumer of the API must admit it should not be stored in data
storages
"index": integer, # relative position index of the object in the text flow of document
"title": OPT {# Title of the Specification Table
"text": string, # Normalized text of the object: hyphenation is resolved, paragraph spans are joined with space, paragraphs are delimited with NEWLINE character
(\n); table cells are delimited with TAB character (\t) for Table and TableRow content text
"regions": [
# Location of the text on the document's page(s) defined by rectangular regions
{
"page": integer, # Number of the document's page, on which the object's region is located; starts from 1
"rect": [X1: number, Y1: number, X2: number, Y2: number] # coordinates of the corner points ((X1,Y1) is top-left corner and (X2,Y2) is bottom-
right corner) of the bounding rectangle around the object's text span in the document, provided as 4 floating numbers in ratio units relative to the
width and height of the page
"angle": OPT number (default: 0) # angle of rotation of the object's bounding rectangle around its center, applied to horizontal text, in degree units
}
]
},
"content": {
# Content of the Specification Table
"text": string, # Normalized text of the object: hyphenation is resolved, paragraph spans are joined with space, paragraphs are delimited with NEWLINE character
(\n); table cells are delimited with TAB character (\t) for Table and TableRow content text
"regions": [
# Location of the text on the document's page(s) defined by rectangular regions
{
"page": integer, # Number of the document's page, on which the object's region is located; starts from 1
"rect": [X1: number, Y1: number, X2: number, Y2: number] # coordinates of the corner points ((X1,Y1) is top-left corner and (X2,Y2) is bottom-
right corner) of the bounding rectangle around the object's text span in the document, provided as 4 floating numbers in ratio units relative to the
width and height of the page
"angle": OPT number (default: 0) # angle of rotation of the object's bounding rectangle around its center, applied to horizontal text, in degree units
}
],
"rows": OPT [
# List of table rows
{
"cells": [
# List of cells of the row
{
"text": OPT string, # Normalized text of the table cell: hyphenation is resolved, paragraph spans are joined with space, paragraphs are
delimited with NEWLINE character (\n)
"rowSpan": OPT integer, (default: 1) # Number of rows for the merged cell
"colSpan": OPT integer (default: 1) # Number of columns for the merged cell
}
]
}
]
},
"context": {
# Context of the object in the document structure
"section": {
# Closest parent section of the object
"title": string # Title of the section
}
},
"entities": [
# List of associated named entities extracted from object's text
{
"class": string = "equipment" | "material" | "parameter" | "reference", # Named entity class
"text": string, # Normalized text of the entity extracted from the source text: singular form, standard letter-case
"source": string = "content" | "title", # Source field of the object, from text of which the entity has been extracted
"offsets": [
# Offsets for highlighting of the entity in the source text to be used for highlighting in the text snippet
{
"start": integer, # Start offset of the entity in the source text
"length": integer # Quantity of characters in the source text that belong to the entity; NOTE: entity 'metal' can have offset length 6
corresponding to 'metals' in the text
}
],
"groups": [string] # Categorization groups for building the multi-level entity tree
}
],
"path": [
# Path to the object in the document's content, including titles of sections and tables, to which the object belongs, ordered top to bottom
{
"text": string # Heading or caption of the path object}
]
}
4.4 Specification Table Row
A Specification Table Row is a specification object representing an individual row within a
Specification Table object extracted from a specification document. Each row consists of
multiple cells, where the content is presented in a normalized format with cell values
separated by tabs. Specification Table Rows are automatically detected and extracted from
tables in PDF documents, which may sometimes lead to errors in cases of complex table
structures, such as merged cells or multi-page tables. Specification Table Rows help
further break down the tabular data into more granular units for detailed analysis of the
specification’s technical content.
Specification Table Row Payload
The following payload shall be provided to Denali team for the purpose of viewing the
specification objects in Document Viewer, potentially for forming snippets in Topics Tree
(left panel) and providing object’s details when object is clicked (right panel).
{
"type": string = "tableRow",
"id": string, # non-persistent ID of the object. It may or may not be unique in the CINT perimeter. Consumer of the API must admit it should not
be stored in data storages
"index": integer, # relative position index of the object in the text flow of document
"content": {
# Content of the Specification Table Row
"text": string, # Normalized text of the object: hyphenation is resolved, paragraph spans are joined with space, paragraphs are delimited
with NEWLINE character (\n); table cells are delimited with TAB character (\t) for Table and TableRow content text
"regions": [
# Location of the text on the document's page(s) defined by rectangular regions
{
"page": integer, # Number of the document's page, on which the object's region is located; starts from 1
"rect": [X1: number, Y1: number, X2: number, Y2: number] # coordinates of the corner points ((X1,Y1) is top-left corner and
(X2,Y2) is bottom-right corner) of the bounding rectangle around the object's text span in the document, provided as 4 floating
numbers in ratio units relative to the width and height of the page
"angle": OPT number (default: 0) # angle of rotation of the object's bounding rectangle around its center, applied to horizontal
text, in degree units
}
]
},
"context": {
# Context of the object in the document structure
"section": {
# Closest parent section of the object
"title": string # Title of the section
}
},
"entities": [
# List of associated named entities extracted from object's text
{
"class": string = "equipment" | "material" | "parameter" | "reference", # Named entity class
"text": string, # Normalized text of the entity extracted from the source text: singular form, standard letter-case
"source": string = "content" | "title", # Source field of the object, from text of which the entity has been extracted
"offsets": [# Offsets for highlighting of the entity in the source text to be used for highlighting in the text snippet
{
"start": integer, # Start offset of the entity in the source text
"length": integer # Quantity of characters in the source text that belong to the entity; NOTE: entity 'metal' can have offset
length 6 corresponding to 'metals' in the text
}
],
"groups": [string] # Categorization groups for building the multi-level entity tree
}
],
"path": [
# Path to the object in the document's content, including titles of sections and tables, to which the object belongs, ordered top to bottom
{
"text": string # Heading or caption of the path object
}
]
}
4.5 Specification Figure
A Specification Figure is a specification object representing a visual element, such as a
diagram, chart, image, or graph, extracted from a specification document. Each figure may
include an associated title (caption) and accompanying text content (e.g. labels on a chart
diagram). Figures are automatically detected and extracted from PDF documents, which
may lead to errors in complex layouts or multi-part visuals. Specification Figures serve as
an important component of a document that complement or enhance the understanding
of the technical content and requirements.
Specification Figure Payload
The following payload shall be provided to Denali team for the purpose of viewing the
specification objects in Document Viewer, forming snippets in Topics Tree (left panel) and
providing object’s details when object is clicked (right panel).
{
"type": string = "figure",
"id": string, # non-persistent ID of the object. It may or may not be unique in the CINT perimeter. Consumer of the API must admit it should not be stored in data
storages
"index": integer, # relative position index of the object in the text flow of document
"title": OPT {
# Title of the Specification Figure
"text": string, # Normalized text of the object: hyphenation is resolved, paragraph spans are joined with space, paragraphs are delimited with NEWLINE character
(\n); table cells are delimited with TAB character (\t) for Table and TableRow content text
"regions": [
# Location of the text on the document's page(s) defined by rectangular regions
{
"page": integer, # Number of the document's page, on which the object's region is located; starts from 1
"rect": [X1: number, Y1: number, X2: number, Y2: number] # coordinates of the corner points ((X1,Y1) is top-left corner and (X2,Y2) is bottom-
right corner) of the bounding rectangle around the object's text span in the document, provided as 4 floating numbers in ratio units relative to the
width and height of the page
"angle": OPT number (default: 0) # angle of rotation of the object's bounding rectangle around its center, applied to horizontal text, in degree units
}
]
},
"content": {
# Content of the Specification Figure (Figure Text elements represented as individual paragraphs)
"text": string, # Normalized text of the object: hyphenation is resolved, paragraph spans are joined with space, paragraphs are delimited with NEWLINE character
(\n); table cells are delimited with TAB character (\t) for Table and TableRow content text
"regions": [
# Location of the text on the document's page(s) defined by rectangular regions{
"page": integer, # Number of the document's page, on which the object's region is located; starts from 1
"rect": [X1: number, Y1: number, X2: number, Y2: number] # coordinates of the corner points ((X1,Y1) is top-left corner and (X2,Y2) is bottom-
right corner) of the bounding rectangle around the object's text span in the document, provided as 4 floating numbers in ratio units relative to the
width and height of the page
"angle": OPT number (default: 0) # angle of rotation of the object's bounding rectangle around its center, applied to horizontal text, in degree units
}
]
},
"context": {
# Context of the object in the document structure
"section": {
# Closest parent section of the object
"title": string # Title of the section
}
},
"entities": [
# List of associated named entities extracted from object's text
{
"class": string = "equipment" | "material" | "parameter" | "reference", # Named entity class
"text": string, # Normalized text of the entity extracted from the source text: singular form, standard letter-case
"source": string = "content" | "title", # Source field of the object, from text of which the entity has been extracted
"offsets": [
# Offsets for highlighting of the entity in the source text to be used for highlighting in the text snippet
{
"start": integer, # Start offset of the entity in the source text
"length": integer # Quantity of characters in the source text that belong to the entity; NOTE: entity 'metal' can have offset length 6
corresponding to 'metals' in the text
}
],
"groups": [string] # Categorization groups for building the multi-level entity tree
}
],
"path": [
# Path to the object in the document's content, including titles of sections and tables, to which the object belongs, ordered top to bottom
{
"text": string # Heading or caption of the path object
}
]
}
5 Data Lineage and Purpose
5.1 Text Normalization
All *.text property values shall not contain NEWLINE (\n) characters except when \n is
used as a delimiter between paragraphs.
In *.text property, newline characters inside paragraph (between spans) that come from
DocStruct shall be replaced with space character.
All *.text property values shall not contain TAB (\t) characters except when \t is used as a
delimiter between table cells.
All *.text property values shall have de-hyphenation applied (no hyphens, words
hyphenated in the document are glued).5.2 Source of Title Text
Table-type objects shall have title text formed from TableCaption paragraph when they are
available from DocStruct.
Figure-type objects shall have title text formed from FigureCaption paragraph when they
are available from DocStruct.
Specification Object Source of Object.title.text
Specification Clause N/A
Specification Statement N/A
Specification Table Extracted from TableCaption paragraphs.
Specification Table Row N/A
Specification Figure Extracted from FigureCaption paragraphs.
5.3 Source of Content Text
Specification objects shall have Object.content.text formed according to the following
rules:
Specification Object Source of Object.content.text
Specification Clause Multiple paragraphs shall be delimited with NEWLINE (\n).
Specification Statement Portion (sentence-size) of paragraph from DocStruct (No newline characters)
Specification Table TableCell paragraphs delimited with \t
Table rows delimited with \n
TableInfo paragraphs shall not be part of Specification Table object (instead, they shall be extracted as Clauses).
Specification Table Row TableCell paragraphs delimited with \t
Specification Figure FigureText paragraphs delimited with \n
5.4 Source of Content Regions
Specification Object Source of Object.content.text
Specification Clause Regions corresponding to the spans of the paragraph(s) of the clause.
Specification Statement Regions corresponding to the characters of the statement.
Specification Table Table bounding box region(s) provided by DocStruct SDK
Specification Table Row Regions corresponding to the spans of the paragraphs of table cells of the table row.
Specification Figure Regions corresponding to the spans of the Figure Text paragraphs.
5.5 Source of Entities
TERA entities shall be extracted from Object.title.text for Table and Figure.
TERA entities shall be extracted from Object.content.text for all (Clause, Statement,
Table, Table Row and Figure) objects.
Extracted entities shall be provided with offsets Object.entities.[].offsets and
Object.entities.[].source so that the source text can be highlighted.
When an entity is extracted from Object.title.text, the property
Object.entities.[].source shall have value “title”.When an entity is extracted from Object.title.content, the property
Object.entities.[].source shall have value “content”.
5.6 Object Identities
Objects in this document offer identification via the “id” property that is defined as:
“non-persistent ID of the object. It may or may not be unique in the CINT perimeter.
Consumer of the API must admit it should not be stored in data storages.”
This definition stresses out that neither format nor lifetime of the “id” are defined.
Consumers of the APIs must be aware that values of the “id” do not guarantee their
persistence. “id” can be volatile.
For the “Milestone 1” scope the utility of “id” is to demonstrate to API consumers and users
of UIs based on that APIs, that the specification objects are Entities (i.e. data structures
that have identities).
The reader of this section should be aware that the Architecture Team is working on the
AURN concept in scope of a bigger concept called the “Resource Model”.
This AURN concept will provide the mechanism of expressing globally unique identifiers
that can be persisted.
Until the concept is published, teams should not invent their mechanisms of persistent
identities.
5.7 Object’s Positional Index
The values of ‘index’ property of specification objects shall be unique across the
document.
The values of ‘index’ property of specification objects reflect the relative ordinal position of
the objects inside document: if object A has index value less than index value of object B,
then object A is not positioned after object B in the PDF document text flow.
Since the same text can be a source of multiple objects of different types, the value of their
‘index’ property shall provide a stable order of object types as follows: index of Clause <
index of Statement < index of Table < index of TableRow < index of Figure.
Note: This means, if the same paragraph is a source for a Clause and for a Statement, then
‘index’ of the Clause shall be less than index of ‘Statement’, etc.
The values of ‘index’ property of specification objects can change with the change of the
version of the Decomposition Service.Statement-type specification objects extracted from the same text paragraph, shall be
ordered by their source paragraph number combined with their char offsets inside
paragraph.
TableRow-type specification objects shall be ordered by the minimal source paragraph
number of all rows of the table combined with row number of their cells identified by
DocStruct.
Example:
• Document has paragraphs: P0, P1, P2, P3, P4, P5, P6.
• Clauses were extracted from paragraphs: P0 → C0, P1 → C1, P3 → C2, P4 → C3, P5
→ C4, P6 → C5.
• Statements were extracted from paragraphs: P0 → S0, S1, S2 (ordered by offsets),
P1 → S3, S4
• TableRows were extracted from paragraphs: P5 → R0, P6 → R1.
• Order of the objects:
1. P0 → C0
2. P0 → S0 Statements always go after Clauses extracted from the same text.
3. P0 → S1
4. P0 → S2
5. P1 → C1
6. P1 → S3
7. P1 → S4
8. P3 → C2
9. P4 → C3
10. P5 → C4
11. P5 → R0
12. P5 P6 → R1 Rows are ordered by minimal paragraph of all table rows.
13. P6 → C5
5.8 Object’s Context
Object.context.parents field provides a list of the parents of Specification Clause and
Specification Statement objects in the hierarchical structure of the document. The list of
parents is ordered from top to bottom. The purpose of this field is to provide enrichment
information for better searchability of the specification objects. For example, if the
Specification Statement “The pump must be designed to withstand X psi/bar.” is located in
“4. Rotary Pumps > 4.3. Performance Criteria > 4.3.2. Pressure Design Criteria”, then thewords “rotary”, “pressure”, etc. from the context parents can be added to the statement’s
search index to improve its findability.
Object.context.section field provides the information about the closest parent section of
the document, to which the objects belongs. The title of the section is supposed to be used
in the column “Section” in the table of requirements extracted from a document or
document collection.
6 Objects Representation on UI (Milestone 1)
6.1 Object Snippets in Topics Tree
When a user expands an entity node in the Topics Tree (left panel), the objects of type
Clause, Table and Figure that has this entity in Object.entities field shall be listed in form
of the object snippets with highlighting of the expanded entity.
The highlighted snippet for objects shall be formed from Object.title.text and
Object.content.text for Table and Figure -type objects.
The highlighted snippet for objects shall be formed from Object.content.text for Clause,
Statement and Table Row objects.
The snippets for objects shall be truncated to contain not more that N (TBD) symbols. (The
exact number depends on UI layout and width of frame.)
The truncation of the snippet shall be marked as “...” (in the beginning or/and in the end).
NOTE: As a summary, the snippets for Specification Objects in the Topics Tree shall be
formed according to the following rules:
Specification
Object
Participation of
object’s entities in the
Topics Tree (Milestone
1)
Title Text
Object.title.text
Content Text
Object.content.text
Remarks
Specification
Clause
✓ N/A ✓
Specification
Statement
– – – –
Specification Table ✓ ✓ ✓ Table cells in the snippet
are represented as one
line.
Specification Table
Row
– – – –
Specification Figure ✓ ✓ ✓
6.2 Object Representation on the Document Pages
Specification objects shall be outlined on the document pages in the document viewer
using the Object.*.regions according to the following rules:Specification Object Title Regions
Object.title.regions
Content Regions
Object.content.regions
Specification Clause ✓
Specification Statement ✓
Specification Table ✓ ✓
Specification Table Row ✓
Specification Figure ✓ ✓
6.3 Object Details View
When a user clicks an object in the document, the right panel shall represent object details
with the following data.
Specification
Object
Title Text
Object.title.text
Content Text
Object.content.text
Specification
Object.specification
Entities
Object.entities
Path
Object.path
Remarks
Specification Clause ✓ ✓ ✓
Specification
Statement
✓ ✓ ✓ ✓
Specification Table ✓ ✓ ✓ Assumed that
Table content is
not show on UI on
the right panel, but
only caption, path
and entities.
Specification Table
Row
✓ ✓ ✓ ✓ How to represent
table row text on UI
– TBD. Assumed
simple way: as is
(in one line).
Complex way:
show individual
cells. This will
require to add
more data to
payload or split
Object.content.tex
t by \t.
Specification Figure ✓ ✓ ✓ ✓
6.4 Examples of Objects Representation
The following examples represent schematic illustration of the representation of the
objects in UI using provided data model.
NOTE: The illustrations below do not dictate styling and UI effects. Instead, they provide
understanding of the potential usage of the suggest data model.
6.4.1 Specification Clause View Example
In Document ViewerIn Topics Tree
• Equipment
1. MICROSCOPE
▪ METALLURGICAL MICROSCOPE
• ... transverse cross sections of at least three tubes from the lot shall be polished for
examination with a metallurgical microscope. Using a 100× magnification, the cladding
thickness at four points 90° apart in each sample shall be measured and the average of
the 12 measurements shall be taken ...
6.4.2 Specification Table View Example
In Document Viewer
In Topics Tree
• Equipment
1. BAR
▪ EXTRUDED BAR
• TABLE 3 Ultrasonic Discontinuity Limits for Extruded Bar and ProfilesAAlloy Thickness,B in. Weight, max per Piece, lb Max Width: Thickness Ratio Discontinuity
Class C 2014 2024 } 2219 0.500 and over 600 10:1 B 7075 } 0.500–1.499 1.500 and ...
• Parameters
1. THICKNESS
▪ ALLOY THICKNESS
• TABLE 3 Ultrasonic Discontinuity Limits for Extruded Bar and Profiles A.
Alloy Thickness,B in. Weight, max per Piece, lb Max Width: Thickness Ratio Discontinuity
Class C 2014 2024 } 2219 0.500 and over 600 10:1 B 7075 } 0.500–1.499 1.500 and ...
6.4.3 Specification Figure View Example
In Document Viewer
In Topics Tree
• Equipment
1. VANE
▪ PNEUMATIC QUARTER-TURN VANE
• Figure 1 Hydraulic and pneumatic cylinder and vane-type actuators for valves and slide gates
... Rack and Pinion Sec. 4.4.8 Test for Quarter-Turn Cylinder and Rack and Pinion Sec.
5.2.3 Pneumatic Quarter-Turn Vane Sec. 4.4.9 Manual Gear Override Sec. 4.4.10 Test for
Quarter-Turn Vane Sec. 5.2.4 Test for Manual Gear Override Sec. 5.2.5 ...
7 References
1. Core Terminology – EPD Wiki2. Specs Decomposition Annotation Guidelines – EPD Wiki
3. INCOSE Guide on writing requirements
8 Issues to Resolve
• Issue 567004: Specification object data model: "entities" is a term to confirm with
product management
• Issue 567006: Specification object data model: proposed change for "regions" field to be
analyzed and confirmed