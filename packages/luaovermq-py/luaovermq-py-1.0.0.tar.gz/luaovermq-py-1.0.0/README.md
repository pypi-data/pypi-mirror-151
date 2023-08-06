# QuikPython
Python Bindings to LuaOverMQ

# Usage
```
from luaovermq.client import LMQClient

lmq_socket = LMQClient("tcp://127.0.0.1:8001")
print(lmq_socket.invoke("tonumber", "100"))

