// RandWorld.cdc
//
// The RandWorld contract contains some random functions.
//

access(all) contract RandWorld {

     //功能：给定物品的概率分布，随机获得一个物品
     //输入：属性和对应的概率值，例如 {"White":0.5, "Green":0.3, "Blue":0.14,"Purple":0.05,"Orange":0.01},概率之和需要=1
     //返回：按照不同属性给定概率，返回一个属性，上面输入例子返回就是 颜色，如 "Blue"
      pub fun get_rand_nft(item_prob:{String:UFix64}): String {
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
            let big_int = unsafeRandom() //UInt64,can't run in playground, need testnet or emu
            //let big_int:UInt64 = 999923
            let base_mod = UInt64(ratio) //same to ratio
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

    //功能：给定一个最大值和最小值，返回两个值区间内的一个随机值，本函数精度到3位小数，如果精度要求更好，可调整ratio即可
     pub fun  get_rand_value(min_value:UFix64, max_value:UFix64): UFix64 {
              var value = 0.0
              if min_value == max_value {
                  value = min_value
                  return value
              }

              let ratio = 1000.0
              let dis = ratio*(max_value - min_value)  //ensure max_value - min_value is more than 0.001
              let big_int = unsafeRandom() //UInt64，can't run in playground, need testnet or emu
              //let big_int:UInt64 = 999923

              let base_mod = UInt64(dis + 1.0)
              let rand_value = big_int % base_mod
              let expand_value = ratio*min_value +  UFix64(rand_value)
              value = expand_value/ratio
              return  value
    }

    // Declare a public field of type String.
    //
    // All fields must be initialized in the init() function.
    access(all) let greeting: String

    // The init() function is required if the contract contains any fields.
    init() {
        self.greeting = "Hello, World!"
    }

    // Public function that returns our friendly greeting!
    access(all) fun hello(): String {
        let item_prob = {"White":0.5, "Green":0.3, "Blue":0.14,"Purple":0.05,"Orange":0.01}
        return self.get_rand_nft(item_prob: item_prob)
    }

    // Public function that returns our friendly greeting!
    access(all) fun hello1(): UFix64 {
        return self.get_rand_value(min_value:1.0, max_value:2.0)
    }
}
