from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import *
from logic import * 
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio


bot = Bot(API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

async def write_status(message: types.Message):
    await message.answer_chat_action(types.ChatActions.TYPING)  # Показывает, что бот печатает

keyboardNew = InlineKeyboardMarkup(row_width=2)
buttonDOXS = InlineKeyboardButton(text='Документация данного бота', callback_data='buttonDOXS')
button1 = InlineKeyboardButton(text='Назад', callback_data='button1')
keyboardNew.add(button1,buttonDOXS)


keyboard = InlineKeyboardMarkup(row_width=2)
button2 = InlineKeyboardButton(text='Код', callback_data='button2')
buttonG = InlineKeyboardButton(text='Генерация фото', callback_data='buttonG')
keyboard.add(button1,button2,buttonG)




@dp.message_handler(commands=['start', 'старт'])
async def handle_start_help(message: types.Message):
    await message.answer("""\
Привет, я бот для генерации фото!
отправь мне текст с запросом и я сделаю по нему фото °˖✧◝(⁰▿⁰)◜✧˖°
                 
для получения кода, который даст возможность создать аналогичного бота, нажми на кнопу 'Код''""", reply_markup=keyboard)

@dp.message_handler(content_types=['photo', 'document'])
async def handle_media(message: types.Message):
    await message.answer("Спасибо за фото/документ! я к сожалению еще не умею обрабатывать такой тип данных( вернитесь позже!")

@dp.message_handler(lambda message: message.text.lower() == 'спасибо')
async def thanks(message: types.Message):
    await message.answer("Пожалуйста! Рад помочь.")

class GenerateImage(StatesGroup):
    waiting_for_prompt = State()

@dp.callback_query_handler(lambda c: c.data == 'buttonG')
async def send_welcome(callback_query: types.CallbackQuery):
    await callback_query.message.reply("Отправь мне текстовый запрос, и я сгенерирую изображение.")
    await GenerateImage.waiting_for_prompt.set()

@dp.message_handler(state=GenerateImage.waiting_for_prompt)
async def generate_image(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    path = f"images/{user_id}.png"
    prompt = message.text

    # Отправляем статус "печатает"
    await bot.send_chat_action(message.chat.id, action=types.ChatActions.TYPING)

    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', API_KEY, SECRET_KEY)
    
    model_id = api.get_model()
    uuid = api.generate(prompt, model_id)
    images = api.check_generation(uuid)
    api.converter_to_png(images[0], path)
    
    with open(path, 'rb') as img:
        await bot.send_photo(message.chat.id, img, caption=f'Картинка по запросу:\n {prompt}')
    
    # Создаем InlineKeyboard и добавляем кнопку "Назад"
    extra_keyboard = InlineKeyboardMarkup(row_width=1)
    extra_keyboard.add(InlineKeyboardButton(text='Назад', callback_data='button1'))
    
    await bot.send_message(message.chat.id, "Теперь вы можете вернуться назад.", reply_markup=extra_keyboard)
    
    await state.finish()

@dp.callback_query_handler(lambda c: c.data in ['buttonDOXS'])
async def process_callback_button(callback_query: types.CallbackQuery):
    if callback_query.data == 'buttonDOXS':
         documentation_link = ""  # замените ссылку на фактическую документацию
         await bot.send_message(callback_query.from_user.id, f"Документация данного бота: {documentation_link}")

@dp.callback_query_handler(lambda c: c.data in ['button2'])
async def process_callback_button(callback_query: types.CallbackQuery):
    if callback_query.data == 'button2':
        extra_keyboard = InlineKeyboardMarkup(row_width=1)
        button3 = InlineKeyboardButton(text='Часть кода 1', callback_data='button3')
        button4 = InlineKeyboardButton(text='Часть кода 2', callback_data='button4')
        button5 = InlineKeyboardButton(text='Часть кода 3', callback_data='button5')
        button6 = InlineKeyboardButton(text='Назад', callback_data='button1')
        extra_keyboard.add(button3, button4, button5, button6)
        await bot.send_message(callback_query.from_user.id, """\
Для создания такого бота как этот тебе понадобиться сделать пару вещей.
1) создание бота в телеграм. для этого нужно перейти в еще один бот https://t.me/BotFather и по инструкции создать бота. не забудь где нибудь записать API токен своего бота (НИКОМУ НЕ СООБЩАЙ ЭТОТ ТОКЕН ВО ИЗБЕЖАНИИ КРАЖИ БОТА)
\
2) зарегистрируйся на сайте https://Fusionbrain.ai и запомни свой ключ и секретный ключ.
        
❕(не забудь что нельзя сообщать секретный ключ и токен бота кому попало, лучше всего удаляй его перед отправкой кода)❕

\
3) зайди в удобную среду разработки и начни творить             
                 
                 """, reply_markup=extra_keyboard)

    elif callback_query.data == 'button1':
        await bot.send_message(callback_query.from_user.id, """\
Вернулся назад!""", reply_markup=keyboard)
    await callback_query.answer()

@dp.callback_query_handler(lambda c: c.data in ['button3', 'button4', 'button5', 'button1'])
async def process_extra_button(callback_query: types.CallbackQuery):
    if callback_query.data == 'button3':
        code_snippet2 ="""\
сейчас я объясню как создать этого бота и как можно его создать! 
первый файл 1️⃣ :

bot.py 
                 
1. Обработка стартовых сообщений

<pre><code class="language-python"> 
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, '''\
Привет, я бот для генерации фото!
отправь мне текст с запросом и я сделаю по нему фото''')
</code></pre>

2. Обработка текстовых запросов и генерация изображения
# Получение текстового запроса от пользователя

<pre><code class="language-python">
propmt = message.text

# Получение идентификатора пользователя
user_id = message.from_user.id

# Генерация изображения на основе запроса
api = Text2ImageAPI('https://api-key.fusionbrain.ai/', API_KEY, SECRET_KEY)
model_id = api.get_model()
uuid = api.generate(promt, model_id)
images = api.check_generation(uuid)
bot.send_photo(message.chat.id, img, caption=f'картинка по запросу:\n {prompt}')
</code></pre>

Этот блок кода отвечает за получение текстового запроса пользователя и генерацию изображения на его основе.

* promt получает текстовый запрос пользователя из сообщения.
* user_id получает идентификатор пользователя, отправившего сообщение.
* api инициализирует объект API для взаимодействия с API Text2Image.
* model_id получает идентификатор модели, которую следует использовать для генерации изображения.
* uuid генерирует уникальный идентификатор для запроса на генерацию.
* images проверяет статус запроса на генерацию и извлекает сгенерированные изображения.
* api.converter_to_png() преобразует первое сгенерированное изображение в формат PNG и сохраняет его в папке images с именем, основанным на user_id.

3. Отправка изображения

# Отправка сгенерированного изображения пользователю

<pre><code class="language-python">
with open(f"images/{user_id}.png", 'rb') as img:
    bot.send_photo(message.chat.id, img, caption=f'картинка по запросу:\n {promt}')
</code></pre>

Этот блок кода отвечает за отправку сгенерированного изображения пользователю.

* with open() открывает сгенерированное изображение для чтения в двоичном формате.
* bot.send_photo() отправляет изображение пользователю вместе с подписью, содержащей исходный текстовый запрос.

4. Ответ на часто задаваемые вопросы (FAQ)

<pre><code class="language-python">
# Словарь с вопросами и ответами
questions_and_answers = {
    "Привет": "Приветствую!",
    "Как дела?": "Хорошо, спасибо",
    "Кто ты?": "Я чат-бот, созданный для помощи людям",
    "Какая погода сегодня?": "Я не знаю, я не могу получить доступ к информации о погоде",
    "Сколько времени?": "Я не знаю, я не могу получить доступ к информации о времени",
}

# Обработка сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # Проверка, есть ли вопрос пользователя в словаре
    if message.text in questions_and_answers:
        # Отправка назад ответа
        bot.reply_to(message, questions_and_answers[message.text])
    else:
        # Отправка сообщения по умолчанию
        bot.reply_to(message, "Извините, я не понимаю ваш вопрос")
</code></pre>

Этот блок кода отвечает за обработку сообщений от пользователя.

* questions_and_answers - это словарь, содержащий часто задаваемые вопросы (FAQ) и соответствующие ответы.
* @bot.message_handler() - это декоратор, который регистрирует функцию echo_all() для обработки всех входящих сообщений.
* Функция echo_all() проверяет, есть ли вопрос пользователя в словаре questions_and_answers. Если вопрос есть, функция отправляет соответствующий ответ. В противном случае функция отправляет сообщение по умолчанию, указывающее, что вопрос не понят.

5. Непрерывное отслеживание.
 - Бот работает в режиме бесконечного опроса, что означает, что он постоянно проверяет новые входящие сообщения и реагирует на них.
<pre><code class="language-python">
bot.infinity_polling()
</code></pre>
                 
"""

        await bot.send_message(callback_query.from_user.id, code_snippet2, parse_mode="HTML")
        await asyncio.sleep(1)
        await bot.send_message(callback_query.from_user.id, """\
Выберете дальнейшее действие""", reply_markup=keyboardNew)
    elif callback_query.data == 'button4':
        code_snippet1 = """\
второй файл 2️⃣ :
                 
logic.py

1. Инициализация объекта API

<pre><code class="language-python">api = Text2ImageAPI('https://api-key.fusionbrain.ai/', API_KEY, SECRET_KEY)</code></pre>

Здесь мы создаем объект Text2ImageAPI и передаем ему URL-адрес API, ключ API и секретный ключ.

2. Получение идентификатора модели

<pre><code class="language-python">model_id = api.get_model()</code></pre>

Этот метод извлекает идентификатор модели, которая будет использоваться для генерации изображений. В данном случае мы предполагаем, что в списке моделей всегда будет хотя бы одна модель, и выбираем первую модель.

3. Генерация изображения

<pre><code class="language-python">uuid = api.generate("кот", model_id)</code></pre>


Этот метод отправляет запрос API для генерации изображения на основе текстового описания "кот". Он возвращает идентификатор запроса (UUID), который можно использовать для отслеживания состояния генерации.

4. Проверка состояния генерации

<pre><code class="language-python">images = api.check_generation(uuid)</code></pre>


Этот метод опрашивает API, пока не будет завершена генерация изображения. Он возвращает список URL-адресов сгенерированных изображений.

5. Преобразование в PNG

<pre><code class="language-python">api.converter_to_png(images[0], "user_id.png")</code></pre>


Этот метод преобразует первое сгенерированное изображение в объект Image и сохраняет его в файле user_id.png.

Полный пример:
<pre><code class="language-python">
import json
import time
from config import *
import requests
import base64
from PIL import Image
from io import BytesIO

class Text2ImageAPI:

    def init(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)

    def converter_to_png(self, base64_string, path):
        decoded_data = base64.b64decode(base64_string)
        image = Image.open(BytesIO(decoded_data))
        image.save(path)


if __name__ == 'main__':
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', API_KEY, SECRET_KEY)
    model_id = api.get_model()
    uuid = api.generate("кот", model_id)
    images = api.check_generation(uuid)
    api.converter_to_png(images[0], "user_id.png")
</code></pre>

Запуск кода:

Чтобы запустить этот код, вы должны заменить API_KEY и SECRET_KEY своими собственными ключами API и секретным ключом и сохранить файл как text2image.py. Затем вы можете запустить код из командной строки:


<pre><code class="language-python">python text2image.py</code></pre>

После этого в текущей директории будет создан файл user_id.png с изображением кота.

"""
        await bot.send_message(callback_query.from_user.id, code_snippet1, parse_mode="HTML")
        await asyncio.sleep(1)
        await bot.send_message(callback_query.from_user.id, """\
Выберете дальнейшее действие""", reply_markup=keyboardNew)
    
    elif callback_query.data == 'button5':
        code_snippet = """
третий файл 3️⃣ :

config.py

этот код представляет собой создание 3-х переменных:
<pre><code class="language-python">
API_KEY='ХХХХ'
SECRET_KEY='ХХХХ'
API_TOKEN = 'ХХХХ'
</code></pre>
вместо данных надо вставить ключ и секретный ключ от ии и api своего бота
"""

        await bot.send_message(callback_query.from_user.id, code_snippet, parse_mode="HTML")

        await asyncio.sleep(1)
        await bot.send_message(callback_query.from_user.id, """\
Выберете дальнейшее действие""", reply_markup=keyboardNew)
        

    elif callback_query.data == 'button1':
        await bot.send_message(callback_query.from_user.id, """\
Вернулся назад!""", reply_markup=keyboard)





if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



