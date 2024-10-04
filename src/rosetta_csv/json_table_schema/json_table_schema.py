"""JSON Table Schema

json-table-schema, an implementation of the JSON Table Schema format,
by Martin Keegan

Original: https://github.com/mk270/json-table-schema-python
(Copyright (C) 2013  Martin Keegan)

Latest, provides partial support for 1.0-pre3.1
Copyright (C) 2014  Ross Spencer

More info: http://www.dataprotocols.org/en/latest/json-table-schema.html

This programme is free software; you may redistribute and/or modify
it under the terms of the Apache Software Licence v2.0
"""

# pylint: disable=C0116, C0115

import json
import sys

try:
    import csvdatatypes
except ModuleNotFoundError:
    try:
        from src.rosetta_csv.json_table_schema import csvdatatypes
    except ModuleNotFoundError:
        from rosetta_csv.json_table_schema import csvdatatypes


class FormatError(Exception):
    pass


class DuplicateFieldName(Exception):
    pass


class NotJSONError(Exception):
    pass


class JSONTableSchema:
    __format_version__ = "1.0-pre3.1-partial-implementation"

    required_field_descriptor_keys = ["name"]
    optional_field_descriptor_keys_strings = ["title", "type", "description"]
    optional_field_descriptor_keys_lists = ["constraints"]
    optional_field_descriptor_keys_patterns = ["format"]
    optional_constraints_keys = [
        "required",
        "minLength",
        "maxLength",
        "unique",
        "pattern",
        "minimum",
        "maximum",
    ]

    def __init__(self, json_string=None):
        # Initialise JSONTableSchema object, optionally from a JSON string

        self.fields = []
        self.format_version = self.__format_version__

        if json_string is not None:
            try:
                self.read_json(json.loads(json_string))
            except ValueError:
                sys.stderr.write(
                    "Invalid JSON object the likely cause. Please check and try again."
                )

    def read_json(self, json_string):
        if "fields" not in json_string:
            raise FormatError(
                "JSON array `fields' must be present JSON Table Schema hash."
            )

        field_list = json_string["fields"]
        if not isinstance(field_list, list):
            raise FormatError("JSON key `fields' must be array")

        for idx, stanza in enumerate(field_list):
            if not isinstance(stanza, dict):
                err_str = f"Field descriptor {idx} must be a dictionary"
                raise FormatError(err_str)

            for key in self.required_field_descriptor_keys:
                if key not in stanza:
                    err_tmpl = f"Field descriptor {idx} must contain key `{key}'"
                    raise FormatError(err_tmpl)

            for key in stanza:
                if (
                    key not in self.required_field_descriptor_keys
                    and key not in self.optional_field_descriptor_keys_strings
                    and key not in self.optional_field_descriptor_keys_lists
                    and key not in self.optional_field_descriptor_keys_patterns
                ):
                    err_tmpl = f"Field descriptor {idx} shouldn't contain key `{key}'"
                    raise FormatError(err_tmpl)

            self.add_field(stanza)
            self.format_version = json_string.get(
                "json_table_schema_version", self.__format_version__
            )

    @property
    def field_names(self):
        return [i["name"] for i in self.fields]

    def add_field(self, field):
        field_dict = {}

        for key in self.required_field_descriptor_keys:
            if not isinstance(field[key], (str,)):
                raise FormatError("Field `name' must be a string")
            if field["name"] in self.field_names:
                raise DuplicateFieldName("field 'name'")
            field_dict[key] = field[key]

        for key in self.optional_field_descriptor_keys_strings:
            if key in field:
                if not isinstance(field[key], (str,)):
                    raise FormatError("Field `name' must be a string")

                if key == "type":
                    self.check_type(field["type"], field["name"])

                field_dict[key] = field[key]

        self.fields.append(field_dict)

    def remove_field(self, field_name):
        if field_name not in self.field_names:
            raise KeyError
        self.fields = filter(lambda i: i["name"] != field_name, self.fields)

    def as_json(self):
        return json.dumps(self.as_dict(), indent=2)

    def as_dict(self):
        return {"json_table_schema_version": self.format_version, "fields": self.fields}

    def as_csv_header(self):
        """Concatenate field names into a single CSV header."""
        joined = '","'.join(self.field_names)
        csv_header = f'"{joined}"'
        return csv_header.strip()

    def check_type(self, field_type, field_name):
        type_found = False
        for field_category in csvdatatypes.__valid_type_names__:
            for type_ in field_category:
                if field_type == type_:
                    type_found = True
                    break

        if type_found is not True:
            err_tmpl = (
                f"Invalid type `{field_type}' in field descriptor for `{field_name}'"
            )
            raise FormatError(err_tmpl)
