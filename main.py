import os
import csv
import time
import random

from loguru import logger
from termcolor import cprint

from web3 import Web3

from config import *


def read_private_keys():
    with open("private_keys.txt", "r") as file:
        private_keys = [line.strip() for line in file if line.strip()]
    return private_keys


def read_proxies():
    with open("proxies.txt", "r") as file:
        proxies = [line.strip() for line in file if line.strip()]
    return proxies


holograph_abi = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"_owner","type":"address"},{"indexed":true,"internalType":"address","name":"_approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"_tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"_owner","type":"address"},{"indexed":true,"internalType":"address","name":"_operator","type":"address"},{"indexed":false,"internalType":"bool","name":"_approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"source","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"FundsReceived","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"_from","type":"address"},{"indexed":true,"internalType":"address","name":"_to","type":"address"},{"indexed":true,"internalType":"uint256","name":"_tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"stateMutability":"payable","type":"fallback"},{"inputs":[],"name":"admin","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"target","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"adminCall","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_price","type":"uint256"}],"name":"purchase","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"wallet","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint32","name":"fromChain","type":"uint32"},{"internalType":"bytes","name":"payload","type":"bytes"}],"name":"bridgeIn","outputs":[{"internalType":"bytes4","name":"","type":"bytes4"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint32","name":"toChain","type":"uint32"},{"internalType":"address","name":"sender","type":"address"},{"internalType":"bytes","name":"payload","type":"bytes"}],"name":"bridgeOut","outputs":[{"internalType":"bytes4","name":"selector","type":"bytes4"},{"internalType":"bytes","name":"data","type":"bytes"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"burned","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"contractURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"exists","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getAdmin","outputs":[{"internalType":"address","name":"adminAddress","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getOwner","outputs":[{"internalType":"address","name":"ownerAddress","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes","name":"initPayload","type":"bytes"}],"name":"init","outputs":[{"internalType":"bytes4","name":"","type":"bytes4"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"wallet","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_operator","type":"address"},{"internalType":"address","name":"_from","type":"address"},{"internalType":"uint256","name":"_tokenId","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"onERC721Received","outputs":[{"internalType":"bytes4","name":"","type":"bytes4"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"target","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"ownerCall","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"adminAddress","type":"address"}],"name":"setAdmin","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"ownerAddress","type":"address"}],"name":"setOwner","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"sourceBurn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"sourceGetChainPrepend","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint224","name":"tokenId","type":"uint224"}],"name":"sourceMint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"wallets","type":"address[]"},{"internalType":"uint224[]","name":"tokenIds","type":"uint224[]"}],"name":"sourceMintBatch","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint224[]","name":"tokenIds","type":"uint224[]"}],"name":"sourceMintBatch","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint224","name":"startingTokenId","type":"uint224"},{"internalType":"uint256","name":"length","type":"uint256"}],"name":"sourceMintBatchIncremental","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"sourceTransfer","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"index","type":"uint256"}],"name":"tokenByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"wallet","type":"address"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"tokenOfOwnerByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"index","type":"uint256"},{"internalType":"uint256","name":"length","type":"uint256"}],"name":"tokens","outputs":[{"internalType":"uint256[]","name":"tokenIds","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"wallet","type":"address"}],"name":"tokensOfOwner","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"wallet","type":"address"},{"internalType":"uint256","name":"index","type":"uint256"},{"internalType":"uint256","name":"length","type":"uint256"}],"name":"tokensOfOwner","outputs":[{"internalType":"uint256[]","name":"tokenIds","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transfer","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"transferFrom","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}, {"inputs":[{"internalType":"uint256","name":"quantity","type":"uint256"}],"name":"getHolographFeeWei","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

def mint(private_key, proxy, wallet_index): 
    req_args = {"proxies": {"http": proxy, "https": proxy,}}
    w3 = Web3(Web3.HTTPProvider(ZORA_PRC, request_kwargs=req_args))
    account = w3.eth.account.from_key(private_key)
    address = w3.to_checksum_address(account.address)
    mint_address = w3.to_checksum_address(NFT_CONTRACT)
    holograph_contract = w3.eth.contract(address=mint_address, abi=holograph_abi)

    cprint(f'\nWallet: [{wallet_index}] | {address}', "light_green")
    logger.info(f"[{wallet_index}]|{address}|Начинаю минтить {NFT_NAME}...")


    #сheck_nft
    if CHECK_NFT:
        holograph_balance = holograph_contract.functions.balanceOf(address).call()
        if holograph_balance > 0:
            logger.warning(f"{NFT_NAME} уже есть на кошельке. Перехожу к следующему.")
            return None
    
    else:
        if LOW_GAS:
            max_fee_per_gas = w3.to_wei(0.005, "gwei")
            max_priority_fee_per_gas = w3.to_wei(0.005, "gwei")
        else:
            max_fee_per_gas = w3.to_wei(1.50000006, "gwei")
            max_priority_fee_per_gas = w3.to_wei(1.5, "gwei")

        amount = random.randint(AMOUNT[0], AMOUNT[1])
        fee = holograph_contract.functions.getHolographFeeWei(amount).call()
        tx = holograph_contract.functions.purchase(amount).build_transaction({
            "from": address,
            "chainId": 7777777,
            "nonce": w3.eth.get_transaction_count(address),
            "value": fee,
            "maxFeePerGas": int(max_fee_per_gas),
            "maxPriorityFeePerGas": int(max_priority_fee_per_gas),
        })
        tx["gas"] = int(w3.eth.estimate_gas(tx) * 1.2)

        signed_tx = w3.eth.account.sign_transaction(tx, private_key)

        try:
            tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            logger.info(f"[{wallet_index}]|{address}|Отправляю транзакцию https://explorer.zora.energy/tx/{w3.to_hex(tx_hash)}")
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            
            if receipt["status"] == 1:
                logger.success(f">>>[{wallet_index}] {address} {amount} {NFT_NAME} успешно заминтил", "green")
                success_csv(wallet_index, address, amount)
                return receipt

        except Exception as e:
            error_message = f"Failed: {str(e)}"
            if "not in the chain after 120 seconds" in str(e):
                logger.warning(f">>>[{wallet_index}] ({address}) Транзакция не в сети спустя 120 секунд, пробую еще раз через 5 секунд...")
                time.sleep(5)
                try:
                    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
                    logger.info(f"[{wallet_index}]|{address}|Отправляю транзакцию https://explorer.zora.energy/tx/{w3.to_hex(tx_hash)}")
                    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
                    
                    if receipt["status"] == 1:
                        logger.success(f">>>[{wallet_index}] {address} {amount} {NFT_NAME} успешно заминтил", "green")
                        success_csv(wallet_index, address, amount)
                        return receipt
                    
                except Exception as e:
                    error_message = f"Failed: {str(e)}"
                    logger.error(f">>>[{wallet_index}] ({address}) Произошла ошибка при минте {amount} {NFT_NAME}: {str(e)}")
                    failed_csv(wallet_index, private_key, address, error_message)
                    return None
            else:
                logger.error(f">>>[{wallet_index}] ({address}) Произошла ошибка при минте {amount} {NFT_NAME}: {str(e)}")
                failed_csv(wallet_index, private_key, address, error_message)
                return None


def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def create_csv(file_path, header):
    if not os.path.exists(file_path):
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)

def success_csv(wallet_index, account_address, amount):
    create_dir('results')
    create_csv(f'results/success.csv', ['wallet_index', 'address', 'amount'])
    with open('results/success.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(['wallet_index', 'address', 'amount'])
        writer.writerow([f"{wallet_index}", account_address, amount])

def failed_csv(wallet_index, private_key, account_address, error_message):
    create_dir('results')
    create_csv('results/failed.csv', ['wallet_index', 'private_key', 'address', 'error'])
    with open('results/failed.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(['wallet_index', 'private_key', 'address', 'error'])        
        writer.writerow([f"{wallet_index}", private_key, account_address, error_message])


belomor = r'''
  _______   ______   __       ______   ___ __ __   ______   ______            
/_______/\ /_____/\ /_/\     /_____/\ /__//_//_/\ /_____/\ /_____/\       
\::: _  \ \\::::_\/_\:\ \    \:::_ \ \\::\| \| \ \\:::_ \ \\:::_ \ \       
 \::(_)  \/_\:\/___/\\:\ \    \:\ \ \ \\:.      \ \\:\ \ \ \\:(_) ) )_   
  \::  _  \ \\::___\/_\:\ \____\:\ \ \ \\:.\-/\  \ \\:\ \ \ \\: __ `\ \  
   \::(_)  \ \\:\____/\\:\/___/\\:\_\ \ \\. \  \  \ \\:\_\ \ \\ \ `\ \ \ 
    \_______\/ \_____\/ \_____\/ \_____\/ \__\/ \__\/ \_____\/ \_\/ \_\/ 
     https://github.com/vittoriomaisano
'''


def main():
    cprint(belomor, "cyan")
    print('Holograph-Zora minter запущен...')
    print(f'Shuffle: {SHUFFLE}\n')
    time.sleep(3)

    private_keys = read_private_keys()
    proxies = read_proxies()
    numbered_private_keys = list(enumerate(private_keys, start=1))
    original_private_keys = numbered_private_keys.copy()
    wallet_pair = dict(zip(private_keys, proxies))
    for private_key in private_keys:
        proxy = wallet_pair[private_key]

    if not private_keys:
        cprint("Отсутствуют приватные ключи. Завершаю работу.", "red")
        return
    
    if len(proxies) != len(private_keys):
        cprint("Количество приватных ключей не соответствует количеству прокси. Завершаю работу.", "red")
        return

    if SHUFFLE:
        random.shuffle(numbered_private_keys)

    for _, private_key in numbered_private_keys:
        wallet_index = next(index for index, (_, key) in enumerate(original_private_keys, start=1) if key == private_key)

        try:
            mint(private_key, proxy, wallet_index)
        except Exception as e:
            logger.error(f">>>[{wallet_index}] Произошла ошибка: {str(e)}")

        sleep = random.randint(DELAY[0], DELAY[1])
        logger.info(f"Ожидание {sleep} секунд перед следующим кошельком...", "yellow")
        time.sleep(sleep)

    print("\nHolograph-Zora minter завершен.\n")

if __name__ == "__main__":
    main()