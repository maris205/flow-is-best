import WowWar from 0x09593c7ceb05bd65
import NonFungibleToken from 0x09593c7ceb05bd65

transaction(recipient: Address,tokenID:UInt64){
    let collectionRef :&WowWar.Collection
    
    
    prepare(signer:AuthAccount){
        self.collectionRef = signer.borrow<&WowWar.Collection>(from:WowWar.collectionStoragePath)
                        ?? panic("Could not borrow collection Ref")
        
        
    }
    execute{
        let receiver = getAccount(recipient)
        let receiverRef =  receiver.getCapability(WowWar.collectionPublicPath)
                .borrow<&{WowWar.WowWarCollectionPublic}>()
                ?? panic("Could not borrow receiver collection ref")
        let nft <- self.collectionRef.withdraw(withdrawID:tokenID)
        receiverRef.deposit(token:<-nft)
    }
}