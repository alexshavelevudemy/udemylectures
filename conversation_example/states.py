from enum import Enum


class States(Enum):
    START = 0
    WAIT_DATE = 1
    WAIT_PERSONS_COUNT = 2
    WAIT_PHONE = 3


