from colorama import Fore as Cc
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import Config as Cfg, sys, keyboard, os, vk_api, colorama, json

class Command:
    def __init__(self, cmd, answer,attachment):
        self.cmd = cmd
        self.answer = answer
        self.attachment = attachment

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

def send_message(user_id, msg, attachments):
    vk_session.method('messages.send', {'user_id': user_id,
                                        'random_id': get_random_id(),
                                        'message': msg,
                                        'attachment': attachments,
                                        'keyboard': None})

def create_cmnt(owner_id, post_id, from_group, message, reply_to_comment):
    vk_session.method('wall.createComment', {'owner_id': owner_id,
                                             'post_id': post_id,
                                             'from_group': 180401388,
                                             'message': message,
                                             'reply_to_comment': reply_to_comment,
                                             'guid': get_random_id()})

with open("Commands.json", "r", encoding="utf-8") as read_file:
    data = json.load(read_file)
    print(Cc.LIGHTGREEN_EX + '\nДоступные команды:')
    for i in range(len(data["Commands"])):
        list_cmds.append(Command(data["Commands"][i]["cmd"], data["Commands"][i]["answer"], data["Commands"][i]["attachment"]))
        print(data["Commands"][i]["cmd"])
print()

def photo_attachemet(vk_session, attach_path):
    upload = vk_api.VkUpload(vk_session)
    photo = upload.photo_messages(photos=attach_path)[0]
    attachments = list()
    attachments.append('photo{}_{}'.format(photo['owner_id'], photo['id']))
    return attachments

def on_message(user_id, msg):
    sended = False
    msg_cmd = str(msg.lower())
    for i in range(len(list_cmds)):
        if list_cmds[i].cmd == msg_cmd and list_cmds[i].attachment == "":
            send_message(user_id, list_cmds[i].answer, None)
            sended = True
        elif list_cmds[i].cmd == msg_cmd and list_cmds[i].attachment != "":
            send_message(user_id, list_cmds[i].answer, photo_attachemet(vk_session, 'images/'+list_cmds[i].attachment))
            sended = True
    if sended == False:
        send_message(user_id, Cfg.wrong_text, None)



#region LongPoolListen
for event in longpoll.listen():

    if event.type == VkBotEventType.MESSAGE_NEW:
        print('Новое сообщение от: ', event.obj.from_id)
        print('Текст: ', event.obj.text)
        on_message(event.obj.from_id, event.obj.text)

    elif event.type == VkBotEventType.MESSAGE_REPLY:
        print('Сообщение для: ', event.obj.peer_id)
        print('Текст: ', event.obj.text)
        print()

    elif event.type == VkBotEventType.GROUP_JOIN:
        print(event.obj.user_id, ' - ', 'Вступил в группу!')
        send_message(event.obj.user_id, Cfg.welcome_text, None)
        print()

    elif event.type == VkBotEventType.GROUP_LEAVE:
        print(event.obj.user_id, ' - ', 'Покинул группу!')
        send_message(event.obj.user_id, Cfg.leaving_text, None)
        print('')
    elif event.type == VkBotEventType.WALL_REPLY_NEW:
        #owner_id, post_id, from_group, message, reply_to_comment
        print("\nНовый комментарий:\nID записи: ", event.obj.post_id, '\nID комментария: ', event.obj.id, '\nТекст комментария: ',event.obj.text, '\nID автора: ',event.obj.from_id)
        if event.obj.from_id != -180401388:
            create_cmnt(event.obj.post_owner_id, event.obj.post_id, event.obj.post_owner_id, 'Тестовы автоответ', event.obj.id)

#endregion
