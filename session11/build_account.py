import asyncio
import time

import flow_py_sdk

import ecdsa
from flow_py_sdk import flow_client, AccountKey, signer
from ecdsa.keys import SigningKey

from flow_py_sdk import flow_client, cadence, Tx, ProposalKey, TransactionTemplates, create_account_template
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


async def create_account():
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

        #sign_algo = ecdsa.NIST256p
        # sign_algo = signer.SignAlgo.ECDSA_P256
        # hash_algo = signer.HashAlgo.SHA2_256
        # sign_algo = SignAlgo.ECDSA_secp256k1
        # hash_algo = HashAlgo.SHA2_256

        secret_key = SigningKey.generate()
        _ = secret_key.to_string()  # private_key
        verifying_key = secret_key.get_verifying_key()
        public_key = verifying_key.to_string()

        # account_key = AccountKey(
        #     public_key=public_key, sign_algo=sign_algo, hash_algo=hash_algo
        # )

        account_key = AccountKey(
            public_key=public_key
        )

        # account_key, _ = AccountKey.from_seed(
        #     seed="dfghj dfj kjhgf hgfd lkjhgf kjhgfd sdf45678l",
        #     sign_algo=SignAlgo.ECDSA_P256,
        #     hash_algo=HashAlgo.SHA3_256,
        # )

        latest_block = await client.get_latest_block()
        tx = (
            create_account_template(
                keys=[account_key],
                reference_block_id=latest_block.id,
                payer=account_address,
                proposal_key=ProposalKey(
                    key_address=account_address,
                    key_id=0,
                    key_sequence_number=proposer.keys[0].sequence_number,
                ),
            ).add_authorizers(account_address)
                .with_envelope_signature(
                account_address,
                0,
                new_signer,
            )
        )


        result = await client.execute_transaction(tx)

        print("new address event:\n")
        print(result.__dict__)
        print("\nCreating account : successfully done...")

if __name__ == "__main__":
    asyncio.run(create_account())