# ECMind blue client: Manage

Helper modules for the ecmind_blue_client to ease the work with management APIs. See discussion here: https://hub.ecmind.ch/t/119

## Installation

`pip install ecmind_blue_client_manage`


## Usage

```python
from ecmind_blue_client.tcp_client import TcpClient as Client
from ecmind_blue_client_manage import manage

client = Client(hostname='localhost', port=4000, appname='test', username='root', password='optimal')
print(manage.get_users(client))
```

### `Sessions

Small example to get all sessions of a enaio server. For example useful for monitoring proposes. 

```python
from ecmind_blue_client.tcp_client import TcpClient as Client
from ecmind_blue_client_manage import manage

client = Client(hostname='localhost', port=4000, appname='test', username='root', password='optimal')
sessions = manage.get_sessions(client)
ax_sessions = list(filter(lambda s: s['instname'] == 'ax', sessions))

print(f"Number of sessions: {len(sessions)}")
print(f"Number of windows client sessions: {len(ax_sessions)}")
```
