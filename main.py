import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram import F
from config import TOKEN

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Добавятся позже
# Список упражнений
exercises = [
    "Метод фокальных объектов:\n"
    "1. Запиши свою идею/проблему (пример: подписка на вендинг)\n"
    "2. Запиши 3 случайных существительных (пример: дерево, мост, птица)\n"
    "3. К каждому существительному добавь по 3 прилагательных (пример: дерево зеленое, высокое, мощное)\n"
    "4. Соедини прилагательные со своей идеей (Подписка на вендинг при вступлении в сообщество 'зеленых', подписка на вендинг с высоким результатом по успеваемости, подписка на вендинг при посещении тренажерного зала)\n"
    "5. Запиши получившиеся варианты."
]

# Функция для создания клавиатуры
def get_keyboard(start_over=False):
    if start_over:
        # Если упражнения завершены, предлагаем кнопку "Начать сначала"
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Начать упражнения сначала")]
            ],
            resize_keyboard=True
        )
    else:
        # Если упражнения продолжаются, предлагаем кнопку "Следующее упражнение"
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Следующее упражнение")]
            ],
            resize_keyboard=True
        )

# Индекс текущего упражнения для каждого пользователя
user_exercise_index = {}

# Обработка команды /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    user_exercise_index[message.from_user.id] = 0
    await message.answer("Привет! Давай начнем наши упражнения.\n" + exercises[0], reply_markup=get_keyboard())

# Обработка кнопки "Следующее упражнение" или "Начать упражнения сначала"
@dp.message(F.text.in_({"Следующее упражнение", "Начать упражнения сначала"}))
async def handle_exercise(message: Message):
    user_id = message.from_user.id
    index = user_exercise_index.get(user_id, 0)

    if message.text == "Начать упражнения сначала":
        # Сбрасываем индекс для пользователя
        index = 0
        user_exercise_index[user_id] = index
        await message.answer("Начинаем сначала!\n" + exercises[index], reply_markup=get_keyboard())
    else:
        if index < len(exercises) - 1:
            # Увеличиваем индекс и отправляем следующее упражнение
            index += 1
            user_exercise_index[user_id] = index
            await message.answer(exercises[index], reply_markup=get_keyboard())
        else:
            # Если это последнее упражнение, предлагаем начать сначала
            await message.answer("Поздравляю! Вы завершили все упражнения.", reply_markup=get_keyboard(start_over=True))

# Запуск бота
if __name__ == '__main__':
    dp.run_polling(bot)
