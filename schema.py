import os
import json
from json_reader import JSONData
from validation_errors import (NoData, MissedNecessaryField, UnknownEvent,
                               WrongDataType)


TYPES_CONVERTED = {
    'string': str,
    'object': dict,
    'integer': int,
    'number': [float, int],
    'array': list,
    'null': type(None),
    'boolean': bool,
    str: 'string',
    dict: 'object',
    int: 'integer',
    list: 'array',
}


class Schema():
    def __init__(self, schema_json=None, path_to_parent_field='data'):
        self.schema_json = schema_json
        self.path_to_field_parent = path_to_parent_field

    @staticmethod
    def load_schemes(path_to_folder):
        schemes = {}
        with os.scandir(path_to_folder) as entries:
            for entry in entries:
                if entry.name.endswith('schema') and "#" not in entry.name:  # Не забыть бы удалить #
                    with open(entry.path) as json_file:
                        schema_json = json.load(json_file)
                    schemes[entry.name.split('.')[0]] = schema_json
        return schemes

    def set_schema(self, schema):
        self.schema_json = schema

    def path_to_field(self, field_name):
        return '.'.join([self.path_to_field_parent, field_name])

    def validate_data(self, data):
        if not data.data or not data.data.get('data'):
            return NoData(data.file_name)
        return False

    def validate_events(self, data, schemes):
        schema_event = data.data.get('event')
        if not schema_event:
            return MissedNecessaryField(data.file_name, 'event')
        if not schemes.get(schema_event):
            return UnknownEvent(data.file_name, schema_event)
        return False

    def validate_required_fields(self, data):
        errors = []
        layer_data = self.get_layer_data(data)
        data_keys = layer_data.keys()
        for field in self.required_fieds:
            if field not in data_keys:
                path_to_field = self.path_to_field(field)
                errors.append(MissedNecessaryField(data.file_name, path_to_field))
        return errors

    def validate_fields_types(self, data):
        errors = []
        layer_data = self.get_layer_data(data)
        data_keys = layer_data.keys()
        for field in self.typed_fields:
            if field not in data_keys:
                continue
            else:
                field_value = layer_data.get(field)
                errors.extend(self.validate_field_type(field, field_value, data))
        return errors

    def validate_field_type(self, field_name, field_value, data):
        errors = []
        required_types = self.field_types(field_name)
        converted_types = self.convert_types(required_types)
        actual_type = type(field_value)
        if actual_type not in converted_types:
            return [WrongDataType(data.file_name, [self.path_to_field(field_name),
                                                  TYPES_CONVERTED.get(actual_type),
                                                  required_types])]
        if actual_type == list:
            field_value = [{}] if not field_value else field_value
            for value in field_value:
                errors.extend(self.check_field_recursively(field_name, value, data))
            return errors
        return []

    def check_field_recursively(self, field_name, field_value, data):
        errors = []
        schema = Schema(self.schema_json['properties'][field_name]['items'],
                        self.path_to_field(field_name))
        inner_data = JSONData(data.file_name, field_value)
        errors.extend(schema.validate_required_fields(inner_data))
        errors.extend(schema.validate_fields_types(inner_data))
        return errors

    def get_layer_data(self, data):
        layer_data = data.data.get('data')
        if layer_data:
            return layer_data
        else:
            return data.data

    def field_types(self, field_name):
        requred = self.schema_json.get('properties').get(field_name).get('type')
        if type(requred) == list:
            return requred
        else:
            return [requred]

    def convert_types(self, required_types):
        converted = []
        for t in required_types:
            conv = TYPES_CONVERTED.get(t)
            if type(conv) == list:
                converted.extend(conv)
            else:
                converted.append(conv)
        return converted

    @property
    def required_fieds(self):
        return self.schema_json.get('required')

    @property
    def typed_fields(self):
        return self.schema_json.get('properties').keys()
