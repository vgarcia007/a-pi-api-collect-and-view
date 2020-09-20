# a-pi-api-collect-and-view

Collects data form Raspberry Pi's that have running https://github.com/vgarcia007/a-pi-api


Data is saved to a sqlite3 database every 30 minutes.

Data can be viewed via web interface at port 8000.

## Requirements

One or more Raspberry's running:
https://github.com/vgarcia007/a-pi-api


## Installation

### Clone Repo
```bash
git clone https://github.com/vgarcia007/a-pi-api-collect-and-view.git
```

### Create *apps/common/devices.py*
```python
devices = [
    {
        "name": "tvheadend",
        "ip": "192.168.188.165"
    },
    {
        "name": "rpiserverschrank",
        "ip": "192.168.188.166"
    }
]
```
### Run Setup
```bash
sudo /bin/bash setup.sh
```


After Setup is completed you have 2 new services running:
* a_pi_api_collector (collects data from the devices)
* a_pi_api_frontend (Web Frontend at port 8888)