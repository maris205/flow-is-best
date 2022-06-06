pub fun main():String{
    let item_prob = {"White":0.5, "Green":0.3, "Blue":0.14,"Purple":0.05,"Orange":0.01}
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