import os


class EnvVarBackend:
    """Backend that reads settings in environment variables."""

    def __init__(self, name_prefix=''):
        self.name_prefix = ''

    def get_setting(self, key):
        key = self.name_prefix + key
        return os.environ.get(key)
