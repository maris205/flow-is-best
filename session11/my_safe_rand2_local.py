import time

import run_script_local
import run_script
import asyncio
from flow_py_sdk.cadence import Address


account_address = Address.from_hex("0x0c7e8619918b5b1e")

filename = "scripts/may_safe_rand4.cdc"
param = [account_address]
#param = []

for i in range(0,100):
    ret = asyncio.run(run_script.run_script(filename, param))
    time.sleep(1)
