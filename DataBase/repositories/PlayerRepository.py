from DataBase.models.PlayerModel import Player

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from typing import NoReturn


async def create_player(state: FSMContext) -> NoReturn:
    data = await state.get_data()
    Player.create(name=data['name'],
                  phone_number=data['phone'],
                  status=0,
                  place=data['status'])
    await state.clear()


def count_player_by_phone_number(message: Message) -> int:
    return Player.select().where(Player.phone_number == message.contact.phone_number[-10:]).count()


def update_player_chat_id_by_phone_number(message: Message) -> NoReturn:
    Player.update(chat_id=message.chat.id).where(Player.phone_number == message.contact.phone_number[-10:])


def get_player_status_by_phone_number(message: Message) -> int:
    return Player.get(Player.phone_number == message.contact.phone_number[-10:]).status


def get_player_id_by_chat_id(chat_id: int) -> int:
    return Player.get(Player.chat_id == chat_id).id


def get_player_name_by_id(player_id: int) -> str:
    return Player.get(Player.id == player_id).name


def get_player_by_place(place: str) -> [Player]:
    return Player.select().where((Player.place == place) & (Player.chat_id.is_null(False)))