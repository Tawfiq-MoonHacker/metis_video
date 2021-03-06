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
                
    }

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }

   function add_user(string memory _username, string memory _email,string memory _password,string memory _token,string memory private_address,string memory secret_api,string memory public_api) public {
       uint num = 0;
       bool _verified = false;
        

       users[msg.sender] = user(_username,_email,_password,num,_token,_verified,"","",private_address,secret_api,public_api);
       ad[num_ad++] = msg.sender;
       
   }
   function get_token()public view returns(string memory){
       return users[msg.sender].token;
   }
   
   
   function change_api(string memory _secret_api,string memory _public_api) public{
       users[msg.sender].secret_api = _secret_api;
       users[msg.sender].public_api = _public_api;
    }

    function check_api(string memory _secret_api,string memory _public_api) public view returns (bool){
       bytes memory b1 = bytes(users[msg.sender].secret_api);
       bytes memory b2 = bytes(_secret_api);
       bytes memory p1 = bytes(users[msg.sender].public_api);
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

   function login(string memory _username, string memory _password) public view returns(bool){
       string memory password_check = users[msg.sender].password;
       string memory username_check = users[msg.sender].username;

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
   function verify() public {
       users[msg.sender].verified = true;
   }

   function get_verify() public view returns(bool){
       return users[msg.sender].verified;
       
   }

   function add_subscription(string memory date) public {
       users[msg.sender].date_end = date;
   }
   function get_subscription() public  view returns(string memory){
       return users[msg.sender].date_end;
   }
   
   function set_GB(string memory _GB) public{
       users[msg.sender].GB = _GB;
   }
   function get_GB() public  view returns(string memory){
       return users[msg.sender].GB;
   }
   
   function add_video(string memory _hash,string memory _date,string memory _name,string memory _url) public {
       videos[msg.sender].push(video(_hash,_name,_date,_url));
       users[msg.sender].num++;

   }

   function delete_video(uint  _num) public {
       delete(videos[msg.sender][_num]);
       users[msg.sender].num--;
   }
   
   function num_videos() public  view returns(uint){

       return users[msg.sender].num;
   }

   function getvideo(uint  _num1) public view returns(string[] memory){
       string[] memory list = new string[](4);

       list[0] = videos[msg.sender][_num1].hash;
       list[1] = videos[msg.sender][_num1].name;
       list[2] = videos[msg.sender][_num1].date_added;
       list[3] = videos[msg.sender][_num1].url;

       return list;

   }

}
