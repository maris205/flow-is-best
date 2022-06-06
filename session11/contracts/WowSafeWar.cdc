import NonFungibleToken from 0x09593c7ceb05bd65
import MetadataViews from 0x09593c7ceb05bd65

pub contract WowSafeWar:NonFungibleToken{
    pub var totalSupply:UInt64
    pub let minterStoragePath:StoragePath
    pub let collectionStoragePath:StoragePath
    pub let collectionPublicPath:PublicPath

    pub event ContractInitialized()

    pub event Withdraw(id:UInt64,from:Address?)
    pub event Deposit(id:UInt64,to:Address?)
    pub event Minted(id:UInt64,to:Address?)

    pub struct WowSafeWarMetadata {
        pub let name:String
        pub let description: String
        pub let url : String

        pub let quality:String //质量，就是颜色
        pub let damage: UFix64 //武器伤害
        pub let agility: UFix64 //敏捷加成
        pub let intelligence: UFix64 //智力加成

        init(
            name:String,
            description: String,
            url : String,
            quality:String,
            damage: UFix64,
            agility: UFix64,
            intelligence: UFix64
        ){
            self.name = name
            self.description =  description
            self.url = url
            self.quality = quality
            self.damage =  damage
            self.agility= agility
            self.intelligence= intelligence
        }
    }

    pub resource NFT: NonFungibleToken.INFT, MetadataViews.Resolver {
        pub let id: UInt64
        pub var metadata:WowSafeWarMetadata?

        pub fun getViews(): [Type] {
            return [
                Type<MetadataViews.Display>(),
                Type<WowSafeWar.WowSafeWarMetadata>()
            ]
        }

        pub fun resolveView(_ view: Type): AnyStruct? {
            switch view {
                case Type<MetadataViews.Display>():
                   if let meta = self.metadata{
                        let name = meta.name
                        let description = meta.description
                        return MetadataViews.Display(
                        name:name,
                        description:description,
                        thumbnail: MetadataViews.HTTPFile(
                            url: meta.url
                          )
                        )
                    }
                    return nil

                case Type<WowSafeWar.WowSafeWarMetadata>():
                    if let meta = self.metadata{
                        return WowSafeWar.WowSafeWarMetadata(
                            name:meta.name,
                            description:meta.description,
                            url: meta.url,
                            quality : meta.quality,
                            damage: meta.damage,
                            agility: meta.agility,
                            intelligence: meta.intelligence
                        )
                    }
                    return nil

            }
            return nil
        }

        init(initID: UInt64, metadata: WowSafeWar.WowSafeWarMetadata) {
            self.id = initID
            self.metadata = metadata
        }

    }

    pub resource interface WowSafeWarCollectionPublic {
        pub fun deposit(token: @NonFungibleToken.NFT)
        pub fun getIDs(): [UInt64]
        pub fun borrowNFT(id: UInt64): &NonFungibleToken.NFT
        pub fun borrowWowSafeWar(id: UInt64): &WowSafeWar.NFT? {
            post {
                (result == nil) || (result?.id == id):
                    "Cannot borrow WowSafeWar reference: the ID of the returned reference is incorrect"
            }
        }
    }

    pub resource Collection: WowSafeWarCollectionPublic, NonFungibleToken.Provider, NonFungibleToken.Receiver, NonFungibleToken.CollectionPublic, MetadataViews.ResolverCollection {
        pub var ownedNFTs: @{UInt64: NonFungibleToken.NFT}

        init () {
            self.ownedNFTs <- {}
        }

        pub fun withdraw(withdrawID: UInt64): @NonFungibleToken.NFT {
            let token <- self.ownedNFTs.remove(key: withdrawID) ?? panic("withdraw - missing NFT")

            emit Withdraw(id: token.id, from: self.owner?.address)
            return <-token
        }

        pub fun deposit(token: @NonFungibleToken.NFT) {
            let token <- token as! @WowSafeWar.NFT
            let id: UInt64 = token.id
            let oldToken <- self.ownedNFTs[id] <- token

            emit Deposit(id: id, to: self.owner?.address)
            destroy oldToken
        }

        pub fun getIDs(): [UInt64] {
            return self.ownedNFTs.keys
        }

        pub fun borrowNFT(id: UInt64): &NonFungibleToken.NFT {
            return &self.ownedNFTs[id] as &NonFungibleToken.NFT
        }

        pub fun borrowWowSafeWar(id: UInt64): &WowSafeWar.NFT? {
            if self.ownedNFTs[id] != nil {
                let ref = &self.ownedNFTs[id] as auth &NonFungibleToken.NFT
                return ref as! &WowSafeWar.NFT
            }

            return nil
        }

        pub fun borrowViewResolver(id: UInt64): &AnyResource{MetadataViews.Resolver} {
            let nft = &self.ownedNFTs[id] as auth &NonFungibleToken.NFT
            let WowSafeWar = nft as! &WowSafeWar.NFT
            return WowSafeWar as &{MetadataViews.Resolver}
        }

        destroy() {
            destroy self.ownedNFTs
        }
    }

    pub fun createEmptyCollection(): @NonFungibleToken.Collection {
        return <- create Collection()
    }

    pub resource NFTMinter {

           //数据一个tag作为随机要素，建议是用户的地址字符串
          pub fun betterRandom(tag:String):UInt256 {
              let rand_int = unsafeRandom()
              let rand_data: [UInt8] = rand_int.toBigEndianBytes()  // is `[73, 150, 2, 210]`

              let data = HashAlgorithm.KECCAK_256.hashWithTag(rand_data, tag:tag) //[UInt8]

              var data_int:UInt256 = 0
              var data_len = UInt256(data.length)

             //[UInt8] 转 UInt256
              for item in data {
                var ratio:UInt256 = 1

                var i:UInt256 = 0
                while (i<data_len-1) {
                    ratio = ratio*256
                    i = i + 1
                }
                data_int = data_int + UInt256(item)*ratio
                data_len = data_len - 1
              }
              return data_int
          }


          pub fun  get_rand_value(min_value:UFix64, max_value:UFix64,tag:String): UFix64 {
              var value = 0.0
              if min_value == max_value {
                  value = min_value
                  return value
              }

              let ratio = 1000.0
              let dis = ratio*(max_value - min_value)  //ensure max_value - min_value is more than 0.001
              //let big_int = unsafeRandom() //UInt64，can't run in playground, need testnet or emu
              //let big_int:UInt64 = 999923
              let big_int = self.betterRandom(tag:tag) //uInt256

              let base_mod = UInt256(dis + 1.0)
              let rand_value = big_int % base_mod
              let expand_value = ratio*min_value +  UFix64(rand_value)
              value = expand_value/ratio
              return  value
          }


          pub fun get_rand_nft(item_prob:{String:UFix64},tag:String): String {
            let prob_list = item_prob.values
            let nft_list = item_prob.keys

            //step 1, build area
            let ratio:UFix64 = 1000.0
            var nft_area_list:[UFix64] = [0.0]
            var prob_sum:UFix64 = 0.0

            for item in prob_list {
              prob_sum = prob_sum + item*ratio
              nft_area_list.append(prob_sum)
            }


            //step 2, get index
            //let big_int = unsafeRandom() //UInt64,can't run in playground, need testnet or emu
            //let big_int:UInt64 = 999923
            let big_int = self.betterRandom(tag:tag) //uInt256

            let base_mod = UInt256(ratio) //same to ratio
            let rand_index = UInt32(big_int % base_mod)


            var item_index = 0
            for item in nft_area_list {
              if 0.0 == item {  // 第一个不算
                continue
              }

              if UFix64(rand_index) < item {
                break
              }

              item_index = item_index + 1
            }

            let rand_nft = nft_list[item_index]
            return rand_nft
          }



        pub fun mintNFT(recipient: &{NonFungibleToken.CollectionPublic}, user_address:Address) {

            let tag = user_address.toString() //random seeds

            //武器质量概率分别
            let quality_prob = {"White":0.5, "Green":0.3, "Blue":0.14,"Purple":0.05,"Orange":0.01}

            //武器的属性值区间，不同质量的属性区间不一样
            let prop_prob = {
                "White":{"damage": [200.0,500.0],
                    "intelligence": [20.0, 40.0],
                    "agility": [10.0, 30.0]},
                "Green":{"damage": [500.0,1000.0],
                    "intelligence": [40.0, 80.0],
                    "agility": [30.0, 70.0]},
                "Blue":{"damage": [1000.0,2000.0],
                    "intelligence": [80.0, 120.0],
                    "agility": [70.0, 110.0]},
                "Purple":{"damage": [2000.0, 2600.0],
                    "intelligence": [120.0, 200.0],
                    "agility": [110.0, 190.0]},
                "Orange":{"damage": [3500.0, 3500.0],
                    "intelligence": [200.0, 400.0],
                    "agility": [190.0, 390.0]}
            }


          let quality = self.get_rand_nft(item_prob:quality_prob, tag:tag)
          log(quality)


          let weapon_metadata:WowSafeWar.WowSafeWarMetadata = WowSafeWar.WowSafeWarMetadata(
            name:"flow sword",
            description: "flow sword WowSafe",
            url : "https://flow.com",
            quality:quality,
            damage:self.get_rand_value(min_value:prop_prob[quality]!["damage"]![0], max_value:prop_prob[quality]!["damage"]![1], tag:tag),
            agility:  self.get_rand_value(min_value:prop_prob[quality]!["agility"]![0], max_value:prop_prob[quality]!["agility"]![1], tag:tag),
            intelligence:  self.get_rand_value(min_value:prop_prob[quality]!["intelligence"]![0], max_value:prop_prob[quality]!["intelligence"]![1], tag:tag),
          )

          var newNFT <- create NFT(initID: WowSafeWar.totalSupply, metadata: weapon_metadata)
          recipient.deposit(token: <-newNFT)
          WowSafeWar.totalSupply = WowSafeWar.totalSupply + 1
        }
    }

     init() {
        self.totalSupply = 0

        self.minterStoragePath = /storage/WowSafeWarMinter
        self.collectionStoragePath = /storage/WowSafeWarCollection
        self.collectionPublicPath  = /public/WowSafeWarCollection

        let collection <- create Collection()
        self.account.save(<-collection, to: self.collectionStoragePath)

        self.account.link<&WowSafeWar.Collection{NonFungibleToken.CollectionPublic, WowSafeWar.WowSafeWarCollectionPublic}>(
            self.collectionPublicPath,
            target: self.collectionStoragePath
        )

        let minter <- create NFTMinter()
        self.account.save(<-minter, to: self.minterStoragePath)

        emit ContractInitialized()
    }
}