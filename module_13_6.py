from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kb.row(button1, button2)

kb2 = InlineKeyboardMarkup(resize_keyboard=True)
button3 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button4 = InlineKeyboardButton('Формулы расчёта', callback_data='formulas')
kb2.add(button3, button4)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb2)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer("https://www.calc.ru/Formula-Mifflinasan-Zheora.html")


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer("Введите свой возраст:")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(first=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(second=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(third=message.text)
    data = await state.get_data()
    result = float(10 * float(data['third']) + 6.25 * float(data['second']) - 5 * float(data['first']) + 5)
    await message.answer(f'Ваша норма калорий {result}')
    state.finish()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.\n'
                         'Что бы узнать Вашу суточную норму калорий,'
                         'введите или выберете "Рассчитать"', reply_markup=kb)


@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
