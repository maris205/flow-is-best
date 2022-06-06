import WowSafeWar from 0x09593c7ceb05bd65
import NonFungibleToken from 0x09593c7ceb05bd65
transaction{
    prepare(signer:AuthAccount){
        signer.save(<-WowSafeWar.createEmptyCollection(), to: WowSafeWar.collectionStoragePath)

        signer.link<&WowSafeWar.Collection{NonFungibleToken.CollectionPublic, WowSafeWar.WowSafeWarCollectionPublic}>(
            WowSafeWar.collectionPublicPath,
            target: WowSafeWar.collectionStoragePath
        )
    }
}