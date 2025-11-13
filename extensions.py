import requests
import json
from config import keys

class APIException(Exception):
    pass

class APIConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException('Перевод валюты саму в себя не имеет смысла.\nУбедитесь, что Вы ввели разные валюты.')
        
        try:
            quote_code = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {quote}')
        
        try:
            base_code = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количестов "{amount}"')
        
        api_text = f'https://v6.exchangerate-api.com/v6/20ad047e09d4313d3b7660f8/latest/{quote_code}'
        r = requests.get(api_text)
        conv_rates = json.loads(r.content)['conversion_rates']
        return amount*conv_rates[base_code]