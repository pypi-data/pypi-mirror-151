# DynamicLogger

DynamicLogger is an extension of logging.Logger to provide additional functionality to log "extra" values quickly and dynamically. </br>

# Installation

## One Liner
```bash
python -m pip install dynamic_logger
```

## Or if you prefer Manual Installation
``` bash
git clone https://github.com/ajatkj/dynamic_logger.git
cd dynamic_logger
pip install .
```

# Usage
```python
import dynamic_logger
import logging
logging.setLoggerClass(dynamic_logger.Logger)

# Set-up log formatter with user-definied attributes
fmt = '[%(asctime)s] <%(app)s> [%(levelname)s] <%(id)s> <%(customer_id)s> --- %(message)s' # Note: format attributes in <> are user-definited

# Load config
logging.basicConfig(format=fmt, datefmt='%d-%b-%y %H:%M:%S', level='INFO')

applogger = logging.getLogger(__name__)

@applogger.log_extras('id',int=0,customer_id='obj.customer_id') # Log value of 'id' and 'obj.customer_id'
def example_1(id=0,id2=0,obj=None):
    applogger.info('This example shows how to log values from function arguments')

if __name__ = "__main__":
    example_1(id=123456,obj={"customer_id":777})
```

Above will produce log output as below for all logging calls from the function:

```
[2022-04-19 12:53:51,658] [INFO] <123456> <customer_id:777> --- This example shows how to log values from function arguments
```

`dynamic_logger` exposes 2 main API's

1. log_extras decorator  
   `log_extras()` will log values dynamically from the decorated function
2. set_extras function  
    `set_extras()` will log static values for all subsequent `logger` calls till you call the `clear()` function.

See more examples in `example.py`

## Some Notes
1. To use with FastAPI, make sure `log_extras()` decorator is added after the path decorator of FastAPI.

# Contribution
Always open to PRs :)

<p align="center"><a href="https://github.com/ajatkj/dynamic_logger/blob/main/LICENSE"><img src="https://img.shields.io/static/v1.svg?style=flat-square&label=License&message=MIT&logoColor=eceff4&logo=github&colorA=4c566a&colorB=88c0d0"/></a></p>