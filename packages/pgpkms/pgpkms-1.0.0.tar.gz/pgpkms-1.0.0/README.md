Using AWS KMS keys for PGP
==========================

This library (and command line utlity) allows to use AWS KMS keys (RSA only,
for now) to generate GnuPG / OpenPGP compatible signatures (v4).

* [Preparing keys in KMS](#preparing-keys-in-kms)
* [Command Line Usage](#command-line-usage)
* [Library Usage](#library-usage)
* [Copyright Notice](NOTICE.md)
* [License](LICENSE.md)



Preparing keys in KMS
---------------------

Your mileage might vary (whether you use the AWS console, AWS cli, or tools like
CloudFormation or Terraform) but overall any RSA "signing" key can be used.

By default the _User ID_ associated with the key will be something along the
lines of `AwsPgpWrapper (...uuid...)` where `uuid` is the random UUID associated
with the key in KMS.

In order to properly specify a _User ID_ in the format of `Name <email@domain>`
we can use a couple of _tags_ on the AWS key itself:

* `PGPName`: the `Name` part of the _User ID_.
* `PGPEmail`: the `email@domain` part of the _User ID_.



Command Line Usage
------------------

The [`pgpkms.sh`](./pgpkms.sh) file provides a quick, minimalistic command line
to _export_ the public key, or _sign_ a file:

#### Usage:

`runme.py <command> [options]`

#### Commands:

* `export`: Export the public key.
* `sign`: Sign some data.

#### Options:

* `-k <id>` or `--key <id>`
  The ID of the key to use (defalts to the value of the `PGP_KMS_KEY` environment variable).
  This can be one of:
  * Key ID: e.g. `1234abcd-12ab-34cd-56ef-1234567890ab`
  * Key ARN: e.g. `arn:aws:kms:us-east-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab`
  * Alias name: e.g. `alias/ExampleAlias`
  * Alias ARN: `arn:aws:kms:us-east-2:111122223333:alias/ExampleAlias`

* `-o <file>` or `--output <file>`
  Use the specified file as output instead of stdout.

* `-i <file>` or `--input <file>`
  Use the specified file as input instead of stdin.

* `-b` or `--binary`
  Do not armour the output.

* `--sha256` or `--sha384` or `--sha512`
  Use the specified hashing algorithm (defaults to the value of the `PGP_KMS_HASH` environment variable or `sha256`).

#### Examples

Export the (unarmoured) public key into the "trusted.gpg" file.

```bash
$ main.py export --binary --output trusted.gpg
```

Sign the file "myfile.bin" and emit the armoured signature to stdout.

```bash
$ runme.py sign --input myfile.bin
```



Library Usage
-------------

Simply import the package and look for the `KmsPgpKey` class documentation:

```python
import pgpkms

help(pgpkms.KmsPgpKey)
```

This is summarized as follows:

#### `class KmsPgpKey(key_id, kms_client=None)`

The `KmsPgpKey` class wraps an AWS KMS key and is capable of producing
signatures compatible with GnuPG / OpenPGP.

* `key_id`: The ID of the AWS KMS key. This can be one of the following:
  * Key ID: e.g. `1234abcd-12ab-34cd-56ef-1234567890ab`
  * Key ARN: e.g. `arn:aws:kms:us-east-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab`
  * Alias name: e.g. `alias/ExampleAlias`
  * Alias ARN: `arn:aws:kms:us-east-2:111122223333:alias/ExampleAlias`

* `kms_client`: A BotoCore _KMS_ client, if `None` this will be initialized as:
  ```
  session = botocore.session.get_session()
  kms_client = session.create_client('kms')
  ```

#### `kmsPgpKey.sign(input, hash='sha256', armoured=True, kms_client=None)`

Sign the specified input using this key, and return the signature in a format
compatible with GnuPG / OpenPGP as a `bytes` string.

* `input`: The data to be signed.
* `hash`: The hashing algorithm used to sign the data.
* `armoured`: Whether the returned signature should be armoured (text) or not (binary).
* `kms_client`: A BotoCore _KMS_ client _(optional)_.

This method returns a `bytes` string containing the GnuPG / OpenPGP formatted
signature.

#### `kmsPgpKey.to_pgp(hash='sha256', armoured=True, kms_client=None)`

Return the public key from AWS KMS wrapped in an OpenPGP v4 key format as a
`bytes` string.

* `hash`: The hashing algorithm used to prepare the self-signature of the public key.
* `armoured`: Whether the returned key should be armoured (text) or not (binary).
* `kms_client`: A BotoCore _KMS_ client _(optional)_.
