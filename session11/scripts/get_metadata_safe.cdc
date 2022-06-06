import WowSafeWar from 0x09593c7ceb05bd65
import NonFungibleToken from 0x09593c7ceb05bd65
import MetadataViews from 0x09593c7ceb05bd65

pub fun main(from:Address,tokenID:UInt64):WowSafeWar.WowSafeWarMetadata{
    let nftRef = getAccount(from)
    .getCapability(WowSafeWar.collectionPublicPath)
    .borrow<&{WowSafeWar.WowSafeWarCollectionPublic}>()
    ?? panic("could not borrow ref")
    let zqNFTRef = nftRef.borrowWowSafeWar(id:tokenID)?? panic("could not borrow zq nft ref")
    let view =  zqNFTRef.resolveView(Type<WowSafeWar.WowSafeWarMetadata>())!
    let meta = view as! WowSafeWar.WowSafeWarMetadata
    return meta
}