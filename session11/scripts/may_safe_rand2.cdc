pub fun main(user_address:Address):UInt256{
  let user_address_data = user_address.toBytes()  // is `[67, 97, 100, 101, 110, 99, 101, 33]`

  let my_block = getCurrentBlock()
  let height = my_block.height
  let cur_time = my_block.timestamp

  let height_data: [UInt8] = height.toBigEndianBytes()  // is `[73, 150, 2, 210]`
  let cur_time_data: [UInt8]  = cur_time.toBigEndianBytes()

  let combine_data:[UInt8] = height_data.concat(cur_time_data).concat(user_address_data)
  let data = HashAlgorithm.KECCAK_256.hash(height_data.concat(combine_data))

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