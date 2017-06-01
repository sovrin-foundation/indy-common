import itertools
import pytest

from plenum.common.constants import *
from sovrin_common.constants import ATTRIB, ENDPOINT
from sovrin_common.types import ClientAttribOperation


validator = ClientAttribOperation()


def test_attrib_with_enc_raw_hash_at_same_time_fails():
    msg = {
        TXN_TYPE: ATTRIB,
        TARGET_NYM: 'foo',
        RAW: '{}',
        ENC: 'foo',
        HASH: 'bar'
    }
    with pytest.raises(TypeError) as ex_info:
        validator.validate(msg)
    ex_info.match("validation error: only one field "
                  "from {}, {}, {} is expected"
                  "".format(RAW, ENC, HASH))


def test_attrib_without_enc_raw_hash_fails():
    msg = {
        TXN_TYPE: ATTRIB,
        TARGET_NYM: 'foo'
    }
    with pytest.raises(TypeError) as ex_info:
        validator.validate(msg)
    ex_info.match("validation error: missed fields {}, {}, {}"
                  "".format(RAW, ENC, HASH))


def test_attrib_with_raw_string_fails():
    msg = {
        TXN_TYPE: ATTRIB,
        TARGET_NYM: 'foo',
        RAW: 'foo',
    }
    with pytest.raises(TypeError) as ex_info:
        validator.validate(msg)
    ex_info.match("validation error: should be a "
                  "valid JSON string \({}=foo\)".format(RAW))


def test_attrib_with_raw_empty_json_fails():
    msg = {
        TXN_TYPE: ATTRIB,
        TARGET_NYM: 'foo',
        RAW: '{}',
    }
    with pytest.raises(TypeError) as ex_info:
        validator.validate(msg)
    ex_info.match("validation error: should contain one attribute "
                  "\({}={{}}\)".format(RAW))


def test_attrib_with_raw_array_fails():
    msg = {
        TXN_TYPE: ATTRIB,
        TARGET_NYM: 'foo',
        RAW: '[]',
    }
    with pytest.raises(TypeError) as ex_info:
        validator.validate(msg)
    ex_info.match("validation error: should be a dict "
                  "\({}=<class 'list'>\)".format(RAW))


def test_attrib_with_raw_having_more_one_attrib_fails():
    msg = {
        TXN_TYPE: ATTRIB,
        TARGET_NYM: 'foo',
        RAW: '{"attr1": "foo", "attr2": "bar"}',
    }
    with pytest.raises(TypeError) as ex_info:
        validator.validate(msg)
    ex_info.match("validation error: should contain one attribute "
                  "\({}={{.*}}\)".format(RAW))


def test_attrib_with_raw_having_one_attrib_passes():
    msg = {
        TXN_TYPE: ATTRIB,
        TARGET_NYM: 'foo',
        RAW: '{"attr1": "foo"}',
    }
    validator.validate(msg)


def test_attrib_with_raw_having_endpoint_equal_null_passes():
    msg = {
        TXN_TYPE: ATTRIB,
        TARGET_NYM: 'foo',
        RAW: '{"endpoint": null}',
    }
    validator.validate(msg)


def test_attrib_with_raw_having_endpoint_ha_equal_null_passes():
    msg = {
        TXN_TYPE: ATTRIB,
        TARGET_NYM: 'foo',
        RAW: '{"endpoint": {"ha": null}}',
    }
    validator.validate(msg)


def test_attrib_with_raw_having_endpoint_without_ha_passes():
    msg = {
        TXN_TYPE: ATTRIB,
        TARGET_NYM: 'foo',
        RAW: '{"endpoint": {"foo": "bar"}}',
    }
    validator.validate(msg)


def test_attrib_with_raw_having_endpoint_ha_with_ip_address_only_fails():
    msg = {
        TXN_TYPE: ATTRIB,
        TARGET_NYM: 'foo',
        RAW: '{"endpoint": {"ha": "8.8.8.8"}}',
    }
    with pytest.raises(TypeError) as ex_info:
        validator.validate(msg)
    ex_info.match("validation error: invalid endpoint format ip_address:port "
                  "\({}={{'ha': '8.8.8.8'}}\)".format(ENDPOINT))


def test_attrib_with_raw_having_endpoint_ha_with_invalid_port_fails():
    msg = {
        TXN_TYPE: ATTRIB,
        TARGET_NYM: 'foo',
        RAW: '{"endpoint": {"ha": "8.8.8.8:65536"}}',
    }
    with pytest.raises(TypeError) as ex_info:
        validator.validate(msg)
    ex_info.match("validation error: invalid endpoint port "
                  "\(ha=8.8.8.8:65536\)")


def test_attrib_with_raw_having_endpoint_ha_with_invalid_ip_address_fails():
    msg = {
        TXN_TYPE: ATTRIB,
        TARGET_NYM: 'foo',
        RAW: '{"endpoint": {"ha": "256.8.8.8:9700"}}',
    }
    with pytest.raises(TypeError) as ex_info:
        validator.validate(msg)
    ex_info.match("validation error: invalid endpoint address "
                  "\(ha=256.8.8.8:9700\)")
