from datetime import datetime
from functools import partial
from functools import wraps
from os import path
import hashlib


def upload_hash_file(
        instance_file_field, file_root, with_timestamp=True, block_size=65536
):
    """Функция для формирования upload_at с использованием MD5."""
    @wraps(upload_hash_file)
    def upload_hash_file_decorator(instance, filename):
        """Получить путь к файлу."""
        hasher = hashlib.md5()
        _, file_ext = path.splitext(filename)
        file = getattr(instance, instance_file_field)

        hasher.update(str(filename).encode("utf-8"))

        file.seek(0)
        for buf in iter(partial(file.read, block_size), b''):
            hasher.update(buf)

        if with_timestamp:
            hasher.update(str(datetime.now()).encode('utf-8'))

        return path.join(
            file_root,
            f'{hasher.hexdigest()}{file_ext}'
        )
    return upload_hash_file_decorator
