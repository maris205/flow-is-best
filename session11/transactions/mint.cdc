import WowWar from 0x09593c7ceb05bd65
import NonFungibleToken from 0x09593c7ceb05bd65

transaction(recipient:Address){
    let minter:&WowWar.NFTMinter
    // let receiver: &{NonFungibleToken.CollectionPublic}
    prepare(signer:AuthAccount){
        self.minter = signer.borrow<&WowWar.NFTMinter>(from:WowWar.minterStoragePath)
            ?? panic("Could not borrow a reference to the NFT minter")

    }

    execute{
        let receiver = getAccount(recipient)
                        .getCapability(WowWar.collectionPublicPath)
                        .borrow<&{NonFungibleToken.CollectionPublic}>()
                        ?? panic("Could not get receiver reference to the NFT Collection")
        
        
        self.minter.mintNFT(
            recipient:receiver
        )
    }
}