import WowWar from 0x09593c7ceb05bd65
import NonFungibleToken from 0x09593c7ceb05bd65
import MetadataViews from 0x09593c7ceb05bd65

pub fun main(from:Address,tokenID:UInt64):WowWar.WowWarMetadata{
    let nftRef = getAccount(from)
    .getCapability(WowWar.collectionPublicPath)
    .borrow<&{WowWar.WowWarCollectionPublic}>()
    ?? panic("could not borrow ref")
    let zqNFTRef = nftRef.borrowWowWar(id:tokenID)?? panic("could not borrow zq nft ref")
    let view =  zqNFTRef.resolveView(Type<WowWar.WowWarMetadata>())!
    let meta = view as! WowWar.WowWarMetadata
    return meta
}