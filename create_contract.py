from solcx import install_solc
from solcx import compile_source
from web3 import Web3
import solcx


def create_contract(address):
    install_solc(version='0.8.0')
    f = open("contract.sol",'r')
    solid = f.read()
    
    
    compiled_sol = solcx.compile_source(
        solid,
        output_values=["abi", "bin-runtime","bin"],
        solc_version="0.8.0")
    
    
    metis_network = "https://andromeda.metis.io/?owner=1088"
    
    contract_id, contract_interface = compiled_sol.popitem()
    
    # get bytecode / bin
    bytecode = contract_interface['bin']
    
    
    #get abi
    abi = contract_interface['abi']
    
    
    w3 = Web3(Web3.HTTPProvider(metis_network))
    
    
    # set pre-funded account as sender
    w3.eth.default_account = address
    
    Greeter = w3.eth.contract(abi=abi, bytecode=bytecode)
    
    tx_hash = Greeter.constructor().transact()
    
    # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    
    greeter = w3.eth.contract(address=tx_receipt.contractAddress,abi=abi)
    
    return tx_receipt.contractAddress
    
