import hashlib  # Provides SHA-256 hashing function
import time  # Used to get the current timestamp

# Creating the initial block class, ie. blueprint for a block in our blockchian
class Block:
    
    # Initializes a block with core attributes required for hashing and chain linkage
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    # Function for calculating the hash of a block
    def calculate_hash(self):
        h1 = hashlib.sha256(str(self.index).encode()).hexdigest()
        h2 = hashlib.sha256(str(self.timestamp).encode()).hexdigest()
        h3 = hashlib.sha256(str(self.data).encode()).hexdigest()
        h4 = hashlib.sha256(str(self.previous_hash).encode()).hexdigest()
        h5 = hashlib.sha256(str(self.nonce).encode()).hexdigest()

        h = h1 + h2 + h3 + h4 + h5
        return hashlib.sha256(h.encode()).hexdigest()
    
    # Function for mining a block with set difficulty by changing the nonce
    def mine_block(self, difficulty):
        
        # Create a target string like "00" or "000" based on difficulty
        target = "0" * difficulty

        # Keep trying new nonce values until hash meets difficulty condition
        while self.hash[:difficulty] != target:
            self.nonce += 1                     # Increment nonce to change hash input
            self.hash = self.calculate_hash()   # Recalculate hash using updated nonce   

    # Function to return a short readable representation of the block
    def __repr__(self):
        return (
            f"Block(index={self.index}, "
            f"timestamp={int(self.timestamp)}, "
            f"hash={self.hash[:10]}..., "
            f"prev={self.previous_hash[:10]}...)"
            )

# Building the Blockchain class
class Blockchain:

    # constructor for the blockchain class
    def __init__(self):
        self.chain = []                 # List that stores all blocks in the blockchain
        self.block_data = []            # Temporary storage for transactions before mining
        self.difficulty = 5             # Controls how hard mining is
        self.create_genesis_block()     # Create the first block when blockchain is initiated
    
    # Function to create the Genesis Block and append it into the Blockchain
    def create_genesis_block(self):
        genesis_block = Block(
            index = 0,
            timestamp = time.time(),
            data = "Genesis Block",
            previous_hash = "0"
        )
        self.chain.append(genesis_block)

    # Function to add a transaction to the temporary data pool
    def add_data(self, sender, recipient, amount):
        self.block_data.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
            })
    
    # Function to create a new block and append it into the Blockchain
    def create_block(self):
        
        # Prevent creation of a block if there is no data to store
        if not self.block_data:
            print("No data to add")
            return None
        
        last_block = self.chain[-1]
        new_block = Block(
            index = len(self.chain),          # Index is current length of blockchain
            timestamp = time.time(),
            data = self.block_data,
            previous_hash = last_block.hash   # Link new block to previous block
        )

        new_block.mine_block(self.difficulty)    # Perform Proof of Work on the new block
        self.block_data = []  # clear old data   # Clear temporary transaction pool
        self.chain.append(new_block)             # Add mined block to blockchain
        return new_block
    
    # A function to verify integrity by checking if hashes are correct and the previous_hash links match
    def is_valid(self):
        
        # Start validation from the second block (genesis has no previous block)
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # Verify that stored hash matches recalculated hash
            if current.hash != current.calculate_hash():
                return False

            # Check chain linkage
            if current.previous_hash != previous.hash:
                return False

        return True
    
    # Prints all blocks in the blockchain in sequential order
    def print_chain(self):
        for block in self.chain:
            print(block)

# =========================

if __name__ == "__main__":

    # Create a new blockchain instance
    bc = Blockchain()

    print("=== Blockchain Initialized ===\n")

    # Add first set of transactions
    print("Adding transactions to Block 1...")
    bc.add_data("Alice", "Bob", 50)
    bc.add_data("Bob", "Charlie", 20)
    bc.create_block()
    print("Block 1 mined and added.\n")

    # Add second set of transactions
    print("Adding transactions to Block 2...")
    bc.add_data("Charlie", "Dave", 10)
    bc.add_data("Alice", "Eve", 30)
    bc.create_block()
    print("Block 2 mined and added.\n")

    # Add third set of transactions
    print("Adding transactions to Block 3...")
    bc.add_data("Eve", "Frank", 15)
    bc.add_data("Dave", "Alice", 5)
    bc.create_block()
    print("Block 3 mined and added.\n")

    # Print the entire blockchain
    print("=== Current Blockchain ===")
    bc.print_chain()
    print()

    # Verify blockchain validity
    print("Blockchain validity:", bc.is_valid())
    print()

    # Demonstrate tampering
    print("=== Tampering with Blockchain ===")
    bc.chain[1].data[0]["amount"] = 999   # Modify transaction data
    print("Transaction data modified.\n")

    # Print blockchain after tampering
    print("=== Blockchain After Tampering ===")
    bc.print_chain()
    print()

    # Re-check blockchain validity
    print("Blockchain validity after tampering:", bc.is_valid())

    block = bc.chain[1]
    print("Stored hash:      ", block.hash)
    print("Recomputed hash:  ", block.calculate_hash())