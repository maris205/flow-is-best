import run_script
import asyncio
from flow_py_sdk.cadence import Address


# filename = "scripts/may_safe_rand1.cdc"
# param = []

filename = "scripts/may_safe_rand2.cdc"
account_address = Address.from_hex("0x0c7e8619918b5b1e")
param = [account_address]

ret = asyncio.run(run_script.run_script(filename, param))
