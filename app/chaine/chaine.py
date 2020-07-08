from blockchain import Blockchain
from flask import Flask, jsonify, request


@app.route('/mine', methods=['GET'])
def mine():
    """
    mine permet de miner un nouveau block.
    Elle est déclenchée par le endpoint /mine (requête GET)

    - exécute l'algorithme de preuve de travail.
    - reçoit une récompense (un coin/une pièce) pour avoir trouvé la preuve.
    - L'expéditeur est "0" pour signifier que c'est le nœud qui a extrait une
    nouvelle pièce/coin.
    - Fabrique le nouveau bloc en l'ajoutant à la chaîne

    :return: réponse en JSON contenant les informations sur le nouveau block
    et le hash précédent (immuabilité de la blockchain), et un code 200 OK.
    :rtype: <JSON>
    """
    last_block = Blockchain.last_block
    proof = Blockchain.proof_of_work(last_block)

    Blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    previous_hash = blockchain.hachage(last_block)
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
    new_transaction permet d'ajouter les données d'une
    nouvelle transaction, en format JSON.
    Elle est déclenchée par le endpoint /transactions/new (requête POST).

    - Vérifie que les valeurs demandée dans la requête sont dans les données
    envoyées en POST. Renvoie un code 400 Bad Request, le cas échéant.
    - Créé une nouvelle transaction dans un block

    :return: réponse en JSON contenant un message de confirmation et
    un code '201 Created'.
    :rtype: <JSON>
    """
    valeurs = request.get_json()

    demande = ['sender', 'recipient', 'amount']
    if not all(k in valeurs for k in demande):
        return 'Valeurs manquantes', 400

    index = blockchain.new_transaction(
                valeurs['sender'],
                valeurs['recipient'],
                valeurs['amount'],
            )

    reponse = {
        'message': f'Ajout d\'une nouvelle transaction au block {index}'
        }
    return jsonify(reponse), 201


@app.route('/chain_of_fools', methods=['GET'])
# https://youtu.be/gGAiW5dOnKo
def full_chain():
    """
    full_chain permet d'obtenir toute la chaine et sa longueur.
    Elle est déclenchée par le endpoint /chain_of_fools (requête GET).

    :return: réponse en JSON contenant la chaine et sa longueur + code 200 OK
    :rtype: <JSON>
    """
    reponse = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(reponse), 200
