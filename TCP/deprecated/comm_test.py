#This program will test if send_command works correctly imported to a different python file 
import rob_client
from rob_client import *

send_command("print('f')")

#sleep(3)
#send_command("fwd()")
#sleep(1)
#send_command("stop()")
