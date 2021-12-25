import json
from web3 import Web3
import time 

metis_network = "HTTP://127.0.0.1:7545"
main_address = "0xA513BC64FE82870828227d4cD6e2815ff3445dD2"
contract = "0x8E7a005Ed7Ee7cdED5430f7853D07d228E923759"

abi = """[{"inputs": [], "stateMutability": "nonpayable", "type": "constructor"}, {"inputs": [{"internalType": "address", "name": "_address", "type": "address"}, {"internalType": "string", "name": "date", "type": "string"}], "name": "add_subscription", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "string", "name": "_username", "type": "string"}, {"internalType": "string", "name": "_email", "type": "string"}, {"internalType": "string", "name": "_password", "type": "string"}, {"internalType": "address", "name": "_address", "type": "address"}, {"internalType": "string", "name": "_token", "type": "string"}, {"internalType": "string", "name": "private_address", "type": "string"}, {"internalType": "string", "name": "secret_api", "type": "string"}, {"internalType": "string", "name": "public_api", "type": "string"}], "name": "add_user", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "string", "name": "_hash", "type": "string"}, {"internalType": "address", "name": "_address", "type": "address"}, {"internalType": "string", "name": "_date", "type": "string"}, {"internalType": "string", "name": "_name", "type": "string"}, {"internalType": "string", "name": "_url", "type": "string"}], "name": "add_video", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "address", "name": "_address", "type": "address"}, {"internalType": "string", "name": "_secret_api", "type": "string"}, {"internalType": "string", "name": "_public_api", "type": "string"}], "name": "change_api", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "address", "name": "_address", "type": "address"}, {"internalType": "string", "name": "_secret_api", "type": "string"}, {"internalType": "string", "name": "_public_api", "type": "string"}], "name": "check_api", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "_address", "type": "address"}, {"internalType": "uint256", "name": "_num", "type": "uint256"}], "name": "delete_video", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "address", "name": "_address", "type": "address"}], "name": "get_verify", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "_address", "type": "address"}, {"internalType": "uint256", "name": "_num1", "type": "uint256"}], "name": "getvideo", "outputs": [{"internalType": "string[]", "name": "", "type": "string[]"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "_address", "type": "address"}, {"internalType": "string", "name": "_username", "type": "string"}, {"internalType": "string", "name": "_password", "type": "string"}], "name": "login", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "_address", "type": "address"}], "name": "num_videos", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "", "type": "address"}], "name": "users", "outputs": [{"internalType": "string", "name": "username", "type": "string"}, {"internalType": "string", "name": "email", "type": "string"}, {"internalType": "string", "name": "password", "type": "string"}, {"internalType": "uint256", "name": "num", "type": "uint256"}, {"internalType": "string", "name": "token", "type": "string"}, {"internalType": "bool", "name": "verified", "type": "bool"}, {"internalType": "string", "name": "date_end", "type": "string"}, {"internalType": "string", "name": "GB", "type": "string"}, {"internalType": "string", "name": "private_address", "type": "string"}, {"internalType": "string", "name": "secret_api", "type": "string"}, {"internalType": "string", "name": "public_api", "type": "string"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "_address", "type": "address"}], "name": "verify", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "address", "name": "", "type": "address"}, {"internalType": "uint256", "name": "", "type": "uint256"}], "name": "videos", "outputs": [{"internalType": "string", "name": "hash", "type": "string"}, {"internalType": "string", "name": "name", "type": "string"}, {"internalType": "string", "name": "date_added", "type": "string"}, {"internalType": "string", "name": "url", "type": "string"}], "stateMutability": "view", "type": "function"}]"""

def get_verify(address):
    w3 = Web3(Web3.HTTPProvider(metis_network))
    w3.eth.default_account = main_address
    
    greeter = w3.eth.contract(address=contract,abi=abi)
    return greeter.functions.get_verify(address).call()

def verify(address):
    w3 = Web3(Web3.HTTPProvider(metis_network))
    w3.eth.default_account = main_address
    
    greeter = w3.eth.contract(address=contract,abi=abi)
    greeter.functions.verify(address).transact()


def add_user(username,email,password,address_created,token,private_address,secret_api,public_api):
    w3 = Web3(Web3.HTTPProvider(metis_network))
    w3.eth.default_account = main_address
    
    greeter = w3.eth.contract(address = contract,abi = abi)
    return greeter.functions.add_user(username,email,password,address_created,token,private_address,secret_api,public_api)


#to get the number of videos that's been uploaded 
def num_videos(address,contract):
    w3 = Web3(Web3.HTTPProvider(metis_network))
    w3.eth.default_account = main_address
    
    greeter = w3.eth.contract(address=contract,abi=abi)
    return greeter.functions.num_videos(address).call()

def add_video(hash,address_created,date,name,url):
    w3 = Web3(Web3.HTTPProvider(metis_network))
    w3.eth.default_account = main_address
    
    greeter = w3.eth.contract(address = contract,abi = abi)
    greeter.functions.add_video(hash,address_created,date,name,url).transact()

def getvideo(address,num1):
    w3 = Web3(Web3.HTTPProvider(metis_network))
    w3.eth.default_account = main_address
    
    greeter = w3.eth.contract(address = contract,abi = abi)
    return greeter.functions.getvideo(address,num1).call()

def change_api(address,secret_api,public_api):
    w3 = Web3(Web3.HTTPProvider(metis_network))
    w3.eth.default_account = main_address
    
    greeter = w3.eth.contract(address = contract,abi = abi)
    greeter.functions.change_api(address,secret_api,public_api).transact()


def check_api(address,secret_api,public_api):
    w3 = Web3(Web3.HTTPProvider(metis_network))
    w3.eth.default_account = main_address
    
    greeter = w3.eth.contract(address = contract,abi = abi)
    return greeter.functions.check_api(address,secret_api,public_api).call()

def add_subscription(address,date):
    w3 = Web3(Web3.HTTPProvider(metis_network))
    w3.eth.default_account = main_address
    
    greeter = w3.eth.contract(address = contract,abi = abi)
    greeter.functions.add_subscription(address,date).transact()

def get_subscription(address):
    w3 = Web3(Web3.HTTPProvider(metis_network))
    w3.eth.default_account = main_address
    
    greeter = w3.eth.contract(address = contract,abi = abi)
    greeter.functions.get_subscription(address).call()

# result = add_video("sdfdf","0xAB36979F5353131de195464d213C76AaDFd5a3EC","date","nameadf","url1")

result = getvideo("0xAB36979F5353131de195464d213C76AaDFd5a3EC",0)

print(result)
# result = add_user("0x8E7a005Ed7Ee7cdED5430f7853D07d228E923759","name","df@gmail.com","password","0xAB36979F5353131de195464d213C76AaDFd5a3EC","token","private_address","secret_api","public_api")

# verify("0xAB36979F5353131de195464d213C76AaDFd5a3EC")

# result = get_verify("0xAB36979F5353131de195464d213C76AaDFd5a3EC")
# print(result)




