"""CSVDataTypes for JSON Table Schema.

json-table-schema, an implementation of the JSON Table Schema format,
by Martin Keegan

Valid data types.

Original: https://github.com/mk270/json-table-schema-python
(Copyright (C) 2013  Martin Keegan)

Latest, provides partial support for 1.0-pre3.1
Copyright (C) 2014  Ross Spencer

More info: http://www.dataprotocols.org/en/latest/json-table-schema.html

This programme is free software; you may redistribute and/or modify
it under the terms of the Apache Software Licence v2.0

NB: Check validity of URIs for certain types...
NB: Check validity of non URI strings...
"""

# pylint: disable=C0301

__valid_type_names__ = [
    [
        "string",
        "http://www.w3.org/2001/XMLSchema#string",
    ],  # a string (of arbitrary length)
    [
        "number",
        "http://www.w3.org/2001/XMLSchema#float",
    ],  # a number including floating point numbers
    [
        "integer",
        "http://www.w3.org/2001/XMLSchema#int",
        "http://www.w3.org/2001/XMLSchema#nonNegativeInteger",
    ],  # an integer
    ["date"],  # a date. This MUST be in ISO6801 format YYYY-MM-DD or, if not,
    # a format field must describe the structure
    ["time"],  # a time without a date
    [
        "date-time",
        "http://www.w3.org/2001/XMLSchema#dateTime",
    ],  # a date-time. This MUST be in ISO8601 format of YYYY-MM-DDThh:mm:ssZ
    # in UTC time or, if not, a format field must be provided
    [
        "boolean",
        "http://www.w3.org/2001/XMLSchema#boolean",
    ],  # a boolean value (1/0, true/false)
    ["binary"],  # base64 representation of binary data
    [
        "object",
        "http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/mapping-object-type.html",
    ],  # (alias json) a JSON-encoded object
    [
        "geopoint",
        "http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/mapping-geo-point-type.html",
    ],  # has one of the following structures
    ["geojson"],  # as per <<http://http://geojson.org/>>
    [
        "array",
        "http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/mapping-array-type.html",
    ],  # an array
    [
        "any",
        "http://www.w3.org/2001/XMLSchema#anyURI",
    ],  # value of field may be any type
]
