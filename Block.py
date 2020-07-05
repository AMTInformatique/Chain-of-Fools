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
    Blockchain est la classe mère: elle gère la séquence immuable de blocks.
    """    
    def __init__(self): 
        self.chain = []
        self.current_transactions = []    
        # créer le premier block
        self.new_block(proof=1989, previous_hash=1)

    @property
    def last_block(self):
        """
        last_block renvoie le dernier block de la chaine.

        :return: un block
        :rtype: <dict>
        """        
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        hash crée un hachage SHA-256 d'un bloc.
        
        - Sérialise le <dict: block> en une <str> formatée en JSON,
        puis encode la <str> en bytes pour être haché.
        NB: La <str> doit être ordonnée, selon les clés du <dict: block>,
        sinon il y aura des hachages incohérents.
        - Hache la chaine puis renvoie une <str> composée d'hex
        NB: sha256 n'est pas le meilleur algo d'hashage.
        
        :param block: le block
        :type block: <dict>
        :return: hash
        :rtype: <str>
        """

        block_string = json.dumps(block, sort_keys=True).encode()
        return sha256(block_string).hexdigest()

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        valid_proof valide la preuve.
        Pour que la preuve soit validée, il faut trouver un nombre j
        tel que le hachage de la chaine (ij) se termine par 4 zéros.
        
        - Encode en bytes la chaine ('dernière_preuve''preuve').
        - On en fait du hachi(parmentier) puis la transforme en chaine hexa.
        - Vérifie que le hash termine par 4 zéros.

        :param last_proof: dernière preuve de travail.
        :type last_proof: <int>
        :param proof: nouvelle preuve de travail.
        :type proof: <int>
        :return: True si les 4 derniers chiffres sont '0000', sinon False.
        :rtype: <bool>
        """        
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def proof_of_work(self, last_block):
        """
        Algorithme de preuve de travail.

        - Tant que la nouvelle preuve de travail n'est pas trouvé par
          le mineur, elle est incrémenté de 1.

        :param last_block: Dernier block miné.
        :type last_proof: <dict>
        :return: Nouvelle preuve de travail.
        :rtype: <int>
        """
        
        last_proof = last_block['proof']
        
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    def new_block(self, proof, previous_hash=None,):
        """
        new_block Créer un nouveau block dans la blockchain.

        :param proof: La preuve donnée par l'algorithme de preuve de travail.
        :type proof: <int>
        :param previous_hash: Hash du block précédent, par défaut: None.
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

        # RàZ de la liste courante des transactions
        self.current_transactions = []
        
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        new_transaction créer une nouvelle transaction qui ira
        dans le block miné.

        :param sender: L'adresse de l'émetteur.
        :type sender: <str>
        :param recipient: L'adresse du bénéficiaire.
        :type recipient: <str>
        :param amount: La quantité.
        :type amount: <int>
        :return: L'index du bloc qui contiendra cette nouvelle transaction.
        :rtype: <int>
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

##########################################
############### NODE EN FLASK ###############
##########################################

# Initialisation du node 
app = Flask(__name__)

# Générer une adresse unique pour ce nœud
# uuid4 est globalement plus aléatoire que uuid1
node_identifier = str(uuid4()).replace('-', '')

# Instantie la Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    """
    mine permet de miner un nouveau block.
    Elle est déclenchée par le endpoint /mine (requête GET)
    
    - exécute l'algorithme de preuve de travail.
    - reçoit une récompense (un coin/pièce) pour avoir trouvé la preuve.
    - L'expéditeur est "0" pour signifier que c'est le nœud qui a extrait
      une nouvelle pièce/coin.
    - Fabrique le nouveau bloc en l'ajoutant à la chaîne
    
    :return: réponse en JSON contenant les informations sur le nouveau
    block et le hash précédent (immuabilité de la blockchain) + code 200 OK
    :rtype: <JSON>
    """
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

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
    new_transaction permet d'ajouter les données d'une nouvelle transaction.
    Elle est déclenchée par le endpoint /transactions/new (requête POST).

    - Vérifie que les valeurs demandée dans la requête sont dans les données
      envoyées en POST. Renvoie un code 400 Bad Request, le cas échéant.
    - Créé une nouvelle transaction dans un block
    
    :return: réponse en JSON contenant un message + code 201 Created
    :rtype: <JSON>
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
    """
    full_chain permet d'obtenir toute la chaine et sa longueur.
    Elle est déclenchée par le endpoint /chain (requête GET).

    :return: réponse en JSON contenant la chaine et sa longueur + code 201 Created
    :rtype: <JSON>
    """    
    reponse = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(reponse), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)