import asyncio

from web3 import Web3
from loguru import logger
from eth_abi import encode
from web3.eth import AsyncEth

from config import CONTRACTS, AMOUNTS_NFT, THREADS

logger.add("logger.log", format="{time:YYYY-MM-DD | HH:mm:ss.SSS} | {level} \t| {function}:{line} - {message}")

async_web3 = Web3(
    Web3.AsyncHTTPProvider('https://rpc-testnet.whitebit.network'), 
    modules={"eth": (AsyncEth)}, middlewares=[]
)


async def mint_nft(q: asyncio.Queue):
    while not q.empty():
        try:
            address, private_key = (await q.get()).split(':')
            balance = async_web3.from_wei(await async_web3.eth.get_balance(address), 'ether')
            logger.info(f'Balance {address}: {balance} WBT')
            
            data = async_web3.keccak(text='mint(uint256)')[:4] + encode(['uint256'], [AMOUNTS_NFT])

            logger.info('Mint nft')
            for contract in CONTRACTS:
                mint = {
                    'from': address,
                    'to': async_web3.to_checksum_address(contract),
                    'data': data,
                    'gas': 100_000, 
                    'gasPrice': async_web3.to_wei(1, 'gwei'),
                    'nonce': await async_web3.eth.get_transaction_count(address),
                    'chainId': 2625
                }

                signed_txn = async_web3.eth.account.sign_transaction(mint, private_key)
                tx_hash = async_web3.to_hex(await async_web3.eth.send_raw_transaction(signed_txn.rawTransaction))

                logger.info(f'{address} | {tx_hash}')

                if len(CONTRACTS) != 1:
                    await async_web3.eth.wait_for_transaction_receipt(tx_hash)

        except Exception as error:
            logger.error(f'{address} | {error}\n')
            with open("error_mint_nft.txt", "a") as f:
                f.write(f'{address}:{private_key}\n')

        else:
            logger.success(f'Successfully mint | {address}\n')
            with open("successfully_mint_nft.txt", "a") as f:
                f.write(f'{address}:{private_key}\n')


async def main():
    with open('wallets.txt') as f:
        wallets = f.read().splitlines()

    q = asyncio.Queue()
    for wallet in wallets:
        q.put_nowait(wallet)

    tasks = [asyncio.create_task(mint_nft(q)) for _ in range(THREADS)]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    print("Bot WhiteBit mint NFT @flamingoat")

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

    logger.success('END')
    input()