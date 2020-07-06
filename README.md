# Chain of Fools

[![image](https://img.shields.io/github/license/Sam-prog-sudo/sam.github.io?style=plastic)](https://youtu.be/gGAiW5dOnKo)
---
## Table des matières

- [Installation](#installation)
  - [Prérequis](#prérequis)
  - [Code source](#code-source)
- [Utilisation](#utilisation)
- [Miner un block](#miner-un-block)
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
- Cloner ce repo sur votre machine local à l'aide de cette adresse: `https://github.com/fvcproductions/SOMEREPO`.  
- 
----
## Utilisation
Commencer par démarer au moins un serveur (node):
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
