class ValidationError:
    __slots__ = ["file_name", "extra_data"]

    ERROR_MESSAGE = ''
    SOLUTION = ''

    def __init__(self, file_name, extra_data=None):
        self.file_name = file_name
        self.extra_data = extra_data

    @property
    def error_message(self):
        if self.extra_data:
            return type(self).ERROR_MESSAGE.format(self.extra_data)
        else:
            return type(self).ERROR_MESSAGE

    @property
    def solution(self):
        if self.extra_data:
            return type(self).SOLUTION.format(self.extra_data)
        else:
            return type(self).SOLUTION


class NoData(ValidationError):
    ERROR_MESSAGE = 'Данных в файле не обнаружено'
    SOLUTION = 'Проверьте исправность источника файла'

    def __init__(self, *args):
        super().__init__(*args)


class MissedNecessaryField(ValidationError):
    ERROR_MESSAGE = "Отсутствует обязательноe поле '{}'"
    SOLUTION = "Заполните обязательное поле '{}'"

    def __init__(self, *args):
        super().__init__(*args)


class UnknownEvent(ValidationError):
    ERROR_MESSAGE = "Неизвестный ивент '{}'"
    SOLUTION = "Добавить схему для ивента '{}', либо проверьте значения поля 'event'"

    def __init__(self, *args):
        super().__init__(*args)


class WrongDataType(ValidationError):
    ERROR_MESSAGE = "Неправильный тип данных для поля '{}', обнаружен '{}', но требуется '{}'"
    SOLUTION = 'Проверьте исправность источника файла (неправильное название поля, расположение и т.д.)'

    def __init__(self, *args):
        super().__init__(*args)

    @property
    def error_message(self):
        if self.extra_data:
            return type(self).ERROR_MESSAGE.format(*self.extra_data)
        else:
            return type(self).ERROR_MESSAGE
