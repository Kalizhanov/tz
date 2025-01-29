from enum import Enum


class FinInstitution(str, Enum):
    KASPI = "Kaspi"
    HALYK = "Halyk"
    JUSAN = "Jusan"


class Language(str, Enum):
    RUS = "rus"
    ENG = "eng"
    KAZ = "kaz"
