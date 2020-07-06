# Chain of Fools

[![image](https://img.shields.io/github/license/Sam-prog-sudo/sam.github.io?style=flat-square)](https://youtu.be/gGAiW5dOnKo)
---
## Table des matières

- [Installation](#installation)
  - [Prérequis](#prérequis)
  - [Code source](#code-source)
- [Utilisation](#utilisation)
  - [Création de node](#création-de-node)
  - [Miner un block](#miner-un-block)
  - [Enregistrer des transaction](#enregistrer-des-transaction)
  - [Obtenir la blockchain](#obtenir-la-blockchain)
  - [Enregistrer un node](#enregistrer-un-node)
  - [Consensus de la blockchain](#consensus-de-la-blockchain)
- [License](https://github.com/Sam-prog-sudo/Chain-of-Fools/blob/master/LICENSE)
---
## Installation
### Prérequis

* Installer [Python 3.6+](https://www.python.org/downloads/). 

* Installer [pipenv](https://github.com/kennethreitz/pipenv).
```shell
pip install pipenv 
```
* Installer [Postman](https://www.postman.com/downloads/).

* Installer les modules requis  
```shell
pipenv install -r requirements.txt
``` 
### Code source
Plusieur solutions s'offre à vous:  
- Cloner ce repo sur votre machine local à l'aide de cette adresse: `https://github.com/fvcproductions/SOMEREPO`.  
- Forker ce repo.
----
## Utilisation
Lancer un Shell pour la création de nodes puis lancer Postman pour l'envoie de requêtes.  
### Création de node
Commencer par démarrer au moins un serveur (node):  
> Par défaut, le numéro de port est 5000  
```shell
pipenv run python Block.py
```
```shell
pipenv run python blockchain.py -p 5001
```
```shell
pipenv run python blockchain.py --port 5002
```
### Miner un block
Envoyer une requête `GET` à l'adresse `http://localhost:[numéro-de-port]/mine`.  

### Enregistrer des transaction
En suivant la nomenclature du format JSON, ajouter dans le `Body`de la requète:
```JSON
{
 "sender": "adresse de l'émetteur",
 "recipient": "adresse du bénéficiaire",
 "amount": quantité émise
}
```
Puis, envoyer la requête `POST` à l'adresse `http://localhost:[numéro-de-port]/transactions/new`. 

### Obtenir la blockchain
Pour obtenir toutes les informations stockées sur la blockchain, il suffit d'envoyer une requête `GET` à l'adresse `http://localhost:5000/chain_of_fools`.  

### Enregistrer un node
En suivant la nomenclature du format JSON, ajouter dans le `Body`de la requète:
```JSON
{
 "nodes": ["adresse du nouveau node"]
}
```
>NB: il s'agit d'une liste de node à rajouter.  

Pour enregistrer un nouveau node sur le réseau, il faut envoyer la requête `POST` à l'adresse `http://localhost:[numéro-de-port]/transactions/new`.

### Consensus de la blockchain
>Dans le cas où il y aurait plusieurs nodes, cette requête permet d'assurer la validité de la chaine, à l'aide d'un algorithme de consensus.  

Pour s'assurer que le node courant détient la chaine la plus à jour (donc la plus longue), il suffit d'envoyer une requête `GET` à l'adresse `http://localhost:5000/nodes/resolve`.
