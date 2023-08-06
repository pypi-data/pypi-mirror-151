from base64 import standard_b64encode
from textwrap import wrap

__CRC24_INIT__ = 0x0b704ce
__CRC24_POLY__ = 0x1864cfb

def __crc24(data: bytes) -> bytes:
    crc = __CRC24_INIT__

    for b in data:
      crc ^= b << 16

      for i in range(8):
        crc <<= 1
        if crc & 0x1000000:
          crc ^= __CRC24_POLY__

    crc = crc & 0xFFFFFF
    return crc.to_bytes(3, 'big')

def armour(header: str, payload: bytes) -> str:
  encoded = standard_b64encode(payload)
  wrapped = wrap(encoded.decode('utf-8'), 64)

  checksum = standard_b64encode(__crc24(payload)).decode('utf-8')

  wrapped.insert(0, '-----BEGIN PGP %s-----' % (header))
  wrapped.insert(1, 'Version: AwsKmsWrapper v1')
  wrapped.insert(2, '')
  wrapped.append('=%s' % (checksum))
  wrapped.append('-----END PGP %s-----' % (header))
  wrapped.append('') # final newline!

  return ('\n'.join(wrapped)).encode('utf-8')
