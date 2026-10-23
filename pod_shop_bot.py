# language: Python, file: pod_shop_bot.py
import asyncio
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ================= НАСТРОЙКА =================
BOT_TOKEN = "8663502210:AAEzmiWaODI8yhryRdl6e6FZ3D_iZtqwyoU"
ADMIN_ID = 8891089617 
YOUR_USERNAME = "L0veSmokIng" 
CARD_NUMBER = "4441 1144 3151 1102"
# =============================================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ============ ТОВАРЫ ============
PRODUCTS = {
    "xros": [
        {"id": 1, "name": "Vaporesso Xros Mini Fresh Edition (Original)", "price": 500, "market": 700},
        {"id": 2, "name": "Vaporesso Xros 3 Mini", "price": 550, "market": 750},
        {"id": 3, "name": "Vaporesso Xros 5 Mini", "price": 600, "market": 800},
        {"id": 4, "name": "Vaporesso Xros 3", "price": 525, "market": 725},
        {"id": 5, "name": "Vaporesso Xros 6 (NEW)", "price": 700, "market": 900}, 
        {"id": 6, "name": "GeekVape Sonder U", "price": 250, "market": 450},
        {"id": 7, "name": "Lost Vape Ursa Nano", "price": 440, "market": 640},
        {"id": 8, "name": "Univapo Kipo", "price": 440, "market": 640},
        {"id": 9, "name": "Voopoo Vinci Q", "price": 240, "market": 440},
    ],
    "cartridges": [
        {"id": 10, "name": "Картридж XROS (Mini/Nano/2/3/4/5/6) 1 шт", "price": 150, "market": 350},
        {"id": 11, "name": "Картридж Univapo KIPO 1 шт", "price": 130, "market": 330},
        {"id": 12, "name": "Картридж Geekvape U 1 шт", "price": 115, "market": 315},
        {"id": 13, "name": "Картридж Lost Vape Ursa Nano 1 шт", "price": 110, "market": 310},
        {"id": 14, "name": "Картридж Oxva Xlim V2 1 шт", "price": 120, "market": 320},
        {"id": 15, "name": "Картридж ZQ Xtal 1 шт", "price": 120, "market": 320},
        {"id": 16, "name": "Картридж Vaporesso Renova Zero POD S 2 1 шт", "price": 110, "market": 310},
        {"id": 17, "name": "Картридж Voopoo Vmate V2/V3 Top Fill 1 шт", "price": 130, "market": 330},
    ],
    "liquids": [
        {"id": 18, "name": "Набір Chaser Mix 30мл - М'ятний Орбіт", "price": 250, "market": 350},
        {"id": 19, "name": "Набір Chaser for Pods 30мл - Вишня Ментол", "price": 250, "market": 350},
        {"id": 20, "name": "Набір Chaser for Pods 30мл - Кавун", "price": 250, "market": 350},
        {"id": 21, "name": "Набір Chaser for Pods 30мл - Чорниця Ментол", "price": 250, "market": 350},
        {"id": 22, "name": "Набір Chaser Black 30мл - Energy Grape", "price": 250, "market": 350},
        {"id": 23, "name": "Набір Chaser Black 30мл - Forest Mix", "price": 250, "market": 350},
        {"id": 24, "name": "Набір Chaser Black 30мл - Blackberry Sour Raspberry", "price": 250, "market": 350},
        {"id": 25, "name": "Набір Chaser Black 30мл - Triple Sour Apple", "price": 250, "market": 350},
        {"id": 26, "name": "Набір Chaser Black 30мл - Watermelon Lemon", "price": 250, "market": 350},
        {"id": 27, "name": "Набір Chaser LUX 30мл - Tropic Punch", "price": 250, "market": 350},
        {"id": 28, "name": "Набір Chaser for Pods 30мл - Персик", "price": 250, "market": 350},
        {"id": 29, "name": "Набір Chaser for Pods 30мл - Кавун Ментол", "price": 250, "market": 350},
        {"id": 30, "name": "Набір Chaser for Pods 10мл - Чорниця", "price": 50, "market": 150},
        {"id": 31, "name": "Набір Chaser for Pods 10мл - Малина", "price": 50, "market": 150},
        {"id": 32, "name": "Набір Chaser for Pods 10мл - М'ята", "price": 50, "market": 150},
        {"id": 33, "name": "Набір Chaser for Pods 10мл - Ягоди", "price": 50, "market": 150},
        {"id": 34, "name": "Набір Chaser for Pods 10мл - Банан", "price": 50, "market": 150},
        {"id": 35, "name": "Набір Chaser for Pods 10мл - Вишня", "price": 50, "market": 150},
        {"id": 36, "name": "Набір Chaser for Pods 10мл - Блакитна Малина", "price": 50, "market": 150},
    ]
}

carts = {}
active_chats = {} 

# ============ СОСТОЯНИЯ ============
class OrderState(StatesGroup):
    waiting_address = State()

class SupportState(StatesGroup):
    waiting_message = State()

# ============ СТАРТ ============
@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    if user_id not in carts:
        carts[user_id] = []
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Под-системы", callback_data="cat_xros")],
        [InlineKeyboardButton(text="💨 Картриджи", callback_data="cat_cartridges")],
        [InlineKeyboardButton(text="🧪 Жидкости", callback_data="cat_liquids")],
        [InlineKeyboardButton(text="🛍 Корзина", callback_data="show_cart")],
        [InlineKeyboardButton(text="📞 Связаться с нами", callback_data="contact")]
    ])
    
    await message.answer(
        "👋 Привет! Это магазин POD-систем.\n"
        "У нас цены ниже рынка на 200 грн (устройства/картриджи) и на 100 грн (жидкости).\n\n"
        "Выбери категорию:",
        reply_markup=kb
    )

# ============ КАТАЛОГ ============
async def show_category(callback: types.CallbackQuery, category: str, title: str):
    items = PRODUCTS.get(category, [])
    if not items:
        await callback.answer("В этой категории пока нет товаров.")
        return
    
    text = f"📋 {title}:\n\n"
    for item in items:
        diff = item["market"] - item["price"]
        text += f"{item['id']}. {item['name']} — {item['price']} грн (дешевле на {diff} грн)\n"
    
    text += "\nНапиши номер товара, чтобы добавить его в корзину."
    await callback.message.edit_text(text)
    await callback.answer()

@dp.callback_query(F.data == "cat_xros")
async def cat_xros(callback: types.CallbackQuery):
    await show_category(callback, "xros", "Под-системы")

@dp.callback_query(F.data == "cat_cartridges")
async def cat_cartridges(callback: types.CallbackQuery):
    await show_category(callback, "cartridges", "Картриджи")

@dp.callback_query(F.data == "cat_liquids")
async def cat_liquids(callback: types.CallbackQuery):
    await show_category(callback, "liquids", "Жидкости")

# ============ ДОБАВЛЕНИЕ В КОРЗИНУ ============
@dp.message(F.text.regexp(r'^\d+$'))
async def add_to_cart(message: types.Message):
    user_id = message.from_user.id
    if user_id not in carts:
        carts[user_id] = []
    
    product_id = int(message.text)
    for category in PRODUCTS.values():
        for item in category:
            if item["id"] == product_id:
                carts[user_id].append(item)
                await message.answer(f"✅ {item['name']} добавлен в корзину.")
                return
    await message.answer("Товар с таким номером не найден.")

# ============ КОРЗИНА ============
@dp.callback_query(F.data == "show_cart")
async def show_cart(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    cart = carts.get(user_id, [])
    if not cart:
        await callback.answer("Корзина пуста.", show_alert=True)
        return
    
    total = sum(item["price"] for item in cart)
    text = "🛒 Твоя корзина:\n\n"
    for item in cart:
        text += f"- {item['name']} — {item['price']} грн\n"
    text += f"\n💰 Итого: {total} грн"
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Оформить заказ", callback_data="checkout")]
    ])
    await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()

# ============ ОФОРМЛЕНИЕ ============
@dp.callback_query(F.data == "checkout")
async def checkout(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    cart = carts.get(user_id, [])
    if not cart:
        await callback.answer("Корзина пуста.", show_alert=True)
        return
    
    await callback.message.edit_text("Введи адрес доставки (город, отделение Новой Почты):")
    await state.set_state(OrderState.waiting_address)
    await callback.answer()

@dp.message(OrderState.waiting_address)
async def finish_order(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    cart = carts.get(user_id, [])
    if not cart:
        await message.answer("Корзина пуста.")
        await state.clear()
        return
    
    total = sum(item["price"] for item in cart)
    items_text = "\n".join([f"- {item['name']} — {item['price']} грн" for item in cart])
    
    await message.answer(
        f"✅ Заказ сформирован!\n\n"
        f"{items_text}\n\n"
        f"💰 Итого: {total} грн\n\n"
        f"Переведи сумму на карту:\n"
        f"<code>{CARD_NUMBER}</code>\n\n"
        f"После перевода отправь чек (скриншот) сюда же.\n"
        f"Адрес доставки: {message.text}",
        parse_mode="HTML"
    )
    
    username = message.from_user.username or message.from_user.id
    await bot.send_message(
        ADMIN_ID,
        f"📦 Новый заказ от @{username}\n"
        f"{items_text}\n"
        f"💰 Итого: {total} грн\n"
        f"📍 Адрес: {message.text}\n\n"
        f"Ожидаем перевод на карту {CARD_NUMBER}"
    )
    
    carts[user_id] = []
    await state.clear()

# ============ СВЯЗАТЬСЯ С НАМИ ============
@dp.callback_query(F.data == "contact")
async def contact(callback: types.CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📩 Написать в личку", url=f"https://t.me/{YOUR_USERNAME}")],
        [InlineKeyboardButton(text="💬 Чат в боте", callback_data="chat_in_bot")]
    ])
    await callback.message.edit_text(
        "Выбери способ связи:\n\n"
        "1. Написать напрямую в личные сообщения.\n"
        "2. Написать в боте (ответ придёт сюда же).",
        reply_markup=kb
    )
    await callback.answer()

@dp.callback_query(F.data == "chat_in_bot")
async def chat_in_bot(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    active_chats[user_id] = True
    await callback.message.edit_text("Напиши своё сообщение, и я передам его администратору. Для отмены напиши /stop.")
    await state.set_state(SupportState.waiting_message)
    await callback.answer()

@dp.message(SupportState.waiting_message)
async def send_support_message(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if not active_chats.get(user_id):
        return
    
    username = message.from_user.username or message.from_user.id
    await bot.send_message(
        ADMIN_ID,
        f"💬 Сообщение от @{username} (ID: {user_id}):\n\n{message.text}\n\n"
        f"Чтобы ответить, напиши: /reply {user_id} Твой ответ"
    )
    await message.answer("✅ Сообщение отправлено администратору. Он ответит тебе здесь.")
    await state.clear()

# ============ ОТВЕТ АДМИНА ============
@dp.message(Command("reply"))
async def admin_reply(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    
    parts = message.text.split(' ', 2)
    if len(parts) < 3:
        await message.answer("Формат: /reply <user_id> <текст>")
        return
    
    target_id = int(parts[1])
    reply_text = parts[2]
    
    try:
        await bot.send_message(target_id, f"💬 Ответ администратора:\n\n{reply_text}")
        await message.answer(f"✅ Ответ отправлен пользователю {target_id}")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")

@dp.message(Command("stop"))
async def stop_chat(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in active_chats:
        del active_chats[user_id]
    await message.answer("Чат с администратором завершён.")
    await state.clear()

# ============ ВЕБ-СЕРВЕР ДЛЯ RENDER ============
async def web_server():
    async def handle(request):
        return web.Response(text="Bot is running!")

    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Render сам назначает порт через переменную окружения PORT
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Web server started on port {port}")

# ============ ЗАПУСК ============
async def main():
    # Запускаем веб-сервер параллельно с ботом
    asyncio.create_task(web_server())
    print("Бот запущен и слушает сообщения...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
