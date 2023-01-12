import googletrans
import aiogram
import config as cfg
import keyboard as k
from aiogram import types
import sqlite3
transl = googletrans.Translator()

bot = aiogram.Bot(token=cfg.TOKEN)

dp = aiogram.Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: aiogram.types.Message):
    con = sqlite3.connect('example.db')
    mycursor = con.cursor()

    sql = "SELECT * FROM users WHERE id = ?"
    adr = (str(message.from_user.id),)
    mycursor.execute(sql, adr)
    myresult = mycursor.fetchall()
    print(myresult)
    if myresult is None or myresult == [] or myresult == ():
        mycursor = con.cursor()
        sql = "INSERT INTO users (id, lang) VALUES (?, ?)"
        val = (str(message.from_user.id), "ru")
        mycursor.execute(sql, val)
        con.commit()
        await message.reply("Registred")
    else:
        await message.reply("You have already register in bot")

    await message.reply(cfg.STARTMSG)


@dp.message_handler(commands=['choose'])
async def process_start_command(message: aiogram.types.Message):
    await message.reply(cfg.CHOOSEMSG, reply_markup=k.keyb)


@dp.callback_query_handler(lambda c: c.data)
async def process_callback_kb1btn1(callback_query: aiogram.types.CallbackQuery):
    con = sqlite3.connect('example.db')
    if callback_query.data in cfg.LANGUES:
        lang = callback_query.data
        mycursor = con.cursor()
        mycursor.execute(f"UPDATE users SET lang = '{lang}' WHERE id = {callback_query.from_user.id}")
        con.commit()
        await bot.send_message(callback_query.from_user.id, "Lang has changed to " + cfg.LANGDICT[lang])


@dp.message_handler()
async def echo_message(msg: types.Message):
    con = sqlite3.connect('example.db')
    mycursor = con.cursor()
    mycursor.execute(f"SELECT * FROM users WHERE id = {msg.from_user.id}")
    myresult = mycursor.fetchall()
    lang = myresult[0][1]
    word = transl.translate(msg.text, src='uk', dest=lang).text

    await bot.send_message(msg.from_user.id, word)

if __name__ == '__main__':
    aiogram.executor.start_polling(dp)
