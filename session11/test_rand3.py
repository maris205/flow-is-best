import run_script
import asyncio


filename = "scripts/test_rand3.cdc"
param = []

index_num_dict = {}
for i in range(100):
    ret = asyncio.run(run_script.run_script(filename, param))
#     index = ret.value
#     index_num_dict.setdefault(index, 0)
#     index_num_dict[index] = index_num_dict[index] + 1
#
# print(index_num_dict)
