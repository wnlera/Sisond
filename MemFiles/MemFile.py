from datetime import datetime, timedelta
from io import BytesIO

class MemFile:
    """
    Класс для хранения файлов в памяти
    """
    def __init__(self, file: BytesIO, url, name):
        self._file = file
        self.url = url  # todo: избыточно, это хранится в менеджере
        self.name = name
        self.created_at = datetime.now()
        self.expires_at = self.created_at + timedelta(minutes=5)

    def wipe(self):
        del self.file
        del self.url
        del self.name
        del self.created_at

    @property
    def file(self):
        copyfile = BytesIO()
        self.copy_filelike_to_filelike(copyfile)
        return copyfile

    def copy_filelike_to_filelike(self, dst, bufsize=16384):
        while True:
            buf = self._file.read(bufsize)
            if not buf:
                break
            dst.write(buf)

    @property
    def expired(self) -> bool:
        return datetime.now() >= self.expires_at



