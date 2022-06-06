import time

import run_script_local
import asyncio


filename = "scripts/test_rand1.cdc"
param = []

for i in range(0,100):
    ret = asyncio.run(run_script_local.run_script(filename, param))
    time.sleep(1)

