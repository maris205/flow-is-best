import time
import random
import run_script_local
import run_script
import asyncio
from flow_py_sdk.cadence import Address
filename = "scripts/may_safe_rand5.cdc"

#get address list
data_file = open("account.txt")
address_list = []
for line in data_file:
    line = line.strip()
    line_item = line.split()
    address = line_item[0]
    address_list.append(address)

index_num_dict = {}
for i in range(0,10000):
    user_address = random.choice(address_list)
    account_address = Address.from_hex(user_address)
    param = [account_address]
    ret = asyncio.run(run_script_local.run_script(filename, param))
    index = ret.value[1].value
    index_num_dict.setdefault(index, 0)
    index_num_dict[index] = index_num_dict[index] + 1

# print(index_num_dict)
index_num_list = sorted(index_num_dict.items(),key=lambda x:x[0],reverse=False)
print(index_num_list)