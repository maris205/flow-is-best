import asyncio
import flow_py_sdk
from flow_py_sdk import flow_client
from flow_py_sdk.cadence import Address
import re
import sql_appbk
#获得合约，一个账号下可能有多个合约账号+合约名为唯一id

def get_contract_name(code):
    #step 1,获得定义
    #step 1,获得所有引用
    p = re.compile('pub contract.*|access\(all\) contract.*') #引用的正则
    import_list = p.findall(code) #包含回车
    print(import_list)
    #'pub contract RaribleFee {'
    #'pub contract RaribleNFT : NonFungibleToken, LicensedNFT {'
    #'pub contract interface LicensedNFT {'
    #pub contract ExampleNFT: NonFungibleToken
    #pub contract Seussibles:然后是换行

    contract_name_line = import_list[0]
    contract_name_line = contract_name_line.replace(" interface","")
    contract_name_line = contract_name_line.replace(":", " ")
    contract_name_line = contract_name_line.replace("{", " ")

    contract_name_line_item = contract_name_line.split()
    contract_name = contract_name_line_item[2].strip()
    print(contract_name)
    return contract_name


    #p = re.compile('pub contract (.+?):|pub contract (.+?) {') #引用的正则
    # p = re.compile('pub contract (.+?)\B{') #引用的正则
    # contract_name = p.findall(code)
    # print(contract_name)

# pip3 install  flow-py-sdk
"""
fun:get contract list of a address
input: address, contract address
return: contract_list, contract list
"""
async def get_contract(address="3642161059eefb9c"):
    async with flow_client(
            host="access.mainnet.nodes.onflow.org", port=9000
    ) as client:
        service_account_address = bytes.fromhex(address)
        #到最新高度的信息
        account = await client.get_account(
            address=service_account_address
        )

        contract_data_list = []
        for key in account.contracts:
            contract = account.contracts[key]
            #print(contract.decode())
            contract_code = contract.decode()
            contract_name = get_contract_name(contract_code)
            contract_data = {
                "contract_address": "0x"+address,
                "contract_name": contract_name,
                "contract_code": contract_code
            }
            contract_data_list.append(contract_data)
        return contract_data_list

def process_all():
    sql = "select * from flow_contract_address where contract_name is null"
    result = sql_appbk.mysql_com(sql)
    for item in result:
        contract_address = item["contract_address"].replace("0x","")
        print(contract_address)
        contract_data_list = asyncio.run(get_contract(contract_address))
        sql_appbk.insert_data_list(contract_data_list, "flow_code")


if __name__ == "__main__":
    #asyncio.run(get_contract("9e03b1f871b3513"))
    process_all()

