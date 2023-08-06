<!--
[![Build Status](https://travis-ci.org/msgpack/msgpack-rpc-python.png)](https://travis-ci.org/msgpack/msgpack-rpc-python)
-->

# MessagePack RPC for Python

MessagePack RPC implementation based on Tornado.

## Installation

```sh
% pip install rpc-msgpack
```

or

```sh
% python setup.py install
```

### Module dependency

- msgpack (>= 1.0)
- tornado (>= 6.1)

## Example

### Server

```python
import msgpackrpc

class SumServer(object):
    def sum(self, x, y):
        return x + y

server = msgpackrpc.Server(SumServer())
server.listen(msgpackrpc.Address("localhost", 18800))
server.start()
```

### Client

```python
import msgpackrpc

client = msgpackrpc.Client(msgpackrpc.Address("localhost", 18800))
result = client.call('sum', 1, 2)  # = > 3
```

## Copyright

<table>
  <tr>
    <td>Author</td><td>Enes Toptas <enes.toptas@eatron.com></td>
  </tr>
  <tr>
    <td>Copyright</td><td>Copyright (c) 2022- Eatron Technologies</td>
  </tr>
  <tr>
    <td>License</td><td>Apache License, Version 2.0</td>
  </tr>
</table>
