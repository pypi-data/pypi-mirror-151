
# SchoolWare.py

An API wrapper for the SchoolWareAPI made in Python.




![Logo](https://vlot-leerlingen.durme.be/css/theme/default/img/wisa/login/login_logo.jpg)

## Installation

Clone the repository and install the requirements

```bash
  git clone https://github.com/bjarneverschorre/schoolware.py
  cd schoolware.py
  pip3 install -r requirements.txt
```

## Usage/Examples

```py
import json
from datetime import datetime
from SchoolWare import SchoolWare

SW = SchoolWare("XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX", "W5IN")

agenda = SW.get_agenda(datetime(2022, 5, 19), datetime(2022, 5, 21))
print(json.dumps(agenda, indent=4))
```

## Features

- [ ]  Get agenda items
- [ ]  Get scores


## Authors

- [@bjarneverschorre](https://www.github.com/bjarneverschorre)


