import logging
import os


class Logger:

    LOG_DIR = "logs"

    os.makedirs(
        LOG_DIR,
        exist_ok=True
    )

    logging.basicConfig(

        filename=os.path.join(
            LOG_DIR,
            "application.log"
        ),

        level=logging.INFO,

        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(message)s"
        )
    )

    logger = logging.getLogger(
        "ResearchEngine"
    )

    @classmethod
    def info(cls, message):

        cls.logger.info(message)

    @classmethod
    def warning(cls, message):

        cls.logger.warning(message)

    @classmethod
    def error(cls, message):

        cls.logger.error(message)