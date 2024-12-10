from aiogram import types, F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from time import time
from db import get_all_events, get_events, add_event, upd_event, upd_cur_event, get_quetion_number, get_event_id

quetions = [("Как называется мероприятие?", "name_of_event"), ("Напишите к каким категориям относятся мероприятие?", "category"), ("Где нужно будет собраться?", "place"), ("Когда?", "time"), ("Кого вы ищите?", "who"), ("Напишите подробнее для чего вам нужна компания?", "description")]

router = Router()

@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("Привет! Я помогу тебе найти компанию поблизости. Регистрируйся и оставляй заявку. Список доступных команд /help")

@router.message(Command("help"))
async def help_handler(msg: Message):
    await msg.answer(f"""
/my_events - список моих мероприятий\n/feed - лента мероприятий, к которым ты можешь присоединиться\n
/registration - регистрация нового пользователя\n
/map - мероприятия на карте\n
/new_event - добавить новое мероприятие""")

"extend"
STEP1_COLLAPSE_CB = "collapse"
STEP1_SETTINGS_CB = "settings"

@router.message(Command("my_events"))
async def my_events_handler(msg: Message):
    answer = get_events(msg.from_user.id)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Присоединиться!",
                             callback_data="join"),
    ]])
    if len(answer) == 0:
        await msg.answer("У тебя нет активных мероприятий.\n/new_event - добавить новое мероприятие")
    for i in answer:
        
        await msg.answer(f"{i[0]}\n\n Где? {i[1]}\n\n Категории {i[2]}\n\n Кого ищут? {i[3]}\n\n Когда? {i[4]}\n\n\n {i[5]}",
                         reply_markup=keyboard,)

@router.message(Command("feed"))
async def feed_handler(msg: Message):
    answer = get_all_events()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Присоединиться!",
                             callback_data="join"),
    ]])
    if len(answer) == 0:
        await msg.answer("Лента мероприятий пуста. Будь первым.\n/new_event - добавить новое мероприятие")
    for i in answer:
        await msg.answer(f"{i[0]}\n\n Где? {i[1]}\n\n Категории {i[2]}\n\n Кого ищут? {i[3]}\n\n Когда? {i[4]}\n\n\n {i[5]}",
                         reply_markup=keyboard,)

@router.callback_query(F.data == "join")
async def join(callback: CallbackQuery):
    await callback.message.edit_text(
        "TODO join"
    )


@router.message(Command("new_event"))
async def new_event_handler(msg: Message):
    event_id = add_event(msg.from_user.id)
    upd_cur_event(msg.from_user.id, event_id)
    await msg.answer(quetions[0][0])


@router.message(Command("registration"))
async def registration_handler(msg: Message):
    await msg.answer("Регистрация TODO")

@router.message(Command("my_profile"))
async def my_profile_handler(msg: Message):
    await msg.answer("Профиль TODO")

@router.message(Command("map"))
async def map_handler(msg: Message):
    await msg.answer("Карта TODO")

@router.message()
async def message_handler(msg: Message):
    quetion_number = get_quetion_number(msg.from_user.id)
    if 0 < quetion_number + 1 < len(quetions):
        upd_event(get_event_id(msg.from_user.id), quetions[quetion_number][1], msg.text)
        await msg.answer(quetions[quetion_number + 1][0])
        return
    elif quetion_number + 1 == len(quetions):
        upd_event(get_event_id(msg.from_user.id), quetions[quetion_number][1], msg.text)
        upd_event(get_event_id(msg.from_user.id), "status", "active")
        await msg.answer("Мероприятие успешно создано")
        return
    await msg.answer(f"TODO")

