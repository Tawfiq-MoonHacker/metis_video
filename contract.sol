pragma solidity 0.8.0;


contract app {

    struct video{
        string hash;
        string name;
        string date_added;
        string url;
    }
    struct user{

        string username;
        string email;
        string password;
        uint num;

        string token;
        bool verified;

        string date_end;
        string GB;

        string private_address;
        string secret_api;
        string public_api;
    }
    
    uint num_ad = 0;
    address private owner;

    mapping(address => video[]) public videos;
    mapping(address => user) public users;
    mapping(uint => address) public ad;
    
    constructor(){
        owner = msg.sender;
        
        
    }

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }

   function add_user(string memory _username, string memory _email,string memory _password,address  _address,string memory _token,string memory private_address,string memory secret_api,string memory public_api) public onlyOwner() {
       uint num = 0;
       bool _verified = false;
        

       users[_address] = user(_username,_email,_password,num,_token,_verified,"","",private_address,secret_api,public_api);
       ad[num_ad++] = _address;
       
   }
   function get_token(address _address)public onlyOwner() view returns(string memory){
       return users[_address].token;
   }
   
   function get_addresses() public onlyOwner()  view returns(address[] memory){
       address[] memory list = new address[](num_ad);
       
       for(uint i = 0;i<num_ad;i++){
           list[i] = ad[i];
       }
       return list;
   }
   
   function change_api(address _address,string memory _secret_api,string memory _public_api) public onlyOwner(){
       users[_address].secret_api = _secret_api;
       users[_address].public_api = _public_api;
    }

    function check_api(address _address,string memory _secret_api,string memory _public_api) public onlyOwner() view returns (bool){
       bytes memory b1 = bytes(users[_address].secret_api);
       bytes memory b2 = bytes(_secret_api);
       bytes memory p1 = bytes(users[_address].public_api);
       bytes memory p2 = bytes(_public_api);

       uint256 l1 = b1.length;
       if (l1 != b2.length || p2.length != p1.length ) return false;
       for (uint256 i=0; i<l1; i++) {
           if (b1[i] != b2[i]) return false;
       }
       for(uint256 i=0; i<p1.length;i++){
           if(p1[i] != p2[i]) return false;
       }
       return true;
    }

   function login(address _address, string memory _username, string memory _password) public onlyOwner()  view returns(bool){
       string memory password_check = users[_address].password;
       string memory username_check = users[_address].username;

       bytes memory b1 = bytes(_username);
       bytes memory b2 = bytes(username_check);
       bytes memory p1 = bytes(_password);
       bytes memory p2 = bytes(password_check);

       uint256 l1 = b1.length;
       if (l1 != b2.length || p2.length != p1.length ) return false;
       for (uint256 i=0; i<l1; i++) {
           if (b1[i] != b2[i]) return false;
       }
       for(uint256 i=0; i<p1.length;i++){
           if(p1[i] != p2[i]) return false;
       }
       return true;
       
       
   }
   function verify(address _address) public onlyOwner() {
       users[_address].verified = true;
   }

   function get_verify(address _address) public onlyOwner()  view returns(bool){
       return users[_address].verified;
       
   }

   function add_subscription(address _address,string memory date) public onlyOwner() {
       users[_address].date_end = date;
   }
   function get_subscription(address _address) public onlyOwner()  view returns(string memory){
       return users[_address].date_end;
   }
   
   function set_GB(address _address,string memory _GB) public  onlyOwner() {
       users[_address].GB = _GB;
   }
   function get_GB(address _address) public onlyOwner()  view returns(string memory){
       return users[_address].GB;
   }
   
   function add_video(string memory _hash, address _address,string memory _date,string memory _name,string memory _url) public onlyOwner() {
       videos[_address].push(video(_hash,_name,_date,_url));
       users[_address].num++;

   }

   function delete_video(address _address,uint  _num) public onlyOwner() {
       delete(videos[_address][_num]);
       users[_address].num--;
   }
   
   function num_videos(address _address) public onlyOwner()  view returns(uint){

       return users[_address].num;
   }

   function getvideo(address  _address,uint  _num1) public onlyOwner()  view returns(string[] memory){
       string[] memory list = new string[](4);

       list[0] = videos[_address][_num1].hash;
       list[1] = videos[_address][_num1].name;
       list[2] = videos[_address][_num1].date_added;
       list[3] = videos[_address][_num1].url;

       return list;

   }

}
