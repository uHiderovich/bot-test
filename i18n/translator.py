from lexicon.lexicon_en import EN
from lexicon.lexicon_ru import RU


def get_translations() -> dict[str, str | dict[str, str]]:
    return {
        "default": "ru",
        "en": EN,
        "ru": RU,
    }
