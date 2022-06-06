import asyncio
import time

import flow_py_sdk
from flow_py_sdk import flow_client, cadence, Tx, ProposalKey, TransactionTemplates
from flow_py_sdk import Script


# pip3 install  flow-py-sdk
# need py 3.9
# 异步
from flow_py_sdk.cadence import Address
from flow_py_sdk.signer import in_memory_signer
from flow_py_sdk.signer.hash_algo import HashAlgo
from flow_py_sdk.signer.in_memory_verifier import InMemoryVerifier
from flow_py_sdk.signer.sign_algo import SignAlgo
from flow_py_sdk.signer.signer import Signer
from flow_py_sdk.signer.verifier import Verifier


async def publish_contract(name, filename):
    # First Step : Create a client to connect to the flow blockchain
    # flow_client function creates a client using the host and port
    # A test Contract define for this example, you can modify it by your self
    code = open(filename).read()
    script = Script(
        code=code)
    contract = {
        "Name": name,
        "source": code
    }
    contract_source_hex = bytes(contract["source"], "UTF-8").hex()

    async with flow_client(
            host="access.devnet.nodes.onflow.org", port=9000
    ) as client:

        account_address = Address.from_hex("09593c7ceb05bd65")
        new_signer = in_memory_signer.InMemorySigner(hash_algo=HashAlgo.SHA3_256,
                                                 sign_algo=SignAlgo.ECDSA_P256,
                                                 private_key_hex="476453b80867cd326b97737aa2b8771dffcddfd9cd5897ad0a3c7b659488c1e0")

        proposer = await client.get_account_at_latest_block(
            address=account_address.bytes
        )

        latest_block = await client.get_latest_block()
        cadenceName = cadence.String(contract["Name"])
        cadenceCode = cadence.String(contract_source_hex)
        tx = (
            Tx(
                code=TransactionTemplates.addAccountContractTemplate,
                reference_block_id=latest_block.id,
                payer=account_address,
                proposal_key=ProposalKey(
                    key_address=account_address,
                    key_id=0,
                    key_sequence_number=proposer.keys[0].sequence_number,
                ),
            ).add_arguments(cadenceName)
                .add_arguments(cadenceCode)
                .add_authorizers(account_address)
                .with_envelope_signature(
                account_address,
                0,
                new_signer,
            )
        )

        result = await client.execute_transaction(tx)
        print(result.status_code)
        print(result.status)
        print(result.error_message)
        print(result.events)




if __name__ == "__main__":
    contracts = [
        {"name":"RandWorld", "filename":"contracts/RandWorld.cdc"},
        {"name": "FungibleToken", "filename": "contracts/FungibleToken.cdc"},
        {"name": "NonFungibleToken", "filename": "contracts/NonFungibleToken.cdc"},
        {"name": "MetadataViews", "filename": "contracts/MetadataViews.cdc"},
        {"name": "WowWar", "filename": "contracts/WowWar.cdc"},
        {"name": "WowSafeWar", "filename": "contracts/WowSafeWar.cdc"},
    ]

    for item in contracts:
        name = item["name"]
        filename = item["filename"]
        asyncio.run(publish_contract(name, filename))
        time.sleep(60)
