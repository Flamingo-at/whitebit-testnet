<h1 align="center">WhiteBIT Testnet</h1>

<p align="center">Claiming tokens, sending transactions, deployment contracts on the WhiteBIT test network</p>
<p align="center">
<img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54">
</p>

## ⚡ Installation
+ Install [python](https://www.google.com/search?client=opera&q=how+install+python)
+ [Download](https://sites.northwestern.edu/researchcomputing/resources/downloading-from-github) and unzip repository
+ Install requirements:
```python
pip install -r requirements.txt
```

## 💻 Preparing
+ Open ```config.py``` with a text editor:
  + ```THREADS``` - number of accounts for ```claim_token_testnet.py``` and number of threads for ```deploy_contract.py``` and ```mint_nft.py```, ```send_transactions.py``` runs in 1 thread
  + ```CAPTCHA_KEY``` - your API key from [rucaptcha](https://rucaptcha.com)
  + ```CONTRACTS``` - nft contracts to be minted, you can leave one address or add more
  + ```AMOUNTS_NFT``` - amount of each nft for minting
  + ```MIN_VALUE```, ```MAX_VALUE``` - the minimum and maximum number of tokens that will be sent from the wallet. The value in this interval will be chosen randomly

With a large number of ```THREADS``` the RPC may give an error due to rate-limit

## ✔️ Usage
+ ```claim_token_testnet.py``` - creates wallets and claiming test tokens. Wallets saved in ```wallets.txt``` in the format ```{address}:{private_key}```
+ ```mint_nft.py``` - claiming nft
+ ```deploy_contract.py``` - deployment contract
+ ```send_transactions.py``` - shuffles all wallets.txt addresses and randomly sends tokens between wallets



## 📧 Contacts
+ Telegram - [@flamingoat](https://t.me/flamingoat)
