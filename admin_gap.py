from rubpy import Rubika
import asyncio


async def checkAd(text: str) -> bool:
    links: list = ['@', 'post', 'join', 'rubika.ir/']
    for link in links:
        if link in text.lower():
            return 1


async def deleteMessage(bot, group_guid: str, message_id: str, user_guid: str) -> dict:
    while 1:
        try:
            group_admins: list = [i['member_guid'] for i in await bot.getGroupAdmins(group_guid)]
            if user_guid in group_admins:
                break
            else:
                await bot.deleteMessages(group_guid, [message_id])
                break
        except:
            continue


async def lookGroup(bot, group_guid: str, message_id: str, user_guid: str) -> dict:
    while 1:
        try:
            group_admins: list = [i['member_guid'] for i in await bot.getGroupAdmins(group_guid)]
            if user_guid in group_admins:
                await bot.setMembersAccess(group_guid, [])
                await bot.sendMessage(group_guid, "**گروه قفل شد.**", message_id=message_id)
                break
        except:
            continue


async def openGroup(bot, group_guid: str, message_id: str, user_guid: str) -> dict:
    while 1:
        try:
            group_admins: list = [i['member_guid'] for i in await bot.getGroupAdmins(group_guid)]
            if user_guid in group_admins:
                await bot.setMembersAccess(group_guid, ['SendMessages'])
                await bot.sendMessage(group_guid, "**گروه باز شد.**", message_id=message_id)
                break
        except:
            continue


async def get_robot(bot, group_guid: str, message_id: str, user_guid: str) -> dict:
    while 1:
        try:
            username: dict = await bot.getUserInfo(user_guid)
            username: str = username['user']['first_name']
            await bot.sendMessage(group_guid, f"بفـــرما **{username}** عزیـــزم 😊🌹", message_id=message_id)
            break
        except:
            continue

bot = Rubika("mgmszldmjynfvcvzxdwmfwpzpcscwotb")
group_guid: str = ("g0BrHbg03fab5b82a4e7affd867e18e2")
answered: list = []
try:
    open('answered.txt', 'r').read()
except FileNotFoundError:
    open('answered.txt', 'w+').write('CreatedByShayan...')


async def main():
    while 1:
        try:
            last_message_id: str = await bot.getGroupLastMessageId(group_guid)
            messages: list = await bot.getMessagesInterval(group_guid, last_message_id)
            for msg in messages:
                if msg['type'] == 'Text' and not msg['message_id'] in open('answered.txt', 'r').read():
                    text: str = msg['text']
                    if await checkAd(text):
                        await deleteMessage(bot, group_guid, msg['message_id'], msg['author_object_guid'])

                    elif text == 'قفل گروه':
                        await lookGroup(bot, group_guid, msg['message_id'], msg['author_object_guid'])

                    elif text == 'بازکردن گروه' or text == 'باز کردن گروه':
                        await openGroup(bot, group_guid, msg['message_id'], msg['author_object_guid'])

                    elif text == 'ربات' or text == 'بات':
                        await get_robot(bot, group_guid, msg['message_id'], msg['author_object_guid'])

                    elif 'forwarded_from' in msg.keys():
                        await deleteMessage(bot, group_guid, msg['message_id'], msg['author_object_guid'])

                    open('answered.txt', 'a+').write('\n' + msg['message_id'])
        except:
            ...

loop = asyncio.new_event_loop()
asyncio.run(main())
asyncio.set_event_loop(loop)
