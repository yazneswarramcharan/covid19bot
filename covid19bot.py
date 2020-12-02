import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
import requests

BOT_TOKEN = os.environ.get("BOT_API_KEY","")

bot = telegram.Bot(BOT_TOKEN)


def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("WORLDWIDE", callback_data='World'),
            InlineKeyboardButton("INDIA", callback_data='india'),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose which data u want:', reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    if query.data == "World":
        world_data=os.environ.get("WORLD_API_KEY","")
        world = requests.get(os.environ.get(world_data).json()
        r = world['data'][0]
        s = ""
        for i in r:
            if i!="updated_at":
                s += str(i) + "  - " + str(r[i]) + "\n"
        bot.send_message(update.effective_user.id, s)
    elif query.data[0] == "+":
        state_data=os.environ.get("STATE_API_KEY","")
        state=requests.get(state_data).json()
        for i in range(len(state)):
            if state[i]['state'] == query.data[1:]:
                s=""
                for j in state[i]:
                    if j!="districtData" and j!="id":
                        s+=str(j) + "  - " +str(state[i][j]) + "\n"
                bot.send_message(update.effective_user.id, s) 
                break
    else:
        world = requests.get(state_data).json()
        india_data=os.environ.get("INDIA_API_KEY","")
        india = requests.get(india_data).json()
        ind=india['data']['timeline'][0];s=""
        for i in ind:
            if i!="updated_at":
                s += str(i) + "  - " + str(ind[i]) + "\n"
        bot.send_message(update.effective_user.id, s) 

        w = world
        keyboard = []
        for i in range(len(w)):
            keyboard += [
                [
                    InlineKeyboardButton(w[i]['state'], callback_data="+" + str(w[i]['state'])),
                ],
            ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        bot.send_message(update.effective_user.id, 'India States', reply_markup=reply_markup)

    query.answer()


def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()

if __name__=='__main__':
    main()
