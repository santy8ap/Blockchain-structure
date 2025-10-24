from flask import Flask, jsonify, request
from uuid import uuid4
import argparse

from mi_coin.blockchain import Blockchain
from mi_coin.wallet import generate_keypair, sign_message, verify_signature, pubkey_to_address

app = Flask(__name__)

# Identificador único del nodo (address)
node_identifier = str(uuid4()).replace('-', '')

# Instancia del blockchain
blockchain = Blockchain()

# ======================
#      ENDPOINTS
# ======================

@app.route('/mine', methods=['GET'])
def mine():
    # Ejecutar Proof of Work
    last_proof = blockchain.last_block.proof
    proof = blockchain.proof_of_work(last_proof)

    # Recompensa por minado: el "0" indica que proviene del sistema
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
        signature="",
        pubkey=""
    )

    previous_hash = blockchain.hash(blockchain.last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "Nuevo bloque minado",
        'index': block.index,
        'transactions': block.transactions,
        'proof': block.proof,
        'previous_hash': block.previous_hash
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount', 'signature', 'pubkey']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Verificar firma antes de añadir la transacción
    message = f"{values['sender']}:{values['recipient']}:{values['amount']}"
    if values['sender'] != "0":  # Si no es recompensa del sistema
        if not verify_signature(values['pubkey'], message, values['signature']):
            return jsonify({"message": "Invalid signature"}), 400

    index = blockchain.new_transaction(
        values['sender'], values['recipient'], values['amount'],
        values['signature'], values['pubkey']
    )
    return jsonify({'message': f'Transaction will be added to Block {index}'}), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    chain_data = [b.to_dict() for b in blockchain.chain]
    return jsonify({
        'chain': chain_data,
        'length': len(chain_data)
    }), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a list of nodes", 400
    for node in nodes:
        blockchain.register_node(node)
    return jsonify({
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes)
    }), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()
    if replaced:
        return jsonify({
            'message': 'Our chain was replaced',
            'new_chain': [b.to_dict() for b in blockchain.chain]
        }), 200
    else:
        return jsonify({
            'message': 'Our chain is authoritative',
            'chain': [b.to_dict() for b in blockchain.chain]
        }), 200


@app.route('/wallet/new', methods=['GET'])
def wallet_new():
    priv, pub = generate_keypair()
    address = pubkey_to_address(pub)
    return jsonify({
        'private_key': priv,
        'public_key': pub,
        'address': address
    }), 200


@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Nodo blockchain corriendo'}), 200


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='Port to listen on')
    args = parser.parse_args()
    app.run(host='0.0.0.0', port=args.port, debug=True)
