import asyncio
import flow_py_sdk
from flow_py_sdk import flow_client
from flow_py_sdk import Script
from flow_py_sdk.cadence import Address
from flow_py_sdk import cadence
#本地模拟器
#pip3 install  flow-py-sdk
#need py 3.9
#异步
async def run_script(filename="test1.cdc", praram=[]):
    code = open(filename).read()
    script = Script(
        code=code,
        arguments=praram,
    )

    async with flow_client(
            host="127.0.0.1", port=3569
    ) as client:
        ret = await client.execute_script(
            script=script
            # , block_id
            # , block_height
        )
        #print("ret", ret)
        return ret


if __name__=="__main__":
    filename = "scripts/test_rand2.cdc"
    param = []
    ret = asyncio.run(run_script(filename, param))

    # filename = "scripts/test_rand2.cdc"
    # param = []
    #
    # color_num_dict = {}
    # for i in range(10):
    #     ret = asyncio.run(run_script(filename, param))
    #     color = ret.value
    #     color_num_dict.setdefault(color, 0)
    #     color_num_dict[color] = color_num_dict[color] + 1
    #
    # print(color_num_dict)


