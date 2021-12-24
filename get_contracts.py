import json
from web3 import Web3
import time 

metis_network = "https://andromeda.metis.io/?owner=1088"


abi = [{"inputs": [{"internalType": "string", "name": "_str", "type": "string"}], "stateMutability": "nonpayable", "type": "constructor"}, {"inputs": [], "name": "getsha", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "stateMutability": "view", "type": "function"}]

def moveDecimalPoint(num, decimal_places):
    for _ in range(abs(decimal_places)):

        if decimal_places>0:
            num *= 10; #shifts decimal place right
        else:
            num /= 10.; #shifts decimal place left

    return float(num)

#sending eth to other accounts
def transfer_coins(account_send,account_recv,private_key,quantity):
    w3 = Web3(Web3.HTTPProvider(metis_network))

    balance_send = moveDecimalPoint(w3.eth.get_balance(account_send),-18)
    
    if float(quantity) < float(balance_send):
        nonce = w3.eth.getTransactionCount(account_send)
        
        #build a transaction 
        tx = {
              'nonce':nonce,
              'to':account_recv,
              'value':w3.toWei(quantity,'ether'),
              'gas':2000000,
              'gasPrice':w3.toWei('50','gwei')
              
              }
        signed_tx = w3.eth.account.signTransaction(tx,private_key)
    
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        


def get_sha(address,contract):
    w3 = Web3(Web3.HTTPProvider(metis_network))
    w3.eth.default_account = address
    
    greeter = w3.eth.contract(address=contract,abi=abi)
    return greeter.functions.getsha().call()

