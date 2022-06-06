import run_script
import asyncio


filename = "scripts/test_rand2.cdc"
param = []

color_num_dict = {}
for i in range(100):
    ret = asyncio.run(run_script.run_script(filename, param))
    color = ret.value
    color_num_dict.setdefault(color, 0)
    color_num_dict[color] = color_num_dict[color] + 1

print(color_num_dict)
