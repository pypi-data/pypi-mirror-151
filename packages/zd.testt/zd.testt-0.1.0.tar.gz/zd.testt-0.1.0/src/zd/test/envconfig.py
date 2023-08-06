
import os
import logging


logger = logging.getLogger(__name__)


class EnvironmentVar(object):
    def __init__(self, name, required=False, default=None, convert=lambda s: s, get_environment_var=os.environ.get):
        self.name = name
        self.required = required
        self.default = default
        self.convert = convert
        self.get_environment_var = get_environment_var

    def get(self):
        env_var = self.get_environment_var(self.name)
        if self.required:
            assert env_var is not None, '{} {} must be set and not None'.format(self.__class__.__name__, self.name)

        return self.convert(env_var) if env_var is not None else self.default


class EnvironmentVarManager(object):
    def __init__(self, **kwargs):
        self._keys = list(kwargs.keys())

        get_val = lambda v: (v if isinstance(v, EnvironmentVar) else EnvironmentVar(**v)).get()

        try:
            self.__dict__.update(**{k: get_val(v) for k, v in kwargs.items()})
        except AssertionError as e:
            logger.error('Error on environment variable configuration update: ' + str(e))
            raise e

    def to_dict(self):
        return {k: getattr(self, k) for k in self._keys}
