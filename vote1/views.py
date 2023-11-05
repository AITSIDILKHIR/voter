

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

from web3 import Web3
from web3.middleware import geth_poa_middleware
import json

from eth_account import Account

def accueil(request):
    return render(request, 'accueil.html')
    


def resultat_de_vote(request):
    from web3 import Web3
    from web3.middleware import geth_poa_middleware
    import json

    from eth_account import Account

    contract_address = "0xb5a9cabEBBDA33964842B1F1D627cCa9380BC763"
    abi =[
	{
		"constant": False,
		"inputs": [
			{
				"internalType": "uint256",
				"name": "choix",
				"type": "uint256"
			}
		],
		"name": "voter",
		"outputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [],
		"name": "vote_p_1",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [],
		"name": "vote_p_2",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "voters",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	}
]

# Insérez ici l'ABI de votre contrat

# Insérez ici votre clé privée MetaMask
    private_key = "cd75933975c214970c161c81298faecc626b5a6c2814bf81b2746e2babec55a2"


    w3 = Web3(Web3.HTTPProvider("https://sepolia.infura.io/v3/395faf7faee7414484b0ce9cc7059c8c"))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    contract = w3.eth.contract(address=contract_address, abi=abi)
    nonce = w3.eth.get_transaction_count('0xb9380FBAa7De47828bbc0d770b9dFd97779f1E5F')
    nom_personne = request.GET['nom_personne']
    if nom_personne=='MASTER DSEF':
        choix=1
    elif nom_personne=='MASTER IMQ':
        choix=2

    txn_dict = {
        'chainId': 11155111,
        'gas': 2000000,
        'gasPrice': 3000000,
		
        
        
        'nonce': nonce,
        'to': contract_address,
        'value': 0,
        'data': contract.encodeABI(fn_name='voter', args=[choix]),
    }
    account = Account.from_key(private_key)
    signed_txn = account.sign_transaction(txn_dict)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    votes_p1 = contract.functions.vote_p_1().call()
    votes_p2 = contract.functions.vote_p_2().call()
    if votes_p1 > votes_p2:
        gagnat='master DSEF'
    else:
        gagnat='master IMQ'

    nom_personne = request.GET['nom_personne']
    if nom_personne=='MASTER DSEF':
        choix=1
    elif nom_personne=='MASTER IMQ':
        choix=2
    

    return render(request, 'resultat_de_vote.html', {'nom_personne': nom_personne, 'votes_p1': votes_p1, 'votes_p2': votes_p2,'choix':choix,'gagnat':gagnat}) # 'non_personne' ={{ nom_personne }} dans resulta.html
    

