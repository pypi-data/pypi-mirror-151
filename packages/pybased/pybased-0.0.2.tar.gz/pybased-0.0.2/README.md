# pybased

Library for creating arbitrary binary encodings.  Includes variations on base32, base64, base85, and more.

**WARNING:** Although these encodings *do* work end-to-end, they are not compatible with traditional implementations!

I am working on finding out why.

## Encodings

### Types

 * **Sliding:** Random-access bitwise implementation, theoretically compatible with bytestrings of arbitrary size.
 * **BigInt:** Converts bytes into large integers, then incrementally divides by the radix. Incompatible with large files. Suitable for hashes and shorter bytestrings.
 * **Biterator:** Iterates through each byte from the input stream and adds it to a buffer, then extracts the required number of bits to convert to the other radix. Based roughly off of CPython's base64 encoder, but heavily modified to enable arbitrary conversions. **WIP.**

### Available Encodings

<table><thead><caption>Supported Encodings</caption><tr><th>ID</th><th>Type</th><th>Bits/Char</th><th>Chars/Byte</th><th>Alphabet</th></tr></thead><tbody><tr><th>base32</th><td>Biterator</td><td>5</td><td>5</td><td><code>ABCDEFGHIJKLMNOPQRSTUVWXYZ234567</code></td></tr><tr><th>base32hex</th><td>Biterator</td><td>5</td><td>5</td><td><code>0123456789ABCDEFGHIJKLMNOPQRSTUV</code></td></tr><tr><th>base46</th><td>BigInt</td><td>N/A</td><td>N/A</td><td><code>ABCDEFGHJKMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz</code></td></tr><tr><th>base62</th><td>BigInt</td><td>N/A</td><td>N/A</td><td><code>0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz</code></td></tr><tr><th>base64</th><td>Biterator</td><td>6</td><td>3</td><td><code>ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/</code></td></tr><tr><th>base64b64</th><td>Biterator</td><td>6</td><td>3</td><td><code>./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz</code></td></tr><tr><th>base64bash</th><td>Biterator</td><td>6</td><td>3</td><td><code>0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ@_</code></td></tr><tr><th>base64bcrypt</th><td>Biterator</td><td>6</td><td>3</td><td><code>./ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789</code></td></tr><tr><th>base64hqx</th><td>Biterator</td><td>6</td><td>3</td><td><code>!&quot;#$%&amp;&#x27;()*+,-012345689@ABCDEFGHIJKLMNPQRSTUVXYZ[`abcdefhijklmpqr</code></td></tr><tr><th>base64url</th><td>Biterator</td><td>6</td><td>3</td><td><code>ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_</code></td></tr><tr><th>base64uu</th><td>Biterator</td><td>6</td><td>3</td><td><code> !&quot;#$%&amp;&#x27;()*+,-./0123456789:;&lt;=&gt;?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_</code></td></tr><tr><th>base64xx</th><td>Biterator</td><td>6</td><td>3</td><td><code>+-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz</code></td></tr><tr><th>base85</th><td>Biterator</td><td>7</td><td>7</td><td><code>ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!#$%&amp;()*+-;&lt;=&gt;?@^_`{|}~</code></td></tr><tr><th>base94</th><td>BigInt</td><td>N/A</td><td>N/A</td><td><code>!&quot;#$%&amp;&#x27;()*+,-./0123456789:;&lt;=&gt;?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~</code></td></tr><tr><th>crockford32</th><td>Biterator</td><td>5</td><td>5</td><td><code>0123456789ABCDEFGHJKMNPQRSTVWXYZ</code></td></tr><tr><th>geohash32</th><td>Biterator</td><td>5</td><td>5</td><td><code>0123456789bcdefghjkmnpqrstuvwxyz</code></td></tr><tr><th>nintendo32</th><td>Biterator</td><td>5</td><td>5</td><td><code>0123456789BCDFGHJKLMNPQRSTVWXYZ?</code></td></tr><tr><th>wordsafe32</th><td>Biterator</td><td>5</td><td>5</td><td><code>23456789CFGHJMPQRVWXcfghjmpqrvwx</code></td></tr><tr><th>zbase32</th><td>Biterator</td><td>5</td><td>5</td><td><code>ybndrfg8ejkmcpqxot1uwisza345h769</code></td></tr></tbody></table>


### Status

<table><thead><caption>Supported Encodings</caption><tr><th>Standard</th><th>Encoded</th><th>Decoded</th><th>Passed Test</th></tr></thead><tbody><tr><th>base32</th><td><code>JBSWY3DPFQQHO33SNRSCC===</code></td><td><code>b&#x27;Hello, world!&#x27;</code></td><td>✔</td></tr><tr><th>base32hex</th><td><code>91IMOR3F5GG7ERRIDHI22===</code></td><td><code>b&#x27;Hello, world!&#x27;</code></td><td>✔</td></tr><tr><th>base46</th><td><code>GnNaagudEKYvFzFrZSS</code></td><td><code>b&#x27;Hello, world!&#x27;</code></td><td>✔</td></tr><tr><th>base62</th><td><code>1wJfrzvdbthTq5ANZB</code></td><td><code>b&#x27;Hello, world!&#x27;</code></td><td>✔</td></tr><tr><th>base64</th><td><code>SGVsbG8sIHdvcmxkIQ==</code></td><td><code>b&#x27;Hello, world!&#x27;</code></td><td>✔</td></tr><tr><th>base64b64</th><td><code>G4JgP4wg65RjQalY6E==</code></td><td><code>b&#x27;Hello, world!&#x27;</code></td><td>✔</td></tr><tr><th>base64bash</th><td><code>i6lIr6YI87tLsCNA8g==</code></td><td><code>b&#x27;Hello, world!&#x27;</code></td><td>✔</td></tr><tr><th>base64bcrypt</th><td><code>QETqZE6qGFbtakviGO==</code></td><td><code>b&#x27;Hello, world!&#x27;</code></td><td>✔</td></tr><tr><th>base64hqx</th><td><code>5&#x27;9XE&#x27;mX)(G[FQaN)3==</code></td><td><code>b&#x27;Hello, world!&#x27;</code></td><td>✔</td></tr><tr><th>base64url</th><td><code>SGVsbG8sIHdvcmxkIQ==</code></td><td><code>b&#x27;Hello, world!&#x27;</code></td><td>✔</td></tr><tr><th>base64uu</th><td><code>2&amp;5L;&amp;\\L(&#x27;=O&lt;FQD(0</code></td><td><code>b&#x27;Hello, world!&#x27;</code></td><td>✔</td></tr><tr><th>base64xx</th><td><code>G4JgP4wg65RjQalY6E==</code></td><td><code>b&#x27;Hello, world!&#x27;</code></td><td>✔</td></tr><tr><th>base85</th><td>ERR</td><td>ERR</td><td>❌</td></tr><tr><th>base94</th><td><code>/P\|?l:+&gt;Nq\\sr&lt;+r</code></td><td><code>b&#x27;Hello, world!&#x27;</code></td><td>✔</td></tr><tr><th>crockford32</th><td><code>91JPRV3F5GG7EVVJDHJ22</code></td><td><code>b&#x27;Hello, world!&#x27;</code></td><td>✔</td></tr><tr><th>geohash32</th><td><code>91kqsv3g5hh7fvvkejk22</code></td><td><code>b&#x27;Hello, world!&#x27;</code></td><td>✔</td></tr><tr><th>nintendo32</th><td><code>91LQSW3H5JJ7GWWLFKL22</code></td><td><code>b&#x27;Hello, world!&#x27;</code></td><td>✔</td></tr><tr><th>wordsafe32</th><td><code>F3Wgjq5Q7RR9PqqWMVW44</code></td><td><code>b&#x27;Hello, world!&#x27;</code></td><td>✔</td></tr><tr><th>zbase32</th><td><code>jb1sa5dxfoo8q551pt1nn</code></td><td><code>b&#x27;Hello, world!&#x27;</code></td><td>✔</td></tr></tbody></table><strong>Errors:</strong><pre>base85: c = 99, len = 85, bpc = 7</pre>


## Getting started

```shell
$ pip install pybased
```

## Doing stuff
```python
# Lets's assume we want to use the Crockford32 encoding scheme.
from based.standards.base32 import crockford32

# And let's assume the variable data has what we want to encode.
data: bytes = ...

# Encode to string.
encoded: str = crockford32.encode_bytes(data)

# ...

# Decode the string back to bytes.
data: bytes = crockford32.decode_bytes(encoded)
```

## `based` Command-Line Tool

```shell
$ based --help
```
```
usage: based [-h] {dump,encode,decode} ...

positional arguments:
  {dump,encode,decode}

optional arguments:
  -h, --help            show this help message and exit
```


**NOTE:** The `based` CLI tool is currently only useful for testing, and is under *very* active development.

### Encode string to Base94

```shell
$ based encode --standard=base94 --input-string 'Hello, world!'
```
```
/P|?l:+>Nq\sr<+r
```


### Encode string to Base94 and output JSON

```shell
$ based encode --standard=base94 --input-string 'Hello, world!' --output-format json
```
```
{"encoded": "/P|?l:+>Nq\\sr<+r"}
```


### Decode data from Base94

```shell
$ based decode --standard=base94 --input-string '/P|?l:+>Nq\sr<+r'
```
```
>>> input chars: 16B
Bytes representation: b'Hello, world!'
Hex representation: 48656c6c6f2c20776f726c6421
```


## Various Output Encoding Formats

```shell
$ based decode --standard=base94 --input-string '/P|?l:+>Nq\sr<+r' --output-format json
```
```
>>> input chars: 16B
{"b64": "SGVsbG8sIHdvcmxkIQ==", "utf-8": "Hello, world!"}
```

```shell
$ based decode --standard=base94 --input-string '/P|?l:+>Nq\sr<+r' --output-format yaml
```
```
>>> input chars: 16B
encoded: !!binary |
  SGVsbG8sIHdvcmxkIQ==
```
