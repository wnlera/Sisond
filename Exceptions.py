
class MyBaseException(Exception):
    msg = "Неизвестная ошибка сервера."
    code = 500


class WrongFormat(MyBaseException):
    msg = "Отправлен файл не с форматом .docx."
    code = 400







