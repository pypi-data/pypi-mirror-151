
# SchoolWare.py

An API wrapper for the SchoolWareAPI made in Python.




![Logo](https://www.wisa.be/webouders/images/schoolwareLogo.png)

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
from SchoolWare import SchoolWare

SW = SchoolWare("XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX") # Your SchoolWare Token

agenda = SW.get_agenda()
print(json.dumps(agenda, indent=2))
```

## Features

- [x]  Get agenda items
- [ ]  Get scores


## Authors

- [@bjarneverschorre](https://www.github.com/bjarneverschorre)


