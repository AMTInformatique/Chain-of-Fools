app = Flask(__name__)
# Générer une adresse unique pour ce nœud
# uuid4 est globalement plus aléatoire/unique que uuid1
node_identifier = str(uuid4()).replace('-', '')

# Instantie la Blockchain
blockchain = Blockchain()






if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument(
        '-p', '--port', default=5000, type=int, help='port to listen on'
        )
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)