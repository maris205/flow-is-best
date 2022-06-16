pragma solidity 0.8.2;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
//import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
//import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract WowToken is ERC20, ERC20Burnable, Pausable, Ownable {
    constructor() ERC20("Wow Token", "WOT") {
        _mint(msg.sender, 2000000000 * 10 ** decimals());
    }
}