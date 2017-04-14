from plenum.common.constants import STEWARD, TRUSTEE
from sovrin_common.constants import TGB, TRUST_ANCHOR
from sovrin_common.roles import Roles


def testRolesAreEncoded():
    assert STEWARD == "2"
    assert TRUSTEE == "0"
    assert TGB == "100"
    assert TRUST_ANCHOR == "101"


def testRolesEnumDecoded():
    assert Roles.STEWARD.name == "STEWARD"
    assert Roles.TRUSTEE.name == "TRUSTEE"
    assert Roles.TGB.name == "TGB"
    assert Roles.TRUST_ANCHOR.name == "TRUST_ANCHOR"


def testRolesEnumEncoded():
    assert Roles.STEWARD.value == "2"
    assert Roles.TRUSTEE.value == "0"
    assert Roles.TGB.value == "100"
    assert Roles.TRUST_ANCHOR.value == "101"
