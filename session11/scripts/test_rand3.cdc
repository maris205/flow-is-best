pub fun main():[UInt64]{
    let my_block = getCurrentBlock()
    let height = UInt64(my_block.height)
    let big_int = unsafeRandom() //UInt64,can't run in playground, need testnet or emu
    let base_mod = UInt64(10) //same to ratio
    let rand_index = big_int % base_mod
    return [height, big_int, rand_index]
}