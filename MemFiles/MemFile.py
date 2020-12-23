from datetime import datetime, timedelta
from io import BytesIO

class MemFile:
    """
    Класс для хранения файлов в памяти
    """
    def __init__(self, file: BytesIO, url, name):
        self.file = file
        self.url = url  # todo: избыточно, это хранится в менеджере
        self.name = name
        self.created_at = datetime.now()
        self.expires_at = self.created_at + timedelta(minutes=1)

    def wipe(self):
        del self.file
        del self.url
        del self.name
        del self.created_at
        del self.expires_at

    @property
    def expired(self) -> bool:
        return datetime.now() >= self.expires_at



