import itertools
import pytest

from plenum.common.constants import *
from sovrin_common.constants import ATTRIB
from sovrin_common.types import ClientAttribOperation


validator = ClientAttribOperation()


def test_attrib_with_enc_raw_hash_in_same_time_fails():
    txn = {
        TXN_TYPE: ATTRIB,
        TARGET_NYM: 'foo',
        RAW: '{}',
        ENC: 'foo',
        HASH: 'bar'
    }
    with pytest.raises(TypeError) as ex_info:
        validator.validate(txn)
    ex_info.match("only one field from '{}, {}, {}' is expected"
                  "".format(RAW, ENC, HASH))


def test_attrib_without_enc_raw_hash_fails():
    txn = {
        TXN_TYPE: ATTRIB,
        TARGET_NYM: 'foo'
    }
    with pytest.raises(TypeError) as ex_info:
        validator.validate(txn)
    ex_info.match("validation error: missed fields '{}, {}, {}'"
                  "".format(RAW, ENC, HASH))


def test_attrib_raw_is_invalid_json():
    txn = {
        TXN_TYPE: ATTRIB,
        TARGET_NYM: 'foo',
        RAW: 'foo',
    }
    with pytest.raises(TypeError) as ex_info:
        validator.validate(txn)
    ex_info.match("validation error: should be valid JSON string"
                  "".format(RAW, ENC, HASH))
