import os

TABLE_HEADERS = """
<table border="1" style="width:100%; border-collapse: collapse;">
    <tr>
        <th>Файл</th>
        <th>Ошибка</th>
        <th>Возможное решение</th>
    </tr>
"""

class HTMLLogger():
    def __init__(self, path_to_log_file):
        self.path_to_log_file = path_to_log_file
        self.create_log_file()

    def create_log_file(self):
        if not os.path.isfile('./path_of_file'):
            file = open(self.path_to_log_file, 'w')
            file.write(TABLE_HEADERS)
            file.close()

    def write(self, message):
        with open(self.path_to_log_file, 'a') as log_file:
            log_file.write(self.format_message(message))

    def format_message(self, message):
        html_message = " <tr><td>{}</td> <td>{}</td> <td>{}</td></tr>".format(message.file_name,
                                                                              message.error_message,
                                                                              message.solution)
        return html_message
