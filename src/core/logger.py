import logging

# from .settings import BASE_DIR, LOG_LEVEL


#  logs_folder = BASE_DIR / ".data/logs"
#  logs_folder.mkdir(parents=True, exist_ok=True)
#  filename = "bot.log"
#  final_dir = logs_folder / filename

# logging.basicConfig(
#     level=LOG_LEVEL,
#     filename=final_dir,
#     filemode="w",
#     format="%(asctime)s - %(levelname)s - %(message)s",
# )


# Вариант для консольных тестов
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)
