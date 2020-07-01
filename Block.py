from time import time

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []    
        # créer le premier block
        self.new_block(proof=100, previous_hash=1)
        
    def new_block(self, proof, previous_hash=None,):
        """
        Créer un nouveau block dans la blockchain
        :param proof: <int> La preuve donnée par l'algorithme de preuve de travail
        :param previous_hash: (Optionel) <str> Hash du block précédent 
        :return: <dict> nouveau block
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
        créer une nouvelle transaction qui ira dans le block miner
        :param sender: <str> l'adresse de l'émetteur
        :param recipient: <str> l'adresse du bénéficiaire
        :param amount: <int> quantité
        :return: <int> L'index du bloc qui contiendra cette transaction
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1
    
    @staticmethod
    def hash(block):
        # hashe un block
        pass

    @property
    def last_block(self):
        # retourn le dernier block de la chaine
        pass
    

