from enum import Enum, unique

from plenum.common.roles import Roles


@unique
class Roles(Enum):
    #  These numeric constants CANNOT be changed once they have been used,
    #  because that would break backwards compatibility with the ledger
    TRUSTEE = Roles.TRUSTEE.value
    TGB = "1"
    STEWARD = Roles.STEWARD.value
    TRUST_ANCHOR = "3"

    def __str__(self):
        return self.name
