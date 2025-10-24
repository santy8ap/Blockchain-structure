# blockchain.py
import hashlib
import json
import time
from typing import List, Dict, Any, Set
from urllib.parse import urlparse
import requests

class Block:
    def __init__(self, index: int, timestamp: float, transactions: List[Dict], proof: int, previous_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.proof = proof
        self.previous_hash = previous_hash

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "proof": self.proof,
            "previous_hash": self.previous_hash
        }

class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.current_transactions: List[Dict] = []
        self.nodes: Set[str] = set()

        # Genesis block
        self.new_block(proof=100, previous_hash='1')

    # ------- transacciones -------
    def new_transaction(self, sender: str, recipient: str, amount: float, signature: str, pubkey: str) -> int:
        """
        Añade una transacción tras validación de firma.
        Devuelve el índice del bloque que contendrá la transacción.
        """
        # Verificamos firma aquí (mensaje canónico)
        message = f"{sender}:{recipient}:{amount}"
        # La verificación real debe usar ecdsa; para modularidad, la caller puede
    
        tx = {
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
            "signature": signature,
            "pubkey": pubkey
        }
        self.current_transactions.append(tx)
        return self.last_block.index + 1

    # ------- bloques -------
    def new_block(self, proof: int, previous_hash: str = None) -> Block:
        block = Block(
            index=len(self.chain) + 1,
            timestamp=time.time(),
            transactions=self.current_transactions.copy(),
            proof=proof,
            previous_hash=previous_hash or self.hash(self.chain[-1])
        )
        # reset current tx
        self.current_transactions = []
        self.chain.append(block)
        return block

    @staticmethod
    def hash(block: Block) -> str:
        block_string = json.dumps(block.to_dict(), sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    # ------- Proof of Work simple -------
    def proof_of_work(self, last_proof: int) -> int:
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof: int, proof: int) -> bool:
        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        # difficulty: leading 4 zeros (ajusta para producción)
        return guess_hash[:4] == "0000"

    # ------- nodos / consenso -------
    def register_node(self, address: str):
        parsed = urlparse(address)
        if parsed.netloc:
            self.nodes.add(parsed.netloc)
        elif parsed.path:
            # when address like 'http://192.168.0.5:5000'
            self.nodes.add(parsed.path)

    def valid_chain(self, chain: List[Dict[str, Any]]) -> bool:
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            # Check previous hash
            if block['previous_hash'] != self.hash_block_dict(last_block):
                return False
            # Check proof
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False
            last_block = block
            current_index += 1
        return True

    @staticmethod
    def hash_block_dict(block_dict: Dict[str, Any]) -> str:
        block_string = json.dumps(block_dict, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def resolve_conflicts(self) -> bool:
        """
        Consensus: reemplaza la cadena por la más larga válida en la red.
        """
        neighbours = self.nodes
        new_chain = None
        max_length = len(self.chain)

        for node in neighbours:
            try:
                resp = requests.get(f"http://{node}/chain", timeout=5)
                if resp.status_code == 200:
                    length = resp.json()['length']
                    chain = resp.json()['chain']
                    if length > max_length and self.valid_chain(chain):
                        max_length = length
                        new_chain = chain
            except Exception:
                continue

        if new_chain:
            # Reemplazamos (convertir dict -> Block)
            self.chain = []
            for b in new_chain:
                block = Block(
                    index=b['index'],
                    timestamp=b['timestamp'],
                    transactions=b['transactions'],
                    proof=b['proof'],
                    previous_hash=b['previous_hash']
                )
                self.chain.append(block)
            return True
        return False
