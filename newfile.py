import telethon
from telethon import TelegramClient, events

api_id = 21530910 # Замените на ваш API ID
api_hash = '721021ebf79afd43e78bc1cfc7466644' # Замените на ваш API Hash

client = TelegramClient('your_session_name', api_id, api_hash)

@client.on(events.NewMessage(outgoing=True))
async def handler(event):
    chat = await event.get_input_chat()

    async def delete_messages_in_dialog(dialog):
        messages = await client.get_messages(dialog.entity.id, from_user='me', limit=None)
        for message in messages:
            try:
                await message.delete()
            except Exception as e:
                print(f"Ошибка при удалении сообщения: {e}")

    # Удаляем сообщения в диалогах один на один и в группах/каналах одновременно
    dialogs = await client.get_dialogs()
    tasks = []
    for dialog in dialogs:
        if dialog.entity.id == chat.entity.id:  # Проверяем, что это нужный диалог
            tasks.append(delete_messages_in_dialog(dialog))

    # Запускаем удаление сообщений асинхронно
    await asyncio.gather(*tasks)

client.start()
client.run_until_disconnected()