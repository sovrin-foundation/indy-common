from plenum.common.txn import TARGET_NYM, TXN_TYPE, NYM, ROLE, VERKEY
from plenum.common.types import Identifier
from sovrin_common.auth import Authoriser

from sovrin_common.generates_request import GeneratesRequest
from sovrin_common.txn import GET_NYM, NULL
from sovrin_common.types import Request


class Identity(GeneratesRequest):
    def __init__(self,
                 identifier: Identifier,
                 trustAnchor: Identifier=None,
                 verkey=None,
                 role=None,
                 last_synced=None,
                 seqNo=None):
        """

        :param identifier:
        :param trustAnchor:
        :param verkey:
        :param role: If role is explicitly passed as `null` then in the request
         to ledger, `role` key would be sent as None which would stop the
         Identity's ability to do any privileged actions. If role is not passed,
          `role` key will not be included in the request to the ledger
        :param last_synced:
        :param seqNo:
        """
        self.identifier = identifier
        self.trustAnchor = trustAnchor

        # None indicates the identifier is a cryptonym
        self.verkey = verkey

        # None indicates the identifier is a cryptonym
        # if role and role not in (TRUST_ANCHOR, STEWARD):
        if not Authoriser.isValidRole(self.correctRole(role)):
            raise AttributeError("Invalid role {}".format(role))
        self._role = role

        # timestamp for when the ledger was last checked for key replacement or
        # revocation
        self.last_synced = last_synced

        # sequence number of the latest key management transaction for this
        # identifier
        self.seqNo = seqNo

    @staticmethod
    def correctRole(role):
        return None if role == NULL else role

    @property
    def role(self):
        return self.correctRole(self._role)

    @role.setter
    def role(self, role):
        if not Authoriser.isValidRole(self.correctRole(role)):
            raise AttributeError("Invalid role {}".format(role))
        self._role = role

    def _op(self):
        op = {
            TXN_TYPE: NYM,
            TARGET_NYM: self.identifier
        }
        if self.verkey is not None:
            op[VERKEY] = self.verkey
        if self._role:
            op[ROLE] = self.role
        return op

    def ledgerRequest(self):
        if not self.seqNo:
            assert self.identifier is not None
            return Request(identifier=self.trustAnchor, operation=self._op())

    def _opForGet(self):
        return {
            TARGET_NYM: self.identifier,
            TXN_TYPE: GET_NYM,
        }

    def getRequest(self, requestAuthor: Identifier):
        if not self.seqNo:
            return Request(identifier=requestAuthor, operation=self._opForGet())
