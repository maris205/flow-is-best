pub fun main():[UInt256]{

  let my_block = getCurrentBlock()

  let height = my_block.height
  let cur_time = my_block.timestamp

  let height_data: [UInt8] = height.toBigEndianBytes()  // is `[73, 150, 2, 210]`

  let data = HashAlgorithm.KECCAK_256.hashWithTag(height_data, tag:cur_time.toString()) //[UInt8]

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

  return [UInt256(height), data_int]
}