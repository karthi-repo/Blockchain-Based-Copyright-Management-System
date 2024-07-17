from time import time
import requests
from web3 import Web3
import datetime
import os
import pickle
import hashlib as hasher
import acoustic.acoustid_check as ac
# import text_compare.test_text as tc
import image_compare.image_check as ic

""" Class for transactions made on the blockchain. Each transaction has a
    sender, recipient, and value.
    """
class Transaction: 
    
    """ Transaction initializer """
    def __init__(self, title="", filename="", author="", public_key="", genre="", media = ""):
        self.title = title
        self.filename = filename
        self.author = author
        self.public_key = public_key
        self.genre = genre
        self.media = media

    
    """ Converts the transaction to a dictionary """
    def toDict(self):
        return {
            'title': self.title,
            'filename': self.filename,
            'author': self.author,
            'public_key': self.public_key,
            'genre': self.genre,
            'media': self.media,
    }

    def __str__(self):
        toString = self.author + " : " + self.genre + " (" + self.media + ") "
        return toString;

""" Class for Blocks. A block is an object that contains transaction information
    on the blockchain.
    """
class Block:
    def __init__(self, index, transaction, previous_hash, transaction_hash):
        
        self.index = index
        self.timestamp = time()
        self.previous_hash = previous_hash
        self.transaction = transaction
        self.transaction_hash = transaction_hash
    
    def compute_hash(self):
        concat_str = str(self.index) + str(self.timestamp) + str(self.previous_hash) + str(self.transaction['author']) + str(self.transaction['genre'])
        hash_result = hasher.sha256(concat_str.encode('utf-8')).hexdigest()
        return hash_result

    def serialize(self):
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'transaction': self.transaction,
            'transaction_hash': self.transaction_hash
        }


""" Blockchain class. The blockchain is the network of blocks containing all the
    transaction data of the system.
    """
class Blockchain:
    def __init__(self):
        
        
        self.unconfirmed_transactions = {}
        self.chain = []
    
    def create_genesis_block(self):
        empty_media = {
            'title': "",
            'filename': "",
            'author': "",
            'public_key': "",
            'genre': "",
            'media': "",
        }
        new_block = Block(index=0, transaction=empty_media, previous_hash=0, transaction_hash="")
        self.add_block(new_block)

        return new_block
    
    def new_transaction(self, title, filename, author, public_key, genre, media):
        new_trans = Transaction(title, filename, author, public_key, genre, media).toDict();
        self.unconfirmed_transactions= new_trans.copy()
        return new_trans
    
    def mine(self,ownerprivatekey, pubkey):
        #create a block, verify its originality and add to the blockchain
        if (len(self.chain) ==0):
            block_idx = 1
            previous_hash = 0
            transaction_hash = ""
        else:
            block_idx = self.chain[-1].index + 1
            previous_hash = self.chain[-1].compute_hash()
            transaction_hash = ""
        block = Block(block_idx, self.unconfirmed_transactions, previous_hash, transaction_hash)
               #idar eth wala code add kar
        if(self.verify_block(block)):
            transaction_hash = self.store_cid_on_ethereum(ownerprivatekey, pubkey)
            block = Block(block_idx, self.unconfirmed_transactions, previous_hash, transaction_hash)
            self.add_block(block)
            #idar eth wala code add kar
            return block
        else:
            return None
    
    def verify_block(self, block):
        #verify song originality and previous hash
        #check previous hash

        if len(self.chain) ==0:
            previous_hash = 0
        else:
            previous_hash = self.chain[-1].compute_hash()
        if block.previous_hash != previous_hash:
            return 0
        #check originality
        for prev_block in self.chain:
           if block.transaction['genre'] == prev_block.transaction['genre']:
                try:
                    if block.transaction['genre'] == 'Audio':
                        score = ac.calc_accuracy('./uploads/' + block.transaction['media'], './uploads/' + prev_block.transaction['media'])
                        print(score)
                        if score > 0.9:
                          return 0
                    if block.transaction['genre'] == 'Text':
                        score = tc.check_text_similarity('./uploads/' + block.transaction['media'], './uploads/'+prev_block.transaction['media'])
                        print(score)
                        if score < 100:
                            return 0
                    if block.transaction['genre'] == "Image":
                        score = ic.calc_accuracy('./uploads/' + block.transaction['media'], './uploads/' + prev_block.transaction['media'])
                        print(score)
                        if score < 10:
                            return 0
                except:
                    return 0
        return 1

    def lookup(self, transaction):
        #check originality
        for prev_block in self.chain:
           if transaction['genre'] == prev_block.transaction['genre']:
                try:
                    if transaction['genre'] == 'Audio':
                        score = ac.calc_accuracy('./tmp/' + transaction['media'], './uploads/' + prev_block.transaction['media'])
                        print(score)
                        if score > 0.9:
                          return prev_block
                    if transaction['genre'] == 'Text':
                        score = tc.check_text_similarity('./tmp/' + transaction['media'], './uploads/'+prev_block.transaction['media'])
                        print(score)
                        if score < 100:
                            return prev_block
                    if transaction['genre'] == "Image":
                        score = ic.calc_accuracy('./tmp/' + transaction['media'], './uploads/' + prev_block.transaction['media'])
                        print(score)
                        if score < 10:
                            return prev_block
                except:
                    print("exception")
                    return prev_block
        return None
    
    def add_block(self, block):
        self.chain.append(block)
        print(block)

        with open('./blockchain/chain.pkl', 'wb') as output:
            pickle.dump(self.chain, output, pickle.HIGHEST_PROTOCOL)

    
    def check_integrity(self):
        return 0
    
    def upload_to_ipfs(self, file_path):

        API_KEY = '*your_API_KEY*'
        API_SECRET = '*your_API_SECRET*'

        # Set the endpoint for uploading files to IPFS
        UPLOAD_ENDPOINT = 'https://api.pinata.cloud/pinning/pinFileToIPFS'
        headers = {
            'pinata_api_key': API_KEY,
            'pinata_secret_api_key': API_SECRET
        }

        # Prepare the file data
        file_data = {'file': open(file_path, 'rb')}

        # Make the POST request to upload the file
        response = requests.post(UPLOAD_ENDPOINT, headers=headers, files=file_data)

        if response.status_code == 200:
            ipfs_hash = response.json()['IpfsHash']
            ipfs_path = f'URL: https://gateway.ipfs.io/ipfs/{ipfs_hash}'
            print('File uploaded successfully!')
            print('IPFS Hash:', ipfs_hash)
            print(f'URL: https://gateway.ipfs.io/ipfs/{ipfs_hash}')
        else:
            print('Failed to upload file. Status code:', response.status_code)
            print('Response:', response.text)
        
        return ipfs_hash

    def store_cid_on_ethereum(self, PrivateKey, IPFS_CID):

        infura_url = "HTTP://127.0.0.1:7545"
        private_key = PrivateKey
        # private_key = "0xbf325a07baaa8cfd2d66961c831d3fa830653128af504c9404df883bf0684c3d"
        cid = IPFS_CID
        contract_address = "*your_Contract_address*"
        store_cid_function_name = "storeCID"
        contract_abi = [{"inputs": [],"name": "cid","outputs": [{"internalType": "string","name": "","type": "string"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "string","name": "_cid","type": "string"}],"name": "storeCID","outputs": [],"stateMutability": "nonpayable","type": "function"}]

        try:
            web3 = Web3(Web3.HTTPProvider(infura_url))
            contract = web3.eth.contract(address=contract_address, abi=contract_abi)

            # Encode the function call with the CID parameter
            encoded_function_call = contract.encodeABI(
                fn_name=store_cid_function_name,
                args=[cid],
            )

            # Create the account objec
            account = web3.eth.account.from_key(private_key)

            # Create the transaction object
            txn = {
                "from": account.address,
                "to": contract_address,
                "gas": 200000,  # Adjust gas limit as needed
                "gasPrice": web3.to_wei('5', 'gwei'),  # Convert gas price to Wei
                "nonce": web3.eth.get_transaction_count(account.address),
                "data": encoded_function_call,
            }

            # Sign the transaction
            signed_txn = account.sign_transaction(txn)

            # Broadcast the transaction
            tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

            print(f"Transaction hash: {web3.to_hex(tx_hash)}")
            
            return web3.to_hex(tx_hash)
        except Exception as e:
            print(f"Error storing CID: {e}")


    @property
    def last_block(self):
        return self.chain[-1]
    

