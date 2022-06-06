pub fun main():[UInt64]{
    let my_block = getCurrentBlock()
    var rlist: [UInt64] = [UInt64(my_block.height), UInt64(my_block.timestamp)]
    var i = 0
    while i< 2 {
        rlist.append(unsafeRandom())
        i = i + 1
    }
    return rlist
}