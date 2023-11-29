import json

import requests

from conf import keys


class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

            # quote_ticker, base_ticker = keys[quote], keys[base]
        try:
            base_l = base.lower()
            base_ticker = keys[base_l]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')
        try:
            quote_l = quote.lower()
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')
        try:
            amount = float(amount)

        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')
        if float(amount) < 0:
            raise APIException(f'Введите число больше 0, ваше число меньше: {amount}.')

        if quote == base:
            raise APIException(f'Введите различные валюты: {base}.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        total_base *= float(amount)
        return total_base
