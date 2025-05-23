from web3 import Web3

# Connect to the blockchain (e.g., Infura)
infura_url = "94.237.61.252:47148"
web3 = Web3(Web3.HTTPProvider(infura_url))

# Check if connected
if not web3.is_connected():
    raise Exception("Failed to connect to the blockchain")

# Player details
private_key = "0x79b953631f5c8a13f6d844ac98e2958dda1134bcb41568df341898534bf8beaa"
player_address = "0xAD9d9573A063a6d11808d32b0A720F6f3eaCD136"

# Contract addresses
setup_contract_address = "0x48D6f6bb1072f2173C23bE243826309da81B655b"

# Contract ABIs (replace with the actual ABIs)
setup_abi = [
    {
        "inputs": [],
        "name": "TARGET",
        "outputs": [{"internalType": "contract Eldorion", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "isSolved",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    }
]

eldorion_abi = [
    {
        "inputs": [],
        "name": "health",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "damage", "type": "uint256"}],
        "name": "attack",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "isDefeated",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    }
]

# Create contract instances
setup_contract = web3.eth.contract(address=setup_contract_address, abi=setup_abi)

# Get the address of the Eldorion contract
target_address = setup_contract.functions.TARGET().call()
print(f"Eldorion contract address: {target_address}")

# Create Eldorion contract instance
eldorion_contract = web3.eth.contract(address=target_address, abi=eldorion_abi)

# Function to get Eldorion's health
def get_health():
    health = eldorion_contract.functions.health().call()
    print(f"Eldorion's health: {health}")
    return health

# Function to attack Eldorion
def attack(damage):
    nonce = web3.eth.getTransactionCount(player_address)
    tx = eldorion_contract.functions.attack(damage).buildTransaction({
        'chainId': 1,  # Mainnet (replace with the correct chain ID)
        'gas': 2000000,
        'gasPrice': web3.toWei('20', 'gwei'),
        'nonce': nonce,
    })
    signed_tx = web3.eth.account.signTransaction(tx, private_key=private_key)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(f"Attack transaction sent! Hash: {web3.toHex(tx_hash)}")
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    print("Transaction receipt:", tx_receipt)

# Function to check if Eldorion is defeated
def check_defeated():
    is_defeated = eldorion_contract.functions.isDefeated().call()
    print(f"Is Eldorion defeated? {is_defeated}")
    return is_defeated

# Function to check if the challenge is solved
def check_solved():
    is_solved = setup_contract.functions.isSolved().call()
    print(f"Is the challenge solved? {is_solved}")
    return is_solved

# Main interaction
if __name__ == "__main__":
    # Get Eldorion's current health
    get_health()

    # Attack Eldorion with 100 damage (repeat until health is 0)
    while True:
        attack(100)
        health = get_health()
        if health == 0:
            break

    # Check if Eldorion is defeated
    check_defeated()

    # Check if the challenge is solved
    check_solved()



HTB{k3r4S_L   r	y   r   r   r1nj   rct   r0   r}
    
