import logging
from typing import Optional
from datetime import datetime
import re

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

TOKEN = '7128849436:AAE6uhEK6_kViChviOAkfr-NNlAcCEx5wiU'

# Define states for conversation
TEXTS = {
    "ru": {
        "welcome": "Добро пожаловать! Выберите опцию:",
        "main_menu": "Главное меню",
        "tariffs": "Тарифы",
        "tariff": "Тариф",
        "cinerama": "Cinerama",
        "connect": "Подключить",
        "language": "Язык",
        "recommendations": "Мы рекомендуем попробовать тарифы 'Тезкор' или 'Барқарор'.",
        "available_tariffs": "Доступные тарифы:",
        "select_name": "Пожалуйста, введите ваше имя:",
        "select_phone": "Теперь введите ваш номер телефона:",
        "confirmation": "Спасибо! Вот ваша заявка:\n\nИмя: {name}\nТелефон: {phone}\nТариф: {tariff}\n\nСкоро мы с вами свяжемся.",
        "cancel": "Отменить",
        "cancelled": "Заявка отменена. Возврат в главное меню.",
        "language_selection": "Выберите язык:",
        "currency": "сум",
        "speed": "Мбит/с",
        "yourSelectedTariff": "Ваш выбранный тариф:",
        "pleaseEnterYourName": "Введите Ваше имя:",
        "submit": "Подавать",
        "proccesCanceled": "Процесс отменен",
        "proccesCanceledSelectTariff": "Давайте начнем заново. Пожалуйста, выберите тариф.",
        "youRequestSentSuccessfuly": "Ваша информация успешно отправлена!",
        "powEnterPhone":"Спасибо! Теперь введите свой номер телефона:",
        "phone":"Телефон",
        "validatePhone":"Пожалуйста, введите действительный номер телефона",
        "yourDetails":"Спасибо! Вот ваши данные",
        "ifEveryThingCorrect":"Если все верно, нажмите «Подать» для подтверждения или «Отменить», чтобы начать заново.",
        "name":"Имя"

    },
    "uz": {
        "welcome": "Xush kelibsiz! Iltimos, birini tanlang:",
        "main_menu": "Asosiy menyu",
        "tariffs": "Tariflar",
        "tariff": "arif",
        "cinerama": "Cinerama",
        "connect": "Ulanish",
        "language": "Til",
        "recommendations": "Biz 'Tezkor' yoki 'Barqaror' tariflarini tavsiya qilamiz.",
        "available_tariffs": "Mavjud tariflar:",
        "select_name": "Iltimos, ismingizni kiriting:",
        "select_phone": "Endi telefon raqamingizni kiriting:",
        "confirmation": "Rahmat! Sizning arizangiz:\n\nIsm: {name}\nTelefon: {phone}\nTarif: {tariff}\n\nTez orada siz bilan bog'lanamiz.",
        "cancel": "Bekor qilish",
        "cancelled": "Ariza bekor qilindi. Asosiy menyuga qaytish.",
        "language_selection": "Tilni tanlang:",
        "currency": "sum",
        "speed": "MBit/s",
        "yourSelectedTariff": "Siz tanlagan tarif:",
        "pleaseEnterYourName": "Iltimos, ismingizni kiriting:",
        "submit": "Yuborish",
        "proccesCanceled": "Jarayon bekor qilindi",
        "proccesCanceledSelectTariff": "Yana boshlaylik. Iltimos, tarifni tanlang.",
        "youRequestSentSuccessfuly": "Ma'lumotlaringiz muvaffaqiyatli yuborildi!",
        "powEnterPhone":"Rahmat! Iltimos telefon nomeringizni kiriting:",
        "phone":"Telefon",
        "validatePhone":"Iltimos telefon raqamini to'g'ri kiriting",
        "yourDetails":"Rahmat! Mana sizning tafsilotlaringiz",
        "ifEveryThingCorrect":"Agar ma'lumotlar to'gri bo'lsa «Yuborish» tugmasini bosing aks holda «Bekor qilish» tugmasini bosing.",
                "name":"Ism"









    }
}
SELECT_TARIFF, ENTER_NAME, ENTER_PHONE, CONFIRM_DETAILS = range(4)

# Define language dictionaries

logging.basicConfig(level=logging.INFO)

TARIFFS_INFO = [
    {"name": "Тезкор", "price": "185,000", "speed": "100"},
    {"name": "Барқарор", "price": "125,000", "speed": "80"},
    {"name": "Чексиз", "price": "200,000", "speed": "100"},
]

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


# Function to get localized text
def get_text(context: ContextTypes.DEFAULT_TYPE, key: str) -> str:
    lang = context.user_data.get("language", "ru")
    return TEXTS[lang].get(key, key)


async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
        [InlineKeyboardButton(get_text(context, "tariffs"), callback_data="tariffs")],
        [InlineKeyboardButton(get_text(context, "cinerama"), callback_data="cinerama")],
        [InlineKeyboardButton(get_text(context, "connect"), callback_data="connect")],
        [InlineKeyboardButton(get_text(context, "language"), callback_data="language")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message:
        await update.message.reply_text(get_text(context, "welcome"), reply_markup=reply_markup)
    else:
        await update.callback_query.edit_message_text(get_text(context, "welcome"), reply_markup=reply_markup)
    return SELECT_TARIFF




# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['language'] = context.user_data.get("language", "ru")
    context.user_data['chat_id'] = update.message.chat.id 
    await show_main_menu(update, context)
    raise ApplicationHandlerStop()





# Language selection handler
async def language_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Русский", callback_data="lang_ru")],
        [InlineKeyboardButton("O'zbekcha", callback_data="lang_uz")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(get_text(context, "language_selection"), reply_markup=reply_markup)


async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    lang_code = query.data.split("_")[1]
    context.user_data["language"] = lang_code
    await show_main_menu(update, context)


async def tariffs_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Display tariffs dynamically
    keyboard = []
    for idx, tariff in enumerate(TARIFFS_INFO):
        tariff_text = f"{tariff['name']} - {tariff['price']} {get_text(context, 'currency')} ({tariff['speed']} {get_text(context, 'speed')})"
        keyboard.append([InlineKeyboardButton(tariff_text, callback_data=f'tariff_{idx}')])
    keyboard.append([InlineKeyboardButton(get_text(context, 'cancel'), callback_data='cancel')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text(get_text(context, 'tariffs'), reply_markup=reply_markup)
    return SELECT_TARIFF


async def connect_form(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Optional[int]:
    # Display tariffs dynamically
    if "tariff" in context.user_data.keys() and context.user_data['tariff'] != None:
        return SELECT_TARIFF
    else:
        await tariffs_menu(update, context)
        return 9999


# Handler for selecting a tariff
async def select_tariff(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    # Save selected tariff to context
    context.user_data['tariff'] = query.data
    tariff_index = query.data.split("_")[1]
    name = TARIFFS_INFO[int(tariff_index)].get("name")
    keyboard = [[InlineKeyboardButton(get_text(context, 'cancel'), callback_data='cancel')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        f"{get_text(context, 'yourSelectedTariff')} {name}. {get_text(context, 'pleaseEnterYourName')}",
        reply_markup=reply_markup)
    return ENTER_NAME


# Handler for entering name
async def enter_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_name=update.message.text
    if len(user_name)>0:
        context.user_data['name'] = update.message.text
        keyboard = [[InlineKeyboardButton(get_text(context, 'cancel'), callback_data='cancel')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(get_text(context,"powEnterPhone"), reply_markup=reply_markup)
        return ENTER_PHONE
    else:
        await query.edit_message_text(
        f"{get_text(context, 'yourSelectedTariff')} {name}. {get_text(context, 'pleaseEnterYourName')}",
        reply_markup=reply_markup)
        return ENTER_NAME


# Handler for entering phone number
async def enter_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    phone=update.message.text
    if validate_phone_number(phone):
        context.user_data['phone'] = update.message.text
        # Confirm details
        tariff = context.user_data['tariff']
        name = context.user_data['name']
        phone = context.user_data['phone']
        keyboard = [
                [InlineKeyboardButton(get_text(context, "submit"), callback_data="submit")],
                [InlineKeyboardButton(get_text(context, "cancel"), callback_data="cancel")],
                ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        # await update.callback_query.edit_message_text("Please confirm your details.", reply_markup=reply_markup)
        tariff_index = tariff.split("_")[1]
        tariffName = TARIFFS_INFO[int(tariff_index)].get("name")
        await update.message.reply_text(
               f"{get_text(context,"yourDetails")}:\n"
               f"{get_text(context,"tariff")}: {tariffName}\n"
               f"{get_text(context,"name")}: {name}\n"
               f"{get_text(context,"phone")}: {phone}\n"
               f"{get_text(context,"ifEveryThingCorrect")}",
               reply_markup=reply_markup
               )
        return CONFIRM_DETAILS
    else:
        await update.message.reply_text(get_text(context,"validatePhone"), reply_markup=reply_markup)
        return ENTER_PHONE



# Handler for confirmation
async def confirm_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query.data
    if query == 'submit':
        name = context.user_data.get("name")
        phone = context.user_data.get("phone")
        tariff = context.user_data['tariff']
        tariff_index = tariff.split("_")[1]
        tariffName = TARIFFS_INFO[int(tariff_index)].get("name")        
        group_chat_id = "@connection_requests_from_bot"  # Используйте имя группы (например, @mygroupname) или числовой ID группы
        lang_code=context.user_data["language"]
        current_time = datetime.now().strftime("%d.%m.%Y %H:%M")
        message = f"Дата подачи заявления: {current_time}\n\n" \
                  f"Имя: {name}\n" \
                  f"Телефон: {phone}\n" \
                  f"Язык: {lang_code}\n" \
                  f"Тариф: {tariffName}"  
        await update._bot.send_message(chat_id=group_chat_id, text=message)  
        await update.callback_query.message.reply_text(get_text(context,"youRequestSentSuccessfuly"))
        return ConversationHandler.END

        # Perform HTTP request to the server
        # async with aiohttp.ClientSession() as session:
        #     async with session.post('https://example.com/api/submit', json={"data": "your_data_here"}) as response:
        #         if response.status == 200:
        #             await update.callback_query.message.reply_text("Your information has been submitted successfully!")
        #             return ConversationHandler.END
        #         else:
        #             await update.callback_query.message.reply_text(
        #                 "Failed to submit your information. Please try again.")
        #             return SELECT_TARIFF
    elif query == 'cancel':
        await update.callback_query.message.reply_text(get_text(context,proccesCanceledSelectTariff))
        return SELECT_TARIFF


# Cancel handler to exit the conversation
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(get_text(context, "proccesCanceled"), reply_markup=ReplyKeyboardRemove())
    return SELECT_TARIFF

def validate_phone_number(phone: str) -> bool:
    # Regular expression pattern for validating the phone number
    pattern = r"^\+?9989\d{8}$"
    
    # Use re.match() to check if the phone number matches the pattern
    return bool(re.match(pattern, phone))

async def redirect_to_cinerama(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Create an inline keyboard button with the URL
    lang = context.user_data.get("language", "ru")
    keyboard = [[InlineKeyboardButton("Visit Cinerama", url=f"https://cinerama.uz/{lang}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send a message with the inline keyboard
    await update.callback_query.edit_message_text("Click the button below to visit Cinerama:",
                                                  reply_markup=reply_markup)


# Main function to run the bot
def handle_update():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(connect_form, pattern="^connect"))
    application.add_handler(CallbackQueryHandler(show_main_menu, pattern="^cancel"))
    application.add_handler(CallbackQueryHandler(language_menu, pattern="^language$"))
    application.add_handler(CallbackQueryHandler(set_language, pattern="^lang_"))
    application.add_handler(CallbackQueryHandler(redirect_to_cinerama, pattern="^cinerama"))
    application.add_handler(CallbackQueryHandler(confirm_details, pattern="^submit"))
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(tariffs_menu, pattern="^tariffs")],
        states={
            SELECT_TARIFF: [CallbackQueryHandler(select_tariff, pattern="^tariff_")],
            ENTER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_name)],
            ENTER_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_phone)],
            CONFIRM_DETAILS: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_details)],
        },
    
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True
    )

    application.add_handler(conv_handler)
    application.run_polling()
#
# if __name__ == '__main__':
#     handle_update()
