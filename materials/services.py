from forex_python.converter import CurrencyRates


def convert_currencies(rub_price):
    """Конвертирует рубли в доллар"""
    c = CurrencyRates()
    usd_rate = c.get_rate('USD', 'RUB')
    usd_price = rub_price // usd_rate
    return int(usd_price)
