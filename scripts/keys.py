# coding: utf-8
from __future__ import unicode_literals, division, absolute_import, print_function

from _util import generate_pair


def generate_ca_keys(quiet=False):
    generate_pair('ca', quiet=quiet)


def generate_ca2_keys(quiet=False):
    generate_pair('ca2', quiet=quiet)


def generate_client_keys(quiet=False):
    generate_pair('client', quiet=quiet)


def generate_host_keys(quiet=False):
    generate_pair('host', quiet=quiet)
