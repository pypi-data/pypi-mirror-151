import os

from metainfo.exception.MetaInfoMissingError import MetaInfoMissingError
from metainfo.exception.PackageFileNotFoundError import PackageFileNotFoundError


class MetaInfo:

    def __init__(self, default_path='.', meta_file='__init__.py'):
        self.meta_file_path = os.path.join(os.getcwd(), default_path, meta_file)
        if not self.meta_file_exists():
            raise PackageFileNotFoundError()

    def meta_file_exists(self):
        return os.path.exists(self.meta_file_path)

    def get_version(self):
        return self.obtain_value_from_meta('version')

    def get_description(self):
        return self.obtain_value_from_meta('description')

    def obtain_value_from_meta(self, key):
        file_lines = self.read_from_meta_file()
        if len(file_lines) == 0:
            raise MetaInfoMissingError(f'Unable to obtain meta info "{key}"')
        value_of_key = [line for line in file_lines if line.find(key) >= 0]
        if len(value_of_key) == 0:
            raise MetaInfoMissingError(f'Unable to obtain meta info "{key}"')
        normalized_value = value_of_key[0].replace('\n', '').replace(f'__{key}__ = ', '').replace('"', '')
        return normalized_value

    def read_from_meta_file(self):
        with open(self.meta_file_path, 'r') as data_file:
            return data_file.readlines()

