import asyncio

from web3.auto import w3
from loguru import logger
from aiohttp import ClientSession
from pyuseragents import random as random_useragent

from config import CAPTCHA_KEY, THREADS

logger.add("logger.log", format="{time:YYYY-MM-DD | HH:mm:ss.SSS} | {level} \t| {function}:{line} - {message}")


async def sending_captcha(client: ClientSession):
    client.headers.clear()
    try:
        response = await client.get(f'http://rucaptcha.com/in.php?key={CAPTCHA_KEY}&method=userrecaptcha'
            '&googlekey=6Ldg5kQlAAAAABssf_tckVeMdsBruys7MCX9eyaD&pageurl=https://explorer.whitebit.network/testnet/faucet/')
        data = await response.text()
        if "ERROR_WRONG_USER_KEY" in data or "ERROR_ZERO_BALANCE" in data:
            logger.error(data)
            await asyncio.sleep(200)
            input()
            exit()
        elif 'ERROR' in data:
            logger.error(data)
            return await sending_captcha(client)
        return await solving_captcha(client, data[3:])
    except Exception as error:
        raise error


async def solving_captcha(client: ClientSession, id: str):
    client.headers.clear()
    logger.info('Solving captcha')
    while True:
        try:
            response = await client.get(f'http://rucaptcha.com/res.php?key={CAPTCHA_KEY}&action=get&id={id}')
            data = await response.text()
            if data in ['ERROR_CAPTCHA_UNSOLVABLE']:
                logger.error(data)
                return await sending_captcha(client)
            elif 'ERROR' in data:
                logger.error(data)
                await asyncio.sleep(1)
                return await sending_captcha(client)
            elif 'OK' in data:
                return data[3:]
        except Exception as error:
            raise error
        await asyncio.sleep(2)
    return await sending_captcha(client)


async def create_wallet():
    account = w3.eth.account.create()
    return account.address, account.key.hex()


async def claim_token():
    async with ClientSession(
        headers={
            'origin': 'https://explorer.whitebit.network',
            'user-agent': random_useragent()
        }
    ) as client:
        address, private_key = await create_wallet()
        while True:
            try:
                logger.info(f'Claim token | {address}')
                response = await client.post('https://explorer.whitebit.network/testnet/api/faucet/claim',
                                             json={
                                                 "address": address,
                                                 "token": await sending_captcha(client)
                                             })
                data = await response.json()
                data['hash']
            except:
                logger.error(data)
                continue
            else:
                break

    with open('wallets.txt', 'a') as file:
        file.write(f"{address}:{private_key}\n")
    logger.success(f'Claim successfully | {address}')


async def main():
    tasks = [asyncio.create_task(claim_token()) for _ in range(THREADS)]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    print("Bot WhiteBit testnet token claim @flamingoat")

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

    logger.success('END')
    input()