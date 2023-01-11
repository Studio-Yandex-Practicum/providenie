from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot import states


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Кнопка старт. Вывод главного меню."""
    text = "Тут будет актуальная новость из жизни фонда."
    buttons = [
        [
            InlineKeyboardButton(
                text="Хочу стать волонтёром",
                callback_data=str(states.ADD_VOLUNTEER),
            ),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    if context.user_data.get(states.START_OVER):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text=text, reply_markup=keyboard
        )
    else:
        await update.message.reply_text(text=text, reply_markup=keyboard)

    context.user_data[states.START_OVER] = False
    return states.SELECTING_ACTION


async def stop(update: Update, _) -> int:
    """Завершение работы по команде /stop."""
    await update.message.reply_text(
        "До свидания! " "Нажмите /start для повторного запуска"
    )
    return states.END


async def stop_nested(update: Update, _) -> str:
    """Завершение работы по команде /stop из вложенного разговора."""
    await update.message.reply_text(
        "До свидания! " "Нажмите /start для повторного запуска"
    )
    return states.STOPPING


async def end(update: Update, _) -> int:
    """Завершение разговора."""
    await update.callback_query.answer()
    return states.END


async def end_second_level(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Завершение вложенного разговора."""
    context.user_data[states.START_OVER] = True
    await start(update, context)
    return states.END
