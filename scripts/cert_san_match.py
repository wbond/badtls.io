# coding: utf-8
from __future__ import unicode_literals, division, absolute_import, print_function

from datetime import datetime

from asn1crypto.util import timezone
from certbuilder import CertificateBuilder

from _util import load_public, load_private, load_cert, dump_cert, write


def generate_san_match_cert(domain, base_year, quiet=False):
    if not quiet:
        write('Generating san-match cert ... ', end='')

    ca_private_key = load_private('ca')
    ca_cert = load_cert('ca')
    public_key = load_public('host')

    builder = CertificateBuilder(
        {
            'country_name': 'US',
            'state_or_province_name': 'Massachusetts',
            'locality_name': 'Newbury',
            'organization_name': 'Bad TLS Limited',
            'common_name': 'Bad TLS',
        },
        public_key
    )
    builder.issuer = ca_cert
    builder.subject_alt_domains = ['san-match.{}'.format(domain)]
    builder.begin_date = datetime(base_year, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    builder.end_date = datetime(base_year + 1, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    certificate = builder.build(ca_private_key)

    dump_cert('san-match', certificate)

    if not quiet:
        write('done')
