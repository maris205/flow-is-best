import run_script
import asyncio


filename = "scripts/test_rand1.cdc"
param = []

for i in range(0,100):
    ret = asyncio.run(run_script.run_script(filename, param))

