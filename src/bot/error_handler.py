import logging

from telegram import Update
from telegram.ext import ContextTypes


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log Error caused by Update."""
    logging.error(msg="Exception while handling an update:", exc_info=context.error)
