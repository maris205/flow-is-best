import asyncio
import time

import flow_py_sdk
from flow_py_sdk import flow_client
import re
import sql_appbk
from concurrent.futures import ThreadPoolExecutor



# pip3 install  flow-py-sdk
# need py 3.9
# 异步

"""
功能：解析trans脚本，获得引用的合约地址
输入：script，trans脚本
返回：合约地址
"""
def get_contract_address(trans_script):
    #step 1,获得所有引用
    p = re.compile('import.{3,30}from 0x\w{10,25}') #引用的正则
    import_list = p.findall(trans_script)

    #step 2，解析所有引用
    import_data_list = []
    for item in import_list:
        item_list = item.split()
        contract_name = item_list[1]
        contract_address = item_list[3]
        #print(contract_name, contract_address)
        import_data = {
            "contract_name":contract_name,
            "contract_address":contract_address,
        }
        import_data_list.append(import_data)
    return import_data_list



async def get_trans(height=31893338):
    async with flow_client(
            host="access.mainnet.nodes.onflow.org", port=9000
    ) as client:
        latest_block = await client.get_latest_block()
        block = await client.get_block_by_height(height=height)
        #collection是transaction的集合
        trans_list = []
        for i in range(len(block.collection_guarantees)):
            collection_id = block.collection_guarantees[i].collection_id
            collection = await client.get_collection_by_i_d(id=collection_id)
            for trans_id in collection.transaction_ids:
                trans_id_hex = trans_id.hex()
                transaction = await client.get_transaction(id=trans_id)
                user_address= transaction.proposal_key.address.hex()

                trans_script = transaction.script.decode("utf-8")
                #print(trans_script)
                import_data_list = get_contract_address(trans_script)
                for import_data in import_data_list:
                    trans_data = {
                        "trans_id":trans_id_hex,
                        "user_address":"0x" + user_address,
                        "contract_name":import_data["contract_name"],
                        "contract_address":import_data["contract_address"],
                    } #注意使用的时候，基础的nft等类，可以不用
                    #print(trans_data)
                    trans_list.append(trans_data)
        try:
            sql_appbk.insert_data_list(trans_list, "trans_data")
            return 0
        except Exception as e:
            print("ERROR", e)

        return -1



def thread_run(height):
    asyncio.run(get_trans(height))
    #time.sleep(5)


def get_all():
    concurrency_num = 30  #线程数
    executor = ThreadPoolExecutor(max_workers=concurrency_num)
    for height in range(31893338, 31293338, -1*concurrency_num):
        print(height, "time", time.time())

        future_list = []  # 多线程列表

        for i in range(0, concurrency_num):
            thread_height = height - i
            print("thread_height", thread_height)
            future = executor.submit(thread_run, thread_height)
            future_list.append(future)

        #等待完成
        for future in future_list:
            ret = future.result()  # 等待

if __name__ == "__main__":
    #asyncio.run(get_trans())
    get_all()
