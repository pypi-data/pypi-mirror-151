import os
import sys

from botocore import session as aws
from getopt import getopt, GetoptError
from inspect import cleandoc

from .pgpkms import KmsPgpKey

def __help():
  sys.exit(cleandoc('''\
    Usage:

      {cmd} <command> [options]

    Commands:

      export  Export the public key.
      sign    Sign some data.

    Options:

      -k <id> | --key <id>
        The ID of the key to use (defalts to the value of the
        PGP_KMS_KEY environment variable).

        This can be one of:

          Key ID: e.g. "1234abcd-12ab-34cd-56ef-1234567890ab"
          Key ARN: e.g. "arn:aws:kms:us-east-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab"
          Alias name: e.g. "alias/ExampleAlias"
          Alias ARN: "arn:aws:kms:us-east-2:111122223333:alias/ExampleAlias"

      -o <file> | --output <file>
        Use the specified file as output instead of stdout.

      -i <file> | --input <file>
        Use the specified file as input instead of stdin.

      -b | --binary
        Do not armour the output.

      --sha256 | --sha384 | --sha512
        Use the specified hashing algorithm (defaults to the
        value of the PGP_KMS_HASH environment variable or "sha256").

    Examples

      {cmd} export --binary --output trusted.gpg
        Export the (unarmoured) public key into the "trusted.gpg" file.

      {cmd} sign --input myfile.bin
        Sign the file "myfile.bin" and emit the armoured signature to stdout.

  '''.format(cmd = os.getenv('PGP_KMS_ARGV0', sys.argv[0]))) + '\n')

# ==============================================================================

def __export(key, hash, input = None, output = None, armoured = True):
  session = aws.get_session()
  kms_client = session.create_client('kms')

  key = KmsPgpKey(key, kms_client = kms_client)

  pgp_key = key.to_pgp(armoured = armoured, hash = hash, kms_client = kms_client)

  o = open(output, 'wb') if output else sys.stdout.buffer
  o.write(pgp_key)
  o.close()

  sys.exit(0)

# ==============================================================================

def __sign(key, hash, input = None, output = None, armoured = True):
  session = aws.get_session()
  kms_client = session.create_client('kms')

  key = KmsPgpKey(key, kms_client = kms_client)

  i = open(input, 'rb') if input else sys.stdin.buffer

  signature = key.sign(i, armoured = armoured, hash = hash, kms_client = kms_client)

  o = open(output, 'wb') if output else sys.stdout.buffer
  o.write(signature)
  o.close()

  sys.exit(0)

# ==============================================================================

if __name__ == '__main__':
  if len(sys.argv) < 2:
    __help()

  command = sys.argv[1]

  if not(command in [ 'help', 'export', 'sign' ]):
    sys.exit('Error: command "%s" unknown' % (command))
  elif command == 'help':
    __help()

  key = os.environ.get('PGP_KMS_KEY')
  hash = os.environ.get('PGP_KMS_HASH', 'sha256')
  input = None
  output = None
  armoured = True

  try:
    (options, rest) = getopt(sys.argv[2:], 'k:o:i:b', [
      'key=', 'output=', 'input=', 'binary',
      'sha256', 'sha384', 'sha512',
    ])

    if len(rest) > 0:
      sys.exit('Error: unknown option "%s"' % (rest[0]))

    for key, value in options:
      if key in [ '-b', '--binary' ]:
        armoured = False
      elif key in [ '-i', '--input' ]:
        input = value
      elif key in [ '-o' , '--output' ]:
        output = value
      elif key in [ '--sha256', '--sha384', '--sha512' ]:
        hash = key[2:]

  except GetoptError as error:
    sys.exit('Error: %s' % (error))

  if key == None:
    sys.exit('Error: no key ID specified')

  if not(hash in [ 'sha256', 'sha384', 'sha512' ]):
    sys.exit('Error: invalid hashing algorithm "%s"' % (hash))

  { 'export': __export, 'sign': __sign }[command](
    key = key,
    hash = hash,
    input = input,
    output = output,
    armoured = armoured
  )
