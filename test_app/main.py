from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.kdf.concatkdf import ConcatKDFHash
from cryptography.hazmat.primitives.kdf.concatkdf import ConcatKDFHMAC
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.kdf.hkdf import HKDFExpand
from cryptography.hazmat.primitives.kdf.kbkdf import (
   CounterLocation, KBKDFHMAC, Mode
)
from cryptography.hazmat.primitives.kdf.kbkdf import (
   CounterLocation, KBKDFCMAC
)
from cryptography.hazmat.primitives.kdf.x963kdf import X963KDF
from cryptography.hazmat.primitives import hashes
import os

# GOOD
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=os.urandom(16),
    iterations=480000,
)

# BAD SALT Length
salt = os.urandom(2)
# BAD Key Length
keylen = 4
# BAD Iterations
iterations = 1000
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=keylen,
    salt=salt,
    iterations=iterations,
)

# BAD KDF ALGORITHM
kdf = Scrypt(
    salt=salt,
    length=32,
    n=2**14,
    r=8,
    p=1,
)

# BAD KDF ALGORITHM
sharedinfo = b"ANSI X9.63 Example"
xkdf = X963KDF(
    algorithm=hashes.SHA256(),
    length=32,
    sharedinfo=sharedinfo,
)

# BAD SALT RANDOM SOURCE
salt = b'test'
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=480000,
)

# BAD KEY LENGTH
otherinfo = b"concatkdf-example"
keyLen= 4
ckdf = ConcatKDFHash(
    algorithm=hashes.SHA256(),
    length=keyLen,
    otherinfo=otherinfo,
)

# BAD SALT
salt = b'test'
# BAD KEY LENGTH
keyLen = 1
ckdf = ConcatKDFHMAC(
    algorithm=hashes.SHA256(),
    length=keyLen,
    salt=salt,
    otherinfo=otherinfo,
)

# BAD SALT
salt = b'test'
# BAD KEY LENGTH
keyLen = 1
info = b"hkdf-example"
# BAD KDF ALGORITHM
hkdf = HKDF(
    algorithm=hashes.SHA256(),
    length=keyLen,
    salt=salt,
    info=info,
)

# BAD KEY LENGTH
keyLen = 1
# BAD KDF ALGORITHM
hkdf = HKDFExpand(
    algorithm=hashes.SHA256(),
    length=keyLen,
    info = info)

# BAD Key Length
keyLen = 1
# BAD Mode
# This should be a runtime error, but there is apparently only one mode, the mode we accept.
# This is therefore an artificial case to test we can detect a bad mode if one exists in the future
mode = None 
label = b"KBKDF HMAC Label"
context = b"KBKDF HMAC Context"
kdf = KBKDFHMAC(
    algorithm=hashes.SHA256(),
    mode=mode,
    length=keyLen,
    rlen=4,
    llen=4,
    location=CounterLocation.BeforeFixed,
    label=label,
    context=context,
    fixed=None,
)

# GOOD
kdf = KBKDFHMAC(
    algorithm=hashes.SHA256(),
    mode=Mode.CounterMode,
    length=32,
    rlen=4,
    llen=4,
    location=CounterLocation.BeforeFixed,
    label=label,
    context=context,
    fixed=None,
)

# GOOD 
label = b"KBKDF CMAC Label"
context = b"KBKDF CMAC Context"
kdf = KBKDFCMAC(
    algorithm=algorithms.AES,
    mode=Mode.CounterMode,
    length=32,
    rlen=4,
    llen=4,
    location=CounterLocation.BeforeFixed,
    label=label,
    context=context,
    fixed=None,
)

# BAD Key Length
keyLen = 1
# BAD Mode
# This should be a runtime error, but there is apparently only one mode, the mode we accept.
# This is therefore an artificial case to test we can detect a bad mode if one exists in the future
mode = None 
label = b"KBKDF CMAC Label"
context = b"KBKDF CMAC Context"
kdf = KBKDFCMAC(
    algorithm=algorithms.AES,
    mode=mode,
    length=keyLen,
    rlen=4,
    llen=4,
    location=CounterLocation.BeforeFixed,
    label=label,
    context=context,
    fixed=None,
)
