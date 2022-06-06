import WowSafeWar from 0x09593c7ceb05bd65
import NonFungibleToken from 0x09593c7ceb05bd65

transaction(recipient_address:Address){
    let minter:&WowSafeWar.NFTMinter
    // let receiver: &{NonFungibleToken.CollectionPublic}
    prepare(signer:AuthAccount){
        self.minter = signer.borrow<&WowSafeWar.NFTMinter>(from:WowSafeWar.minterStoragePath)
            ?? panic("Could not borrow a reference to the NFT minter")

    }

    execute{
        let receiver = getAccount(recipient_address)
                        .getCapability(WowSafeWar.collectionPublicPath)
                        .borrow<&{NonFungibleToken.CollectionPublic}>()
                        ?? panic("Could not get receiver reference to the NFT Collection")


        self.minter.mintNFT(
            recipient:receiver, user_address:recipient_address
        )
    }
}