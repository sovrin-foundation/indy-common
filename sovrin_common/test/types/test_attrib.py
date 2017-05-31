import itertools
import pytest

from plenum.common.constants import *
from sovrin_common.constants import ATTRIB, ENDPOINT
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
    ex_info.match("validation error: only one field "
                  "from {}, {}, {} is expected"
                  "".format(RAW, ENC, HASH))


def test_attrib_without_enc_raw_hash_fails():
    txn = {
        TXN_TYPE: ATTRIB,
        TARGET_NYM: 'foo'
    }
    with pytest.raises(TypeError) as ex_info:
        validator.validate(txn)
    ex_info.match("validation error: missed fields {}, {}, {}"
                  "".format(RAW, ENC, HASH))


def test_attrib_raw_is_invalid_json_fails():
    txn = {
        TXN_TYPE: ATTRIB,
        TARGET_NYM: 'foo',
        RAW: 'foo',
    }
    with pytest.raises(TypeError) as ex_info:
        validator.validate(txn)
    ex_info.match("validation error: should be a "
                  "valid JSON string \({}=foo\)".format(RAW))


def test_attrib_raw_empty_dict_fails():
    txn = {
        TXN_TYPE: ATTRIB,
        TARGET_NYM: 'foo',
        RAW: '{}',
    }
    with pytest.raises(TypeError) as ex_info:
        validator.validate(txn)
    ex_info.match("validation error: should contain one attribute "
                  "\({}={{}}\)".format(RAW))


def test_attrib_raw_list_fails():
    txn = {
        TXN_TYPE: ATTRIB,
        TARGET_NYM: 'foo',
        RAW: '[]',
    }
    with pytest.raises(TypeError) as ex_info:
        validator.validate(txn)
    ex_info.match("validation error: should be a dict "
                  "\({}=<class 'list'>\)".format(RAW))


def test_attrib_raw_more_that_one_attrib_fails():
    txn = {
        TXN_TYPE: ATTRIB,
        TARGET_NYM: 'foo',
        RAW: '{"attr1": "foo", "attr2": "bar"}',
    }
    with pytest.raises(TypeError) as ex_info:
        validator.validate(txn)
    ex_info.match("validation error: should contain one attribute "
                  "\({}={{.*}}\)".format(RAW))


def test_attrib_raw_one_attrib_passes():
    txn = {
        TXN_TYPE: ATTRIB,
        TARGET_NYM: 'foo',
        RAW: '{"attr1": "foo"}',
    }
    validator.validate(txn)


def test_attrib_raw_endpoint_none_passes():
    txn = {
        TXN_TYPE: ATTRIB,
        TARGET_NYM: 'foo',
        RAW: '{"endpoint": null}',
    }
    validator.validate(txn)


def test_attrib_raw_endpoint_ha_none_passes():
    txn = {
        TXN_TYPE: ATTRIB,
        TARGET_NYM: 'foo',
        RAW: '{"endpoint": {"ha": null}}',
    }
    validator.validate(txn)


def test_attrib_raw_endpoint_without_ha_passes():
    txn = {
        TXN_TYPE: ATTRIB,
        TARGET_NYM: 'foo',
        RAW: '{"endpoint": {"foo": "bar"}}',
    }
    validator.validate(txn)


def test_attrib_raw_endpoint_ha_only_ip_address_fails():
    txn = {
        TXN_TYPE: ATTRIB,
        TARGET_NYM: 'foo',
        RAW: '{"endpoint": {"ha": "8.8.8.8"}}',
    }
    with pytest.raises(TypeError) as ex_info:
        validator.validate(txn)
    ex_info.match("validation error: invalid endpoint format ip_address:port "
                  "\({}={{'ha': '8.8.8.8'}}\)".format(ENDPOINT))


def test_attrib_raw_endpoint_ha_invalid_port_fails():
    txn = {
        TXN_TYPE: ATTRIB,
        TARGET_NYM: 'foo',
        RAW: '{"endpoint": {"ha": "8.8.8.8:65536"}}',
    }
    with pytest.raises(TypeError) as ex_info:
        validator.validate(txn)
    ex_info.match("validation error: invalid endpoint port "
                  "\(ha=8.8.8.8:65536\)")


def test_attrib_raw_endpoint_ha_invalid_ip_address_fails():
    txn = {
        TXN_TYPE: ATTRIB,
        TARGET_NYM: 'foo',
        RAW: '{"endpoint": {"ha": "256.8.8.8:9700"}}',
    }
    with pytest.raises(TypeError) as ex_info:
        validator.validate(txn)
    ex_info.match("validation error: invalid endpoint address "
                  "\(ha=256.8.8.8:9700\)")
