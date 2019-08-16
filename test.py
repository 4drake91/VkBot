from colorama import Fore as Cc
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import Config as Cfg, sys, keyboard, os, vk_api, colorama, json

list_cmds = []
colorama.init(autoreset=True)
vk_session = vk_api
print(Cc.LIGHTMAGENTA_EX + '')
print(Cc.LIGHTBLUE_EX + 'Press Ctrl+1 to exit')
keyboard.add_hotkey('Ctrl + 1', lambda : os.abort())

try:
    vk_session = vk_api.VkApi(token=Cfg.token)
    longpoll = VkBotLongPoll(vk_session, Cfg.group_id)
except Exception as e:
    print(e)
    print(Cc.LIGHTBLUE_EX + 'Error! Press Ctrl+1 to exit')
    keyboard.wait('Enter')
else:
    print(Cc.GREEN + 'Успешный вход!')

def wallPost (owner_id, from_group, message):
    vk_session.method('wall.post', {'owner_id': owner_id,
                                             'from_group': from_group,
                                             'message': message,
                                             'guid': get_random_id()})

wallPost(-180401388, 1, "тест")
