import os


class CacheManager:

    CACHE_DIR = "data/cache"

    @classmethod
    def ensure_cache_dir(cls):

        os.makedirs(
            cls.CACHE_DIR,
            exist_ok=True
        )

    @classmethod
    def is_processed(cls, paper_id):

        cls.ensure_cache_dir()

        return os.path.exists(
            os.path.join(
                cls.CACHE_DIR,
                f"{paper_id}.done"
            )
        )

    @classmethod
    def mark_processed(cls, paper_id):

        cls.ensure_cache_dir()

        with open(
            os.path.join(
                cls.CACHE_DIR,
                f"{paper_id}.done"
            ),
            "w"
        ):

            pass