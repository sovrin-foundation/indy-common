from enum import Enum

from plenum.common.transactions import PlenumTransactions


class SovrinTransactions(Enum):
    #  These numeric constants CANNOT be changed once they have been used,
    #  because that would break backwards compatibility with the ledger
    NODE = PlenumTransactions.NODE.value
    NYM = PlenumTransactions.NYM.value
    ATTRIB = "2"
    SCHEMA = "3"
    ISSUER_KEY = "4"

    DISCLO = "6"
    GET_ATTR = "7"
    GET_NYM = "8"
    GET_TXNS = "9"
    GET_SCHEMA = "10"
    GET_ISSUER_KEY = "11"

    POOL_UPGRADE = "12"
    NODE_UPGRADE = "13"

    def __str__(self):
        return self.name
