class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []    
        # créer le premier block
        self.new_block(previous_hash=1, proof=100)
        
    def new_block(self):
        # créer un nouveau block et l'ajoute à la chaine
        pass
    
    def new_transaction(self):
        # ajoute une nouvelle transaction à la liste des transactions
        pass
    
    @staticmethod
    def hash(block):
        # hashe un block
        pass

    @property
    def last_block(self):
        # retourn le dernier block de la chaine
        pass
    
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
