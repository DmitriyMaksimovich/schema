import os
import sys
from json_reader import JSONReader
from html_logger import HTMLLogger
from schema import Schema


class JSONValidator():
    def __init__(self, data_directory, schema_directory, logger, reader=JSONReader()):
        self.data_directory = data_directory
        self.schemes = Schema.load_schemes(schema_directory)
        self.logger = logger
        self.reader = reader

    def write_to_log(self, message):
        self.logger.write(message)

    def save_validation_errors_in_log(self, errors):
        for error in errors:
            if error:
                self.logger.write(error)

    def validate_data(self):
        for data in self.reader.json_data_from_folder(self.data_directory):
            schema = Schema()
            data_error = schema.validate_data(data)
            if data_error:
                self.logger.write(data_error)
                continue
            schema_error = schema.validate_events(data, self.schemes)
            if schema_error:
                self.logger.write(schema_error)
                continue
            else:
                schema.set_schema(self.schemes[data.data['event']])
            errors = []
            errors.extend(schema.validate_required_fields(data))
            errors.extend(schema.validate_fields_types(data))
            self.save_validation_errors_in_log(errors)


if __name__ == '__main__':
    try:
        json_data_folder = sys.argv[1]
        json_schema_folder = sys.argv[2]
    except IndexError:
        json_data_folder = os.getcwd() + '/task_folder/event'
        json_schema_folder = os.getcwd() + '/task_folder/schema'
    log_file = os.getcwd() + "/log.html"
    validator = JSONValidator(json_data_folder, json_schema_folder, HTMLLogger(log_file))
    validator.validate_data()
