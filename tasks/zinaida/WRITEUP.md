# Вопрос на миллион: Write-up

Мы обнаруживаем себя на импровизированном рабочем месте кассира продуктового магазина, где нам надо вводить штрих-коды продуктов. Сканера в интерфейсе нет, однако, как и на любой настоящей кассе, штрих-код можно ввести с клавиатуры.

Нам поставлена задача пробить товаров на миллион рублей. При средней цене товара 50–100 рублей это 10–20 тысяч действий — придётся автоматизировать.

Откроем вкладку _Network_ веб-инспектора своего браузера и посмотрим, что будет, если ввести верный штрих-код. Видим, что, помимо скачивания картинки товара и штрих-кода, делается POST-запрос на адрес вида `/token/next` с единственным параметром `barcode`. Ответ содержит заголовок `Set-Cookie` с чем-то непонятным, а также информацию для дисплея: цену и название последнего товара, очередной штрих-код и общую заработанную сумму. Если мы введём ещё один штрих-код, придёт аналогичный ответ, снова с непонятной кукой (уже другой).

Выходит, если хранить эту куку и всегда верно распознавать штрих-коды, как раз можно заработать миллион.

Воспользуемся Python-библиотекой _requests_. Можно создать объект класса `requests.Session`: он сам будет принимать куки и передавать их с последующими запросами. Поискав способы автоматически распознавать штрих-коды, найдём библиотеку [pyzbar](https://pypi.org/project/pyzbar/) и установим её.

Будем после каждого распознавания печатать приходящие с сервера данные — наверное, по достижении миллиона рублей там будет что-нибудь интересное.

```python
URL = "https://zinaida.s.2020.ugractf.ru/271655eb81c8b8b4/next"

import requests
import base64
import PIL.Image
import io
from pyzbar.pyzbar import decode

s = requests.Session()
barcode = ""
while True:
    data = s.post(URL, {"barcode": barcode}).json()
    print({k: v for k, v in data.items() if k != "next_barcode"})
    barcode = decode(PIL.Image.open(io.BytesIO(base64.b64decode(data["next_barcode"]))))[0].data
```

Запустим код. Зарабатывание миллиона займёт 15–20 минут.

```python
...
{'sum': 99968335, 'last': 'БЗМЖ ТВОРОГ ДЕТСКИЙ "КРЕПЫШ" 10% 100ГР (6+) СТАКАН', 'last_price': 2377, 'next_pic': 'https://grozd.ru/content/images/thumbs/5ecc1bb846c34676c8f9ff87_aj-lipton-ernyj-english-breakfast-25pak-50gr_280.jpeg'}
{'sum': 99975946, 'last': 'ЧАЙ "LIPTON" ЧЕРНЫЙ ENGLISH BREAKFAST 25ПАК 50ГР', 'last_price': 7611, 'next_pic': 'https://grozd.ru/content/images/thumbs/5ed9ca55d0ebd044562a7877_konf-vdohnovenie-okorehkrem-i-celfund-240gr_280.jpeg'}
{'sum': 100008092, 'last': 'ugra_must_be_funny_in_a_rich_man_s_world_9803aed1e485', 'last_price': 32146, 'next_pic': 'https://grozd.ru/content/images/thumbs/5ecfae6846c34676c88c30aa_luk-zelenyj-1t-rossi_280.jpeg'}
{'sum': 100012352, 'last': 'ugra_must_be_funny_in_a_rich_man_s_world_9803aed1e485', 'last_price': 4260, 'next_pic': 'https://grozd.ru/content/images/thumbs/5ece5b3d46c34676c899a751_kolbaski-iz-govdiny-evapii-300g-miratorg-lotok_280.jpeg'}
...
```

Вот и флаг. Наконец можно плюнуть на тирана-директора и уйти домой.

Флаг: **ugra_must_be_funny_in_a_rich_man_s_world_9803aed1e485**
