# Chain of Fools

[![image](https://img.shields.io/github/license/Sam-prog-sudo/sam.github.io?style=flat-square)](https://github.com/Sam-prog-sudo/Chain-of-Fools/blob/master/LICENSE)
---
## Avant-propos

Mon but: créer une blockchain, en 🐍python🐍, en moins d'une semaine.
Il s'agit de mon premier gros projet, en python, il m'a permis de progresser et d'apprendre de mes erreurs.
J'y ai découvert Flask, les algorithmes de hachages, j'ai écris des kilomètres de docstrings.  
Soyez indulgent.e 😁.

## Table des matières

- [Avant-propos](#avant-propos)
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
- [Améliorations possibles](#améliorations-possibles)
- [FAQ](#faq)
- [License](#license)
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
- 👯Cloner ce repo sur votre machine local à l'aide de cette adresse: `https://github.com/fvcproductions/SOMEREPO`.  
- 🍴Forker ce repo.
>C'est une invitation à la contribution👋

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
Pour miner un nouveau block, il faut trouver la nouvelle preuve de travail.
Pour ce faire, il faut envoyer une requête `GET` à l'adresse `http://localhost:[numéro-de-port]/mine`.  

### Enregistrer des transaction
En suivant la nomenclature du format JSON, ajouter dans le `Body` de la requête:
```
{
 "sender": "adresse de l'émetteur",
 "recipient": "adresse du bénéficiaire",
 "amount": quantité-émise (un entier),
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

## Améliorations possibles
Cette liste n'est pas exhaustive:
- Créer des nodes qui vérifient les transactions.  
- Gérer les erreurs de 'requests'.
- Améliorer l'algorithme de travail.  
- Améliorer l'algorithme de hashage.  
- Permettre une saugarde physique de la blockchain.  
- Stocker d'autres informations sur la blockchain (hors cryptomonnaie).  
- Améliorer la sécurité des nodes (une vraie passoire...).
- Diviser l'API en modules (partie classe/gestion de la chaine, gestion des nodes)

## FAQ

>Pourquoi une blockchaine ?  

[Parce que :)](https://youtu.be/gGAiW5dOnKo)

>Euh ... les p'tites blagues dans le code, c'est normal ?  

😅  

## License
**[MIT license](http://opensource.org/licenses/mit-license.php)**
