import ExampleNFT from  0x9d1005912a600bcb
import NonFungibleToken from  0x9d1005912a600bcb

pub fun main(acc:Address):[UInt64]{
    let ref = getAccount(acc).getCapability(ExampleNFT.CollectionPublicPath)
    .borrow<&{NonFungibleToken.CollectionPublic}>()
    ?? panic("could not borrow this acc ref")
    return ref.getIDs()
}