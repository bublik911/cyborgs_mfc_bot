from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import AddPlayer
from misc.utils import phone_parse
from keyboards.event_place import event_place_keyboard
from keyboards.admin_panel import admin_panel_keyboard
from DataBase.models_db import *
router = Router()


@router.message(
    F.text == "Добавить игрока"
)
async def create_player(message: Message, state: FSMContext):
    await message.answer("Введи имя игрока")
    await state.set_state(AddPlayer.name)


@router.message(
    AddPlayer.name
)
async def add_client_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите номер телефона клиента")
    await state.set_state(AddPlayer.phone)


@router.message(
    AddPlayer.phone
)
async def add_player_phone(message: Message, state: FSMContext):
    await state.update_data(phone=phone_parse(message.text))
    await message.answer("В заявке на какой турнир?",
                         reply_markup=event_place_keyboard())
    await state.set_state(AddPlayer.status)


@router.message(
    AddPlayer.status
)
async def commit(message: Message, state: FSMContext):
    await state.update_data(status=message.text)
    await message.answer("Игрок добавлен. Чтобы пользоваться ботом, ему нужно авторизоваться")
    data = await state.get_data()
    Player.create(name=data['name'],
                  phone_number=data['phone'],
                  status=0,
                  place=data['status'])
    await state.clear()
    await message.answer("Что-то еще?",
                         reply_markup=admin_panel_keyboard())