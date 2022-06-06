import asyncio
import time

import flow_py_sdk
from flow_py_sdk import flow_client, cadence, Tx, ProposalKey
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

global my_seq_num

async def run_trans(account_address, private_key_hex, filename, *args):
    code = open(filename).read()
    async with flow_client(
            host="access.devnet.nodes.onflow.org", port=9000
    ) as client:
        #account_address = Address.from_hex("09593c7ceb05bd65")
        # Assume you stored private key somewhere safe and restore it in private_key.
        new_signer = in_memory_signer.InMemorySigner(hash_algo=HashAlgo.SHA3_256,
                                                 sign_algo=SignAlgo.ECDSA_P256,
                                                 private_key_hex=private_key_hex)

        latest_block = await client.get_latest_block()

        proposer = await client.get_account_at_latest_block(
            address=account_address.bytes
        )
        seq_num = proposer.keys[0].sequence_number

        transaction = Tx(
            code=code,
            reference_block_id=latest_block.id,
            payer=account_address,
            proposal_key=ProposalKey(
                key_address=account_address,
                key_id=0,
                key_sequence_number=seq_num,
            ),
        ).with_gas_limit(1000).add_arguments(*args).add_authorizers(account_address).with_envelope_signature(
            account_address,
            0,
            new_signer,
        )
        response = await client.send_transaction(transaction=transaction.to_signed_grpc())

        print(response.id.hex()) #tran id

if __name__ == "__main__":
    #step 1, setup accunt
    # account_address = Address.from_hex("0x0c7e8619918b5b1e")
    # private_key_hex = "ca983febc69516a85adb9d2567f4900fd270f81a7eb14fc94601614513327764"
    # filename = "transactions/setup_account.cdc"
    # asyncio.run(run_trans(account_address, private_key_hex, filename))

    #step 2, mint
    # account_address = Address.from_hex("0x09593c7ceb05bd65")
    # private_key_hex = "476453b80867cd326b97737aa2b8771dffcddfd9cd5897ad0a3c7b659488c1e0"
    # filename = "transactions/mint.cdc"
    # user_account_address = Address.from_hex("0x0c7e8619918b5b1e")
    # asyncio.run(run_trans(account_address, private_key_hex, filename, user_account_address))

    #step 1, setup accunt safewar
    # account_address = Address.from_hex("0x0c7e8619918b5b1e")
    # private_key_hex = "ca983febc69516a85adb9d2567f4900fd270f81a7eb14fc94601614513327764"
    # filename = "transactions/setup_account_safe.cdc"
    # asyncio.run(run_trans(account_address, private_key_hex, filename))


    #step 2, mint safe
    account_address = Address.from_hex("0x09593c7ceb05bd65")
    private_key_hex = "476453b80867cd326b97737aa2b8771dffcddfd9cd5897ad0a3c7b659488c1e0"
    filename = "transactions/mint_safe.cdc"
    user_account_address = Address.from_hex("0x0c7e8619918b5b1e")
    asyncio.run(run_trans(account_address, private_key_hex, filename, user_account_address))
