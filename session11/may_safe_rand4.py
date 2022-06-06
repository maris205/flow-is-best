import time
import random
import run_script_local
import run_script
import asyncio
from flow_py_sdk.cadence import Address
filename = "scripts/may_safe_rand4.cdc"

#get address list
data_file = open("account.txt")
address_list = []
for line in data_file:
    line = line.strip()
    line_item = line.split()
    address = line_item[0]
    address_list.append(address)


for i in range(0,100):
    user_address = random.choice(address_list)
    account_address = Address.from_hex(user_address)
    param = [account_address]
    ret = asyncio.run(run_script.run_script(filename, param))
    time.sleep(1)
