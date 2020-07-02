import hashlib
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
    
    @staticmethod
    def hash(block):
        """
        hash crée un hachage SHA-256 d'un bloc

        :param block: un block
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
        # 
        return self.chain[-1]
        pass
    

