pub fun main(user_address:Address):[UInt256]{
  let my_block = getCurrentBlock()
  let height = my_block.height

  let rand_int = unsafeRandom()
  let rand_data: [UInt8] = rand_int.toBigEndianBytes()  // is `[73, 150, 2, 210, ...]`
  let tag = user_address.toString()

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

  let base_mod = UInt256(10)
  let index =  data_int % base_mod

  return [UInt256(height), index]
}