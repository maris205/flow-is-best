import RandWorld from 0x09593c7ceb05bd65
pub fun main():{String:UFix64}{
    let key = RandWorld.hello()
    let value = RandWorld.hello1()
    log(key)
    log(value)
    return {key:value}
}