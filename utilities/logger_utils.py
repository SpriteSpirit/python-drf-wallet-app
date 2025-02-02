import logging


logger = logging.getLogger("custom_logger")
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

logger.addHandler(ch)

# Примеры использования логгера
# logger.debug("Это отладочное сообщение")
# logger.info("Это информационное сообщение")
# logger.warning("Это предупреждающее сообщение")
# logger.error("Это сообщение об ошибке")
# logger.critical("Это критическое сообщение")
