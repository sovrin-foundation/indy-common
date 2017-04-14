from plenum.common.init_util import initialize_node_environment as \
    p_initialize_node_environment
from plenum.persistence.orientdb_store import OrientDbStore
from sovrin_common.config_util import getConfig


def cleanup_environment(name, config):
    o_client = OrientDbStore.new_orientdb_client(user=config.OrientDB["user"],
                                                 password=config.OrientDB["password"],
                                                 host=config.OrientDB["host"],
                                                 port=config.OrientDB["port"],)
    OrientDbStore.wipe_db(o_client, name)
    pass


def initialize_node_environment(name, base_dir, sigseed=None,
                                override_keep=False,
                                config=None):
    # Question: Does this comment belong here? I dont think so.
    """
    transport-agnostic method; in the future when the transport protocol is
    abstracted a bit more, this function and the one below will be the same
    and likely a method of an interface
    """
    config = config or getConfig()
    cleanup_environment(name, config)
    vk = p_initialize_node_environment(name, base_dir, sigseed, override_keep)
    return vk
