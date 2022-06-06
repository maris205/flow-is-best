import WowWar from 0x09593c7ceb05bd65
import NonFungibleToken from 0x09593c7ceb05bd65

pub fun main(acc:Address):[UInt64]{
    let ref = getAccount(acc).getCapability(WowWar.collectionPublicPath)
    .borrow<&{NonFungibleToken.CollectionPublic}>()
    ?? panic("could not borrow this acc ref")
    return ref.getIDs()
}