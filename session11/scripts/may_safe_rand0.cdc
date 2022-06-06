pub fun main():[UInt8]{

  let my_block = getCurrentBlock()

  let height = my_block.height
  let cur_time = my_block.timestamp

  let height_data: [UInt8] = height.toBigEndianBytes()  // is `[73, 150, 2, 210]`
  let cur_time_data: [UInt8]  = cur_time.toBigEndianBytes()

  let combine_data:[UInt8] = height_data.concat(cur_time_data)

  let data = HashAlgorithm.KECCAK_256.hash(combine_data) //[UInt8]

  var data_int:UInt256 = 0
  var data_len = UInt256(data.length)
  return data
}