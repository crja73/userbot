from pyrogram import Client
import asyncio
import os


api_id = 111
api_hash = ""

app = Client(
    "account",
    api_id=api_id,
    api_hash=api_hash
)

logined = False

print("Происходит запуск программы. Пожалуйста, подождите...")
chat_list = []  # [chat_id, chat_title, chat_num]
phrases = []


app.start()


def get_phrases():
    path = "./txt_files"
    files = os.listdir(path=path)

    result = []

    for file in files:

        with open(path + "/" + file, "r", encoding='utf-8') as file:
            data = list(map(lambda string: string.strip().lower() if string.strip() != "" else None, file.readlines()))
            result.append(data)

    return result


async def get_dialogs():
    global chat_list, phrases
    index = 1

    async for dialog in app.get_dialogs():

        if str(dialog.chat.type) != "ChatType.PRIVATE" and str(dialog.chat.type) != "ChatType.BOT":
            chat_name, chat_id = dialog.chat.title or dialog.chat.first_name, dialog.chat.id

            if chat_name is not None:
                chat_list.append([chat_id, chat_name.lower(), index])
                index += 1


if not logined:

    tracked_chats_ids = set()
    tracked_chats_titles = set()

    

    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_dialogs())




    c = "\n".join([str(x[2]) + ") " + x[1] for x in chat_list])
    print(c)

    numbers = input("\nДля выбора отслеживаемых чатов введите их номера через запятую. Пример: 1, 2, 3, 4, 5, "
                    "... (Обязательно пробел после запятой) ---> ")
    numbers = numbers.split(", ")

    try:
        for digit in numbers:
            tracked_chats_ids.add(chat_list[int(digit) - 1][0])
            tracked_chats_titles.add(chat_list[int(digit) - 1][1])

    except Exception:
        print("Номера групп были неправильно введены. Перезапустите программу и повторите попытку\n")
        input('Press ENTER to exit')
        exit(0)

    print("\nСписок отслеживаемых чатов:")
    print(" | ".join(list(tracked_chats_titles)))

    # phrase4user = input("\nВведите фразу, которая будет отправлена пользователю -> ")
    # print("Принято!\n")

    # key_phrases = []
    # print('Ниже введите ключевые слова/фразы для поиска. Для окончания ввода напишите "stop/стоп"')

    # while True:
    #     phrase = input("Введите фразу --> ")
    #     if phrase == "stop" or phrase == "стоп":
    #         break

    #     key_phrases.append(phrase.lower())
    try:
        phrases = get_phrases()
        print("\nПрограмма работает и сканирует чаты...")
        logined = True

    except Exception:
        input("Произошла ошибка чтения фраз из файлов. НАЖМИТЕ ENTER для выхода")
        exit(0)

app.stop()


@app.on_message()
async def check_msg(client, message):
    for phrase in phrases:
        try:
            key_phrases, phrase4user = phrase[1:], phrase[0]

            if (message.chat.id in tracked_chats_ids) & (any([word for word in key_phrases if word is not None and word in message.text.lower()]) & (message.chat.id in tracked_chats_ids)):
                    await app.send_message(message.from_user.id, phrase4user)
                    print(f"Сообщение '{phrase4user}' отправлено пользователю {message.from_user.first_name} {message.from_user.last_name} из чата {message.chat.title}")

        except Exception:
            pass


app.run()
