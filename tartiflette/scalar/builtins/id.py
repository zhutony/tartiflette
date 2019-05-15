from tartiflette import Scalar

from .string import ScalarString


class ScalarId(ScalarString):
    pass


def bake(schema_name, config):
    sdl = "scalar ID"

    Scalar(name="ID", schema_name=schema_name)(ScalarId(config))

    return sdl
