from enum import auto
from enum import Enum
from enum import IntEnum
from types import SimpleNamespace


class Plan(Enum):

    BLOSSOM = dict(
        per_minute=100,
        ticket_create=40,
        ticket_update=40,
        ticket_list=40,
        contacts_list=40,
    )

    GARDEN = dict(
        per_minute=200,
        ticket_create=80,
        ticket_update=60,
        ticket_list=60,
        contacts_list=60,
    )

    ESTATE = dict(
        per_minute=400,
        ticket_create=160,
        ticket_update=160,
        ticket_list=100,
        contacts_list=100,
    )

    FOREST = dict(
        per_minute=700,
        ticket_create=280,
        ticket_update=280,
        ticket_list=200,
        contacts_list=200,
    )

    def __init__(self, value):

        self.rates = SimpleNamespace(**self.value)


class APIVersion(IntEnum):

    V1 = auto()
    V2 = auto()

    def __init__(self, value):

        self.path = f'/v{value}'


class Resource(Enum):

    TICKET = '/tickets'
    TICKET_FIELDS = '/admin/ticket_fields'
