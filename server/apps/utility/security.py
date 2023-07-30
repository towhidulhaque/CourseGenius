# flake8: noqa WPS202
import base64
import random
import string
import uuid
from calendar import timegm
from hashlib import md5
from time import gmtime, strftime, strptime, time
from typing import Any, Tuple

from Crypto.Cipher import AES  # noqa: S413
from openid import cryptutil

NONCE_CHARS = string.ascii_letters + string.digits

# Keep nonces for five hours (allow five hours for the combination of
# request time and clock skew). This is probably way more than is
# necessary, but there is not much overhead in storing nonces.
SKEW = 15

time_fmt = '%Y-%m-%dT%H:%M:%SZ'  # noqa: WPS323
time_str_len = len('0000-00-00T00:00:00Z')

BLOCK_SIZE = 16  # Bytes


def pad(raw_data) -> bytes:
    """Pad the given bytes to make 16 byte."""
    character = BLOCK_SIZE - len(raw_data) % BLOCK_SIZE
    times = BLOCK_SIZE - len(raw_data) % BLOCK_SIZE
    return raw_data + times * chr(character)


def unpad(raw_data) -> bytes:
    """Unpad the given bytes."""
    return raw_data[:-ord(
        raw_data[len(raw_data) - 1:],
    )]


def encrypt(key, plaintext) -> str:
    """Encrypt a string using AES."""
    key = md5(key.encode('utf8')).hexdigest()  # noqa: S303
    plaintext = pad(plaintext)
    cipher = AES.new(key.encode('utf8'), AES.MODE_ECB)
    # urlsafe is used for encoding complex which will be used in query param
    encoded_byte = base64.urlsafe_b64encode(cipher.encrypt(plaintext.encode('utf8')))
    # covert byte into string
    return encoded_byte.decode('utf8')


def decrypt(key, ciphertext) -> str:
    """Decrypt a string using AES."""
    key = md5(key.encode('utf8')).hexdigest()  # noqa: S303
    enc = base64.urlsafe_b64decode(ciphertext.encode('utf8'))
    cipher = AES.new(key.encode('utf8'), AES.MODE_ECB)
    return unpad(cipher.decrypt(enc)).decode('utf8')


def split(nonce_string) -> Tuple[int, str]:
    """Extract a timestamp from the given nonce string."""
    timestamp_str = nonce_string[:time_str_len]
    try:
        timestamp = timegm(strptime(timestamp_str, time_fmt))
    except AssertionError:  # Python 2.2
        timestamp = -1
    if timestamp < 0:
        raise ValueError('time out of range')
    return timestamp, nonce_string[time_str_len:]


def validate_nonce(nonce_string, allowed_skew=SKEW, now=None) -> bool:
    """Check the timestamp that is part of the specified nonce string."""
    try:
        stamp, _ = split(nonce_string)
    except ValueError:
        return False
    else:
        if now is None:
            now = time()

        past = now - allowed_skew
        future = now + allowed_skew
        return past <= stamp <= future


def create_nonce(when=None) -> str:
    """Generate a nonce with the current timestamp."""
    salt = cryptutil.randomString(6, NONCE_CHARS)
    if when is None:
        gmt_time = gmtime()
    else:
        gmt_time = gmtime(when)

    time_str = strftime(time_fmt, gmt_time)
    return time_str + salt


def generate_random_number(size=4, chars=string.digits) -> str:
    """Random number generator method."""
    return ''.join(random.choice(chars) for _ in range(size))  # NOQA S311


def generate_random_code() -> str:
    """Random code generator method."""
    length_four = 4
    length_eight = 4
    length_twelve = 4
    return '{0}-{1}-{2}-{3}-{4}'.format(
        uuid.uuid4().hex[:length_eight],
        uuid.uuid4().hex[:length_four],
        uuid.uuid4().hex[:length_four],
        uuid.uuid4().hex[:length_four],
        uuid.uuid4().hex[:length_twelve],
    )
