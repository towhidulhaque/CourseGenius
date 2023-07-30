# flake8: noqa WPS115
from types import MappingProxyType


class Constant(object):
    """Class for organizing constants."""

    demo_single_const = 'const'

    demo_constant = MappingProxyType(
        dict(
            constant_a='constant_a',
            constant_b='constant_b'
        )
    )
