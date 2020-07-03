from hashlib import sha256
import json
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request

##########################################
############ CLASS BLOCKCHAIN ############
##########################################

class Blockchain:
    """
    Blockchain est la classe définissant et gère la séquence immuable de blocks.

    :param object: [description]
    :type object: [type]
    """    
    def __init__(self): 
        self.chain = []
        self.current_transactions = []    
        # créer le premier block
        self.new_block(proof=100, previous_hash=1)
    
    @property
    def last_block(self):
        """
        last_block renvoie le dernier block de la chaine

        :return: un block
        :rtype: dict
        """        
        return self.chain[-1]
    
    @staticmethod
    def hash(block):
        """
        hash crée un hachage SHA-256 d'un bloc

        :param block: le block
        :type block: <dict>
        :return: hash
        :rtype: <str>
        """
        # Le dictionnaire 'block' doit être ordonné, sinon il y aura des hachages incohérents
        # puis converti en bytes pour être haché
        block_string = json.dumps(block, sort_keys=True).encode()
        #renvoie une chaine de caractère composée d'hex
        # NB: sha256 n'est pas le meilleur algo d'hashage
        return sha256(block_string).hexdigest()

    def new_block(self, proof, previous_hash=None,):
        """
        new_block Créer un nouveau block dans la blockchain

        :param proof: La preuve donnée par l'algorithme de preuve de travail
        :type proof: <int>
        :param previous_hash: Hash du block précédent, par défaut: None
        :type previous_hash: <str>, optional
        :return: nouveau block
        :rtype: <dict>
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # RàZ de la list courante des transactions
        self.current_transactions = []
        
        self.chain.append(block)
        return block
    
    def new_transaction(self, sender, recipient, amount):
        """
        new_transaction créer une nouvelle transaction qui ira dans le block miné

        :param sender: l'adresse de l'émetteur
        :type sender: <str>
        :param recipient: l'adresse du bénéficiaire
        :type recipient: <str>
        :param amount: quantité
        :type amount: <int>
        :return: L'index du bloc qui contiendra cette transaction
        :rtype: <int>
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        valid_proof valide la preuve. Pour que la preuve soit validée,
        il faut trouver un nombre j tel que le hachage de la chaine (ij)
        se termine par 4 zéro.
        
        - encode en bytes la chaine ('dernière_preuve''preuve')
        - on en fait du hachi(parmentier) puis on la transforme en chaine hexa
        - Vérifie que le hash('dernière_preuve'+'preuve') termine par 4 zéros.

        :param last_proof: dernière preuve de travail
        :type last_proof: <int>
        :param proof: nouvelle preuve de travail
        :type proof: <int>
        :return: True si les 4 derniers chiffres sont '0000'
        :rtype: <bool>
        """        
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def proof_of_work(self, last_block):
        """
        Algorithme de preuve de travail:

         - tant que la nouvelle preuve de travail n'est pas trouvé par le mineur,
        elle est incrémenté de 1

        :param last_block: dernierblock miné
        :type last_proof: <dict>
        :return: nouvelle preuve de travail
        :rtype: <int>
        """
        
        last_proof = last_block['proof']
        
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

##########################################
############### NODE FLASK ###############
##########################################

# Initialisation du node Node
app = Flask(__name__)

# Générer une adresse unique pour ce nœud
# uuid 4 sera plus aléatoire que uuid1
node_identifier = str(uuid4()).replace('-', '')

# Instantie la Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    """
    mine définie la requète GET

    :return: réponse en JSON
    :rtype: <dict>
    """    
    # exécute l'algorithme de preuve de travail pour obtenir la prochaine preuve
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    # recevoir une récompense (un coin/pièce) pour avoir trouvé la preuve.
    # L'expéditeur est "0" pour signifier que ce nœud a extrait une nouvelle pièce/coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # fabrique le nouveau bloc en l'ajoutant à la chaîne
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    reponse = {
        'message': "Nouveau block miné",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(reponse), 200
  
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    """
    new_transaction définie la requète POST pour une nouvelle transaction

    - Vérifie que les valeurs demandée sont dans les données 
    envoyées en POST
    - créé une nouvelle transaction dans un block
    
    :return: réponse en JSON
    :rtype: <dict>
    """    
    valeurs = request.get_json()

    demande = ['sender', 'recipient', 'amount']
    if not all(k in valeurs for k in demande):
        return 'Valeurs manquantes', 400

    index = blockchain.new_transaction(valeurs['sender'], valeurs['recipient'], valeurs['amount'])

    reponse = {'message': f'Ajout d\'une nouvelle transaction au block {index}'}
    return jsonify(reponse), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    reponse = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    # https://flask.palletsprojects.com/en/1.1.x/api/#flask.json.jsonify
    return jsonify(reponse), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)