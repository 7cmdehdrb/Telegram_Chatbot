import sys
import os
from dotenv import load_dotenv
import keyboard
import threading
from telegram import Bot
from telegram.ext import Updater, CommandHandler
from weather import getWeatherXML, getWeatherJSON
from user import checkPasswordValidation, createUser, confirmUser

""" SYSTEM VARIABLE """

load_dotenv(verbose=True)

TOKEN = os.getenv("TOKEN")
BOT = Bot(token=TOKEN)
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher


def programExit():
    while True:
        if keyboard.read_key() == "esc":
            print("SHUTDOWN...")
            os._exit(1)


def start(update, context):
    text = "명령어\n\n/enroll (비밀번호) - 사용자 등록\n/weather (도시명, 영문) - 날씨 정보 조회"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    # Unique User ID
    # print(update.effective_chat.id)

    # Params
    # ex) /start HELLO WORLD => args[0] == "HELLO", args[1] == "WORLD"
    # print(context.args)

    return 0


def enroll(update, context):
    try:
        if len(context.args) == 0:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="비밀번호를 입력해주세요"
            )
            return 0

        id = str(update.effective_chat.id)
        pw = context.args[0]

        if checkPasswordValidation(pw) is True:
            if confirmUser(id) is True:
                context.bot.send_message(
                    chat_id=update.effective_chat.id, text="이미 등록된 사용자입니다"
                )
            else:
                createUser(id)
                context.bot.send_message(
                    chat_id=update.effective_chat.id, text="사용자를 등록하였습니다"
                )

        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="비밀번호가 일치하지 않습니다"
            )

    except Exception as ex:
        context.bot.send_message(chat_id=update.effective_chat.id, text="알 수 없는 오류")
        print(ex)
    finally:
        return 0


def weather(update, context):
    try:
        if len(context.args) == 0:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="도시 이름을 입력해주세요"
            )
            return 0

        id = str(update.effective_chat.id)

        if confirmUser(id) is True:
            city = context.args[0]

            # GET DATA WITH HTTP REQUESTS
            # wt = getWeatherXML(city=city)
            wt = getWeatherJSON(city=city)

            context.bot.send_message(
                chat_id=update.effective_chat.id, text=str(wt.createText())
            )

        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="등록되지 않은 사용자입니다"
            )

    except Exception as ex:
        context.bot.send_message(chat_id=update.effective_chat.id, text="알 수 없는 오류")
        print(ex)
    finally:
        return 0


if __name__ == "__main__":

    # keyboard input 'esc' to stop
    thread = threading.Thread(target=programExit)
    thread.start()

    # CommandHandler(command_name:str, callback_function: function)
    start_handler = CommandHandler("start", start)
    enroll_handler = CommandHandler("enroll", enroll)
    weather_handler = CommandHandler("weather", weather)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(enroll_handler)
    dispatcher.add_handler(weather_handler)

    updater.start_polling()
