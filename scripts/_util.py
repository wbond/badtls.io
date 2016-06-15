# coding: utf-8
from __future__ import unicode_literals, division, absolute_import, print_function

import sys
from os import path

from oscrypto import asymmetric
from crlbuilder import pem_armor_crl


certs_dir = path.join(path.dirname(__file__), '..', 'certs')


def write(text, end='\n'):
    print(text, end=end)
    sys.stdout.flush()


def get_arg(num):
    if num > len(sys.argv) - 1:
        return None
    value = sys.argv[num]
    if sys.version_info < (3,):
        value = value.decode('utf-8')
    return value


def generate_pair(name, quiet=False, key_type='rsa', key_size=2048):

    if not quiet:
        write('Generating {} keys ... '.format(name), end='')

    public_key, private_key = asymmetric.generate_pair(key_type, bit_size=key_size)

    with open(path.join(certs_dir, '{}.key'.format(name)), 'wb') as f:
        f.write(asymmetric.dump_private_key(private_key, None))

    with open(path.join(certs_dir, '{}.pubkey'.format(name)), 'wb') as f:
        f.write(asymmetric.dump_public_key(public_key))

    if not quiet:
        write('done')


def generate_dh_params(name, quiet=False, size=2048):

    if not quiet:
        write('Generating DH params, this could take a few minutes ... ', end='')

    dh_params = asymmetric.generate_dh_parameters(size)

    with open(path.join(certs_dir, '{}.pem'.format(name)), 'wb') as f:
        f.write(asymmetric.dump_dh_parameters(dh_params))

    if not quiet:
        write('done')


def load_public(name):
    return asymmetric.load_public_key(path.join(
        certs_dir,
        '{}.pubkey'.format(name)
    ))


def load_private(name):
    return asymmetric.load_private_key(path.join(
        certs_dir,
        '{}.key'.format(name)
    ))


def load_cert(name):
    return asymmetric.load_certificate(path.join(
        certs_dir,
        '{}.crt'.format(name)
    ))


def dump_cert(name, certificate):
    with open(path.join(certs_dir, '{}.crt'.format(name)), 'wb') as f:
        f.write(asymmetric.dump_certificate(certificate))


def dump_crl(name, certificate_list):
    with open(path.join(certs_dir, '{}.crl'.format(name)), 'wb') as f:
        f.write(pem_armor_crl(certificate_list))
