pragma solidity ^0.7.0;


            
contract hash {
            
    string private sha = "";
    
    constructor(string memory _str){
        sha = _str;
        
    } 
    
    function getsha() public view returns (string memory) {
        return sha;
    }
    
}