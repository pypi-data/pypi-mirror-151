import dynamic_logger
from pydantic import BaseModel, Field
import logging

'''
Some examples on how to use dynamic_logger's Logger class.
'''

class UserModel(BaseModel):
    user_id: int = Field(..., example='10000001', description='Business ID of the campaign owner' )

fmt = '[%(asctime)s] <%(app)s> [%(levelname)s] (%(funcName)s) [%(id)s] [%(customer_id)s] [%(int)s] --- %(message)s (%(filename)s:%(lineno)d)'
logging.basicConfig(format=fmt, datefmt='%d-%b-%y %H:%M:%S', level='INFO')
logging.setLoggerClass(dynamic_logger.Logger)
applogger = logging.getLogger(__name__)
# print(logging.getLogRecordFactory())


@applogger.log_extras('id',int=0,customer_id='obj.customer_id',id1='id2') # Log value of 'id' and 'obj.customer_id'
def example_1(a,id=0,id2=0,obj=None):
    applogger.info('This example shows how to log values from function arguments')

@applogger.log_extras(id='input_model.user_id')
def example_2(input_model: UserModel):
    applogger.info('This example shows how to extract fields from a pydantic model (or any other class with "dict" method)')

def example_3(some_arg):
    applogger.set_extras({'app': 'special'})
    applogger.info('Logging with static parameters.')
    applogger.clear()

def example_4(x,y):
    applogger.info(f'No customization here. Plain & simple log entry.')

@applogger.log_extras(id="0.user_id")
def example_5(input_model):
    applogger.info(f'Using position number instead of argument name (This is same as example_2)')

if __name__ == '__main__':
    example_1(0, id=7192370129382,id2=None,obj={'customer_id': 829201024})
    u = UserModel(user_id=8888888)
    example_2(input_model=u)
    example_3('hello there')
    example_4(2,2)
    example_5(u)

# Output entries

# [2022-04-19 13:32:04,933] [INFO] (example_1) [7192370129382] [customer_id:829201024] [int:0] --- This example shows how to log values from function arguments (example.py:20)
# [2022-04-19 13:32:04,934] [INFO] (example_2) [id:8888888] --- This example shows how to extract fields from a pydantic model (or any other class with "dict" method) (example.py:24)
# [2022-04-19 13:32:04,934] <special> [INFO] (example_3) [id:8888888] --- Logging with static parameters. (example.py:28)
# [2022-04-19 13:32:04,934] [INFO] (example_4) --- No customization here. Plain & simple log entry. (example.py:32)
# [2022-04-19 13:32:04,934] [INFO] (example_5) [id:8888888] --- Using position number instead of argument name (This is same as example_2) (example.py:36)