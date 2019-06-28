# badtls.io

A server that serves up various bad (and good) TLS certificates and
configurations for the sake of testing.

 - [Domains](#domains)
 - [Running Locally](#running-locally)
 - [Installing](#installing)
 - [Generating New Certificates](#generating-new-certificates)

## Domains

Various "good" configurations:

 - [domain-match.badtls.io:10000](https://domain-match.badtls.io:10000)
 - [wildcard-match.badtls.io:10001](https://wildcard-match.badtls.io:10001)
 - [san-match.badtls.io:10002](https://san-match.badtls.io:10002)
 - [required-auth.badtls.io:10003](https://required-auth.badtls.io:10003)
 - [optional-auth.badtls.io:10004](https://optional-auth.badtls.io:10004)
 - [dh1024.badtls.io:10005](https://dh1024.badtls.io:10005)
 - [no-san.badtls.io:10006](https://no-san.badtls.io:10006)

Various "bad" configurations:

 - [expired-1963.badtls.io:11000](https://expired-1963.badtls.io:11000)
 - [future.badtls.io:11001](https://future.badtls.io:11001)
 - [domain-mismatch.badtls.io:11002](https://domain-mismatch.badtls.io:11002)
 - [san-mismatch.badtls.io:11003](https://san-mismatch.badtls.io:11003)
 - [weak-sig.badtls.io:11004](https://weak-sig.badtls.io:11004)
 - [bad-key-usage.badtls.io:11005](https://bad-key-usage.badtls.io:11005)
 - [expired.badtls.io:11006](https://expired.badtls.io:11006)
 - [wildcard.mismatch.badtls.io:11007](https://wildcard.mismatch.badtls.io:11007)
 - [rc4.badtls.io:11008](https://rc4.badtls.io:11008)
 - [rc4-md5.badtls.io:11009](https://rc4-md5.badtls.io:11009)

## CA Certificate

In order to properly test TLS connections, the CA certificate used for the
various domains will need to be added to the trust store/list used by the
code or application being tested.

The CA certificate is located at [certs/ca.crt](certs/ca.crt).

## Running Locally

To use the certificates for testing, `nginx` and `socat` must be installed. All
of the domains run on non-privileged ports for ease-of-use.

To start nginx and socat, execute:

```bash
bash ./scripts/local.sh
```

## Installing

To install the nginx configuration, web files and certificates on a server,
invoke the following command:

```bash
python scripts/install.py {nginx_conf_dir} {nginx_ssl_dir} {wwwroot_dir}
```

 - `{nginx_conf_dir}` should be a folder to copy the `badtls.conf` file into
 - `{nginx_ssl_dir}` should be a folder in which to create a subfolder named
   `badtls_certs`, which will contain all certificates, keys and related
   files
 - `{wwwroot_dir}` should be a folder in which to create a subfolder named
   `badtls_wwwroot` which will contain the webfiles

The values provided will be used to customize the `badtls.conf` file. All that
is necessary will be to add an `include` directive into the main `nginx.conf`:

```
http {
    ...

    include  relative/path/to/badtls.conf;
}
```

By default, the install script will not overwrite existing files/directories.
To have existing files and folders replaced, add the `overwrite` parameter to
the arguments:

```bash
python scripts/install.py overwite {nginx_conf_dir} {nginx_ssl_dir} {wwwroot_dir}
```

Additionally, socat will need to be configured to run on port 10003 using
the configuration from [scripts/local.sh](scripts/local.sh). This allows proper
testing of a host requiring client certificates. Unfortunately nginx does not
allow requiring certificates at the TLS protocol level.

## Generating New Certificates

New certificates and keys can be generated if you wish to run your own instance
of the domains.

### Dependencies

Python 2.6, 2.7 or 3.2+ with the following packages:

 - [asn1crypto](https://github.com/wbond/asn1crypto)
 - [oscrypto](https://github.com/wbond/oscrypto)
 - [certbuilder](https://github.com/wbond/certbuilder)
 - [crlbuilder](https://github.com/wbond/crlbuilder)

The simplest way to install them is:

```bash
pip install certbuilder crlbuilder
```

### Commands

To generate all keys and certificates, execute the following, replacing
`{domain}` with the domain name you with to use:

```bash
python scripts/generate.py {domain}
```

If only domain certs need to be regenerated, use:

```bash
python scripts/generate.py --regen-certs {domain}
```
