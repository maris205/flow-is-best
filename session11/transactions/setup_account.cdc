import WowWar from 0x09593c7ceb05bd65
import NonFungibleToken from 0x09593c7ceb05bd65
transaction{
    prepare(signer:AuthAccount){
        signer.save(<-WowWar.createEmptyCollection(), to: WowWar.collectionStoragePath)

        signer.link<&WowWar.Collection{NonFungibleToken.CollectionPublic, WowWar.WowWarCollectionPublic}>(
            WowWar.collectionPublicPath,
            target: WowWar.collectionStoragePath
        )
    }
}