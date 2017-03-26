from copy import deepcopy
from hashlib import sha256

from plenum.common.request import Request as PRequest
from plenum.common.constants import TXN_TYPE, RAW, ENC, HASH
from plenum.common.types import OPERATION

from sovrin_common.constants import ATTRIB


class Request(PRequest):
    def getSigningState(self):
        """
        Special signing state where the the data for an attribute is hashed
        before signing
        :return: state to be used when signing
        """
        if self.operation.get(TXN_TYPE) == ATTRIB:
            d = deepcopy(super().getSigningState())
            op = d[OPERATION]
            keyName = {RAW, ENC, HASH}.intersection(set(op.keys())).pop()
            op[keyName] = sha256(op[keyName].encode()).hexdigest()
            return d
        return super().getSigningState()


