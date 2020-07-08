

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    """
    register_nodes permet d'enregistrer au moins un nouveau node,
    en format JSON.
    Elle est déclenchée par le endpoint /nodes/register (requête POST).

    - Vérifie que les valeurs envoyé dans la requête POST existe.
    Renvoie un code 400 Bad Request, le cas échéant.
    - Enregistre les nodes grace à la méthode register_node.

    :return: réponse en JSON contenant un message de confirmation,
    la liste des nodes et un code 201 Created.
    :rtype: <JSON>
    """
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Erreur: Veuillez fournir une liste valide de nœuds", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'Au mois un nouveau node a été ajouté.',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    """
    consensus regarde si la chaine courante fait consensus.
    Elle est déclenchée par le endpoint /nodes/resolve (requête GET).

    :return: réponse en JSON contenant un message spécifiant la chaine
    faisant autorité, et un code 200 OK.
    :rtype: <JSON>
    """
    replaced = blockchain.algo_cansensus()

    if replaced:
        response = {
            'message': 'La chaine courante a été remplacée.',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'La chaine courante fait authorité.',
            'chain': blockchain.chain
        }
    return jsonify(response), 200
