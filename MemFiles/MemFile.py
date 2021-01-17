from datetime import datetime, timedelta
from io import BytesIO

class MemFile:
    """
    Класс для хранения файлов в памяти
    """
    def __init__(self, file: BytesIO, url, name):
        self._file = file
        self._file.seek(0)
        # self.file = file
        self.url = url  # todo: избыточно, это хранится в менеджере
        self.name = name
        self.created_at = datetime.now()
        self.expires_at = self.created_at + timedelta(minutes=5)
        # self.expires_at = self.created_at + timedelta(minutes=1)

    def wipe(self):
        del self._file
        del self.url
        del self.name
        del self.created_at

    @property
    def file(self):
        copyfile = BytesIO()
        self.copy_filelike_to_filelike(copyfile)
        copyfile.seek(0)

        assert not copyfile.closed, "IO is closed, which is not expected"

        return copyfile

    def copy_filelike_to_filelike(self, dst, bufsize=16384):
        while True:
            buf = self._file.read(bufsize)
            if not buf:
                break
            dst.write(buf)
        self._file.seek(0)

    @property
    def expired(self) -> bool:
        return datetime.now() >= self.expires_at



