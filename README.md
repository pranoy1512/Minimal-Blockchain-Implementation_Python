# Minimal Blockchain Implementation (Python)

This project implements a basic blockchain from scratch to demonstrate how **hashing**, **block chaining**, **data integrity**, and **Proof-of-Work** operate at a fundamental level.

---

## 📦 Block Structure

Each block in the blockchain is represented by a `Block` class and contains the following fields:

- **index**  
  Indicates the position of the block in the blockchain.

- **timestamp**  
  Records the exact time when the block was created.

- **data**  
  Stores the transaction data included in the block.  
  In this implementation, it is a list of simple transaction dictionaries.

- **previous_hash**  
  Stores the hash of the previous block, which links blocks together and forms the chain.

- **nonce**  
  A number that is modified during mining to satisfy the Proof-of-Work condition.

- **hash**  
  A SHA-256 hash calculated from all the above fields.  
  Any change in block data results in a completely different hash.

---

## 🔍 Validation Logic and Tampering Detection

The blockchain integrity is verified using the `is_valid()` function.

Validation is performed in two steps:

1. **Hash Recalculation Check**  
   Each block’s hash is recalculated using its stored data.  
   If the recalculated hash does not match the stored hash, the block is considered tampered.

2. **Chain Link Verification**  
   Each block’s `previous_hash` is compared with the hash of the previous block.  
   If the linkage is broken, the blockchain is marked invalid.

Because each block’s hash depends on both its own data and the previous block’s hash, modifying any block invalidates that block and all subsequent blocks.

---

## ⛏️ Proof-of-Work Approach

This implementation includes a basic Proof-of-Work mechanism using a **nonce**.

- A difficulty level is defined (e.g., `difficulty = 2`).
- A block is considered valid only if its hash starts with a specific number of leading zeros (e.g., `"00"`).
- During mining, the nonce is repeatedly incremented and the hash recalculated until the difficulty condition is satisfied.

This introduces computational effort into block creation, making tampering computationally expensive.

---

## 🛠️ Technologies Used

- Python
- SHA-256 hashing (`hashlib` module)

---

## 📌 Note

This project is for educational purposes and demonstrates core blockchain concepts in a simplified manner.
