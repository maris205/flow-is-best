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
    # account_address = Address.from_hex("0x85fb4b7799a02d19")
    # private_key_hex = "52b0d61a77bd61d4cc61d9f9ae925caefabeacd0049ebef60a895d355cda0da0"
    # filename = "transactions/setup_account.cdc"
    # asyncio.run(run_trans(account_address, private_key_hex, filename))

    #step 2, mint
    account_address = Address.from_hex("0x9d1005912a600bcb")
    private_key_hex = "059e642d6b0d8cd486f5a41dff11ee49481690ee3f1d6fd57a646a6e6621b951"
    filename = "transactions/mint.cdc"
    user_account_address = Address.from_hex("0x85fb4b7799a02d19")
    asyncio.run(run_trans(account_address, private_key_hex, filename, user_account_address, cadence.String("abc2"),cadence.String("abc1"),cadence.String("abc1")))


