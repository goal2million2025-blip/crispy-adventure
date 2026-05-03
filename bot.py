"""
Telegram-бот для @creator_bek1 — digital-специалист
Запуск: pip install aiogram==3.x && python bot.py
"""

import asyncio
import logging
from pathlib import Path
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton, FSInputFile
)
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# ─── НАСТРОЙКИ ───────────────────────────────────────────────
OWNER_USERNAME = "@creator_bek1"    # ← ник для перенаправления клиентов
START_PHOTO_PATH = Path(__file__).resolve().with_name(
    "WhatsApp Image 2026-05-03 at 10.52.49.jpeg"
)
TOKEN_ENV_FILES = [
    Path(__file__).resolve().with_name(".env"),
    Path(r"C:\Users\User\.vscode\telegram-bot-render\.env"),
]

logging.basicConfig(level=logging.INFO)
dp = Dispatcher(storage=MemoryStorage())


def load_token_from_env_file() -> str:
    for env_file in TOKEN_ENV_FILES:
        if not env_file.exists():
            continue

        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip().lstrip("\ufeff")
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            if key.strip() == "BOT_TOKEN":
                return value.strip().strip('"').strip("'")

    return ""


def get_bot_token() -> str:
    token = os.getenv("BOT_TOKEN", "").strip()
    if token:
        return token

    token = load_token_from_env_file()
    if token:
        return token

    raise RuntimeError("BOT_TOKEN not found in environment or .env file")


# ─── СОСТОЯНИЯ (для сценария заказа) ─────────────────────────
class OrderStates(StatesGroup):
    waiting_service = State()
    waiting_style   = State()
    waiting_example = State()


# ─── ГЛАВНОЕ МЕНЮ ────────────────────────────────────────────
def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🖼 Работы"),      KeyboardButton(text="💰 Прайс")],
            [KeyboardButton(text="💬 Отзывы"),      KeyboardButton(text="📲 Заказать")],
            [KeyboardButton(text="❓ FAQ")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Выбери раздел 👇"
    )


# ─── /start ──────────────────────────────────────────────────
@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    photo = FSInputFile(str(START_PHOTO_PATH))
    caption = (
        "👋 Привет! Это Я тот самой Ai-inzhenner\n"
        "Меня зовут Бекнур можете звать crash beka😊\n\n"
        "ВОТ МЕНЮ ЧТО ВЫ ВЫБИРАЕТЕ\n"
        "🎨 Уникальные изображения с помощью ИИ\n"
        "🧑‍💼 Портреты / аватары\n"
        "📱 Дизайн для Instagram и Telegram\n"
        "🌐 Создание сайтов под ключ\n"
        "🤖 Разработка Telegram-ботов\n"
        "⚡ Арты в индивидуальном стиле"
    )
    await message.answer_photo(
        photo=photo,
        caption=caption,
        reply_markup=main_menu()
    )


# ─── 🖼 РАБОТЫ ───────────────────────────────────────────────
AVATAR_PHOTOS = [
    "BQACAgIAAxkBAAFIor9p9vTii78a-YqfdHywIv0Ml7WbKwACvpIAAgRwuEvlTxfm-xrIcjsE",
]

@dp.message(F.text == "🖼 Работы")
async def section_portfolio(message: Message):
    await message.answer(
        "🖼 <b>Портфолио</b>\n\n"
        "Смотри примеры моих работ 👇",
        parse_mode="HTML"
    )

    # Аватары
    await message.answer("🧑‍🎨 <b>Аватары и портреты</b>", parse_mode="HTML")
    for file_id in AVATAR_PHOTOS:
        await message.answer_document(document=file_id)

    # Остальные разделы (заглушки)
    await message.answer(
        "🎨 <b>ИИ-арты</b>\n"
        "   └ [скоро будут примеры]\n\n"
        "📐 <b>Баннеры и дизайн</b>\n"
        "   └ [скоро будут примеры]\n\n"
        "🌐 <b>Сайты</b>\n"
        "   └ [скоро будут примеры]\n\n"
        "🤖 <b>Telegram-боты</b>\n"
        "   └ [скоро будут примеры]\n\n"
        "Понравилось? 👇 Оформи заказ!",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📲 Заказать", callback_data="start_order")]
        ])
    )


# ─── 💰 ПРАЙС ────────────────────────────────────────────────
@dp.message(F.text == "💰 Прайс")
async def section_price(message: Message):
    text = (
        "💰 <b>Прайс-лист</b>\n\n"
        "┌─────────────────────────────\n"
        "│ 🧑‍🎨 Аватар            — <b>2 000 ₸</b>\n"
        "│ 🎨 ИИ-арт             — <b>3 000 ₸</b>\n"
        "│ 📐 Баннер             — <b>5 000 ₸</b>\n"
        "│ 🌐 Сайт               — <b>20 000 ₸</b>\n"
        "│ 🤖 Telegram-бот      — <b>10 000 ₸</b>\n"
        "└─────────────────────────────\n\n"
        "✅ Срок: 1–2 рабочих дня\n"
        "✅ Правки включены\n"
        "✅ Предоплата обсуждается\n\n"
        "Готов сделать заказ? 👇"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📲 Заказать", callback_data="start_order")]
    ])
    await message.answer(text, parse_mode="HTML", reply_markup=keyboard)


# ─── 💬 ОТЗЫВЫ ───────────────────────────────────────────────
@dp.message(F.text == "💬 Отзывы")
async def section_reviews(message: Message):
    text = (
        "💬 <b>Отзывы клиентов</b>\n\n"
        "⭐⭐⭐⭐⭐\n"
        "🗣 <b>Клиент 1</b>\n"
        "«Сделал аватар — просто огонь! Быстро, красиво, всё как просил. "
        "Буду заказывать снова!»\n"
        "[здесь будет скриншот отзыва]\n\n"
        "⭐⭐⭐⭐⭐\n"
        "🗣 <b>Клиент 2</b>\n"
        "«Заказал баннер для Instagram — результат превзошёл ожидания. "
        "Очень доволен, рекомендую!»\n"
        "[здесь будет скриншот отзыва]\n\n"
        "⭐⭐⭐⭐⭐\n"
        "🗣 <b>Клиент 3</b>\n"
        "«Сделали сайт за 2 дня. Всё чётко, профессионально, с правками. "
        "Спасибо!»\n"
        "[здесь будет скриншот отзыва]\n\n"
        "📌 <i>Хочешь так же? Оформляй заказ! 👇</i>"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📲 Заказать", callback_data="start_order")]
    ])
    await message.answer(text, parse_mode="HTML", reply_markup=keyboard)


# ─── ❓ FAQ ───────────────────────────────────────────────────
@dp.message(F.text == "❓ FAQ")
async def section_faq(message: Message):
    text = (
        "❓ <b>Часто задаваемые вопросы</b>\n\n"
        "⏱ <b>Сколько времени занимает выполнение?</b>\n"
        "   └ Обычно 1–2 рабочих дня.\n\n"
        "✏️ <b>Можно ли вносить правки?</b>\n"
        "   └ Да, правки включены в стоимость.\n\n"
        "💳 <b>Нужна ли предоплата?</b>\n"
        "   └ Условия оплаты обсуждаются индивидуально.\n\n"
        "🖼 <b>Какой формат я получу?</b>\n"
        "   └ PNG, JPG, PDF — в зависимости от заказа.\n\n"
        "📩 <b>Как связаться с мастером?</b>\n"
        f"   └ Напиши напрямую: {OWNER_USERNAME}\n\n"
        "Остались вопросы? Просто напиши — отвечу быстро 😊"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📲 Заказать", callback_data="start_order")]
    ])
    await message.answer(text, parse_mode="HTML", reply_markup=keyboard)


# ─── 📲 ЗАКАЗАТЬ (кнопка меню) ───────────────────────────────
@dp.message(F.text == "📲 Заказать")
async def section_order(message: Message, state: FSMContext):
    await start_order_flow(message, state)


# ─── ЗАКАЗАТЬ (inline-кнопка) ────────────────────────────────
@dp.callback_query(F.data == "start_order")
async def cb_start_order(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await start_order_flow(callback.message, state)


# ─── ШАГ 1: Что нужно? ───────────────────────────────────────
async def start_order_flow(message: Message, state: FSMContext):
    await state.set_state(OrderStates.waiting_service)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧑‍🎨 Аватар",        callback_data="svc_avatar")],
        [InlineKeyboardButton(text="🎨 ИИ-арт",          callback_data="svc_art")],
        [InlineKeyboardButton(text="📐 Баннер / Дизайн", callback_data="svc_banner")],
        [InlineKeyboardButton(text="🌐 Сайт",            callback_data="svc_site")],
        [InlineKeyboardButton(text="🤖 Telegram-бот",    callback_data="svc_bot")],
    ])
    await message.answer(
        "📲 <b>Оформление заказа</b>\n\n"
        "<b>Шаг 1 из 3</b> — Что тебе нужно?\n"
        "Выбери услугу 👇",
        parse_mode="HTML",
        reply_markup=keyboard
    )


SERVICE_NAMES = {
    "svc_avatar": "🧑‍🎨 Аватар",
    "svc_art":    "🎨 ИИ-арт",
    "svc_banner": "📐 Баннер / Дизайн",
    "svc_site":   "🌐 Сайт",
    "svc_bot":    "🤖 Telegram-бот",
}


# ─── ШАГ 2: Стиль ────────────────────────────────────────────
@dp.callback_query(OrderStates.waiting_service, F.data.in_(SERVICE_NAMES))
async def order_step2(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    service = SERVICE_NAMES[callback.data]
    await state.update_data(service=service)
    await state.set_state(OrderStates.waiting_style)
    await callback.message.answer(
        f"✅ Выбрано: <b>{service}</b>\n\n"
        "<b>Шаг 2 из 3</b> — Какой стиль тебе нравится?\n\n"
        "Например: реалистичный, аниме, минимализм, тёмный, яркий, деловой...\n"
        "Или просто опиши своё пожелание 👇",
        parse_mode="HTML"
    )


# ─── ШАГ 3: Фото/пример ──────────────────────────────────────
@dp.message(OrderStates.waiting_style)
async def order_step3(message: Message, state: FSMContext):
    await state.update_data(style=message.text)
    await state.set_state(OrderStates.waiting_example)
    await message.answer(
        "<b>Шаг 3 из 3</b> — Есть ли у тебя фото или пример?\n\n"
        "📎 Если есть — отправь файл/изображение прямо сюда.\n"
        "Если нет — напиши <b>«нет»</b> и я всё равно сделаю круто 😊",
        parse_mode="HTML"
    )


# ─── ФИНАЛ: редирект к мастеру ───────────────────────────────
@dp.message(OrderStates.waiting_example)
async def order_final(message: Message, state: FSMContext):
    data = await state.get_data()
    service = data.get("service", "—")
    style   = data.get("style", "—")

    # Определяем пример
    if message.photo or message.document:
        example = "✅ Файл/фото получен"
    else:
        example = message.text or "—"

    await state.clear()

    summary = (
        "✅ <b>Отлично! Вот что мы собрали:</b>\n\n"
        f"📌 Услуга: <b>{service}</b>\n"
        f"🎨 Стиль: <b>{style}</b>\n"
        f"🖼 Пример: <b>{example}</b>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        f"Теперь напиши мастеру напрямую — <b>{OWNER_USERNAME}</b>\n"
        "и скинь эти данные. Отвечу быстро! ⚡"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=f"✉️ Написать {OWNER_USERNAME}",
            url=f"https://t.me/{OWNER_USERNAME.lstrip('@')}"
        )]
    ])
    await message.answer(summary, parse_mode="HTML", reply_markup=keyboard)


# ─── ЗАПУСК ──────────────────────────────────────────────────
async def main():
    bot = Bot(token=get_bot_token())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
