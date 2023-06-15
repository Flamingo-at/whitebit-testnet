import random
import asyncio

from web3 import Web3
from loguru import logger

from config import MIN_VALUE, MAX_VALUE

logger.add("logger.log", format="{time:YYYY-MM-DD | HH:mm:ss.SSS} | {level} \t| {function}:{line} - {message}")


async def send_transactions(q: asyncio.Queue, wallets: list):
    while not q.empty():
        try:
            from_address, private_key = (await q.get()).split(':')
            balance = web3.from_wei(web3.eth.get_balance(from_address), 'ether')
            logger.info(f'Balance {from_address}: {balance} WBT')
            
            to_address = (random.choice(wallets)).split(':')[0]

            value = round(random.uniform(MIN_VALUE, MAX_VALUE), 2)

            logger.info(f'Sending transaction | {from_address} -> {to_address} | {value} WBT')
            transfer = {
                'from': from_address,
                'to': to_address,
                'value': web3.to_wei(value, 'ether'),
                'gas': 21_000,
                'gasPrice': web3.to_wei(1, 'gwei'),
                'nonce': web3.eth.get_transaction_count(from_address),
                'chainId': 2625
            }

            signed_txn = web3.eth.account.sign_transaction(transfer, private_key)
            tx_hash = web3.to_hex(web3.eth.send_raw_transaction(signed_txn.rawTransaction))

            logger.info(f'{from_address} | {tx_hash}')

        except Exception as error:
            logger.error(f'{from_address} | {error}\n')
            with open("error_send_transactions.txt", "a") as f:
                f.write(f'{from_address}:{private_key}\n')

        else:
            logger.success(f'Successfully | {from_address}\n')
            with open("successfully_send_transactions.txt", "a") as f:
                f.write(f'{from_address}:{private_key}\n')


async def main():
    with open('wallets.txt') as f:
        wallets = f.read().splitlines()

    wallets_random = wallets[:]
    random.shuffle(wallets_random)

    q = asyncio.Queue()
    for wallet in wallets_random:
        q.put_nowait(wallet)

    tasks = [asyncio.create_task(send_transactions(q, wallets)) for _ in range(1)]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    print("Bot WhiteBit send transaction @flamingoat")

    web3 = Web3(Web3.HTTPProvider('https://rpc-testnet.whitebit.network'))
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

    logger.success('END')
    input()