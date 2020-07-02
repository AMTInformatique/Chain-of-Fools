from hashlib import sha256
import json
from time import time

class Blockchain(object):
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
    
    def proof_of_work(self, last_block):
        """
        Algorithme de preuve de travail:

         - Trouver un nombre j tel que le hachage (i*j) contient les 4 premiers zéros
         - i est la preuve précédente, et j est la nouvelle preuve

        :param last_block: dernierblock miné
        :type last_proof: <dict>
        :return: nouvelle preuve de travail
        :rtype: <int>
        """
        
        last_proof = last_block['proof']
        last_hash = self.hash(last_block)
        
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        valid_proof valide la preuve
        
        Vérifie que le hash(dernière preuve, preuve) termine par 4 zéros.

        :param last_proof: dernière preuve de travail
        :type last_proof: <int>
        :param proof: preuve de travail actuelle
        :type proof: <int>
        :return: [description]
        :rtype: <bool>
        """        
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
######
    @staticmethod
    def hash(block):
        """
        hash crée un hachage SHA-256 d'un bloc

        :param block: le block
        :type block: <dict>
        :return: hash
        :rtype: <str>
        """
        # Le dictionnaire doit être ordonné, sinon il y aura des hachages incohérents
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        """
        last_block renvoie le dernier block de la chaine

        :return: un block
        :rtype: dict
        """        
        return self.chain[-1]