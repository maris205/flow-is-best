import asyncio
import flow_py_sdk
from flow_py_sdk import flow_client
from flow_py_sdk import Script
from flow_py_sdk.cadence import Address
from flow_py_sdk import cadence

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
            host="access.devnet.nodes.onflow.org", port=9000
    ) as client:
        ret = await client.execute_script(
            script=script
            # , block_id
            # , block_height
        )
        print("ret", ret)
        return ret


if __name__=="__main__":
    account_address = Address.from_hex("0x0c7e8619918b5b1e")
    # #step 1， get total supply
    # filename = "scripts/get_total_supply.cdc"
    # param = []
    # ret = asyncio.run(run_script(filename, param))
    #
    # #step 2，get ids
    # filename = "scripts/get_ids.cdc"
    # param = [account_address]
    # ret = asyncio.run(run_script(filename, param))
    #
    # #step 3， get metadata
    # filename = "scripts/get_metadata.cdc"
    # param = [account_address, cadence.UInt64(1)]
    # ret = asyncio.run(run_script(filename, param))
    #
    # for i in range(0, len(ret.fields)):
    #     key = ret.struct_type.fields[i].identifier
    #     value = ret.fields[i]
    #     print(key, value)

 #step 1， get total supply
    filename = "scripts/get_total_supply_safe.cdc"
    param = []
    ret = asyncio.run(run_script(filename, param))

    #step 2，get ids
    filename = "scripts/get_ids_safe.cdc"
    param = [account_address]
    ret = asyncio.run(run_script(filename, param))

    #step 3， get metadata
    filename = "scripts/get_metadata_safe.cdc"
    param = [account_address, cadence.UInt64(2)]
    ret = asyncio.run(run_script(filename, param))

    for i in range(0, len(ret.fields)):
        key = ret.struct_type.fields[i].identifier
        value = ret.fields[i]
        print(key, value)
