from plenum.common.log import getlogger
from plenum.common.roles import Roles
from plenum.common.txn import TRUSTEE, TGB, STEWARD, TRUST_ANCHOR
from sovrin_common.txn import OWNER

logger = getlogger()


class Authoriser:
    ValidRoles = (TRUSTEE, TGB, STEWARD, TRUST_ANCHOR, None)

    AuthMap = {
        'NYM_role__{}'.format(TRUSTEE):
            {TRUSTEE: [],},
        'NYM_role__{}'.format(TGB):
            {TRUSTEE: [],},
        'NYM_role__{}'.format(STEWARD):
            {TRUSTEE: [], STEWARD: []},
        'NYM_role__{}'.format(TRUST_ANCHOR):
            {TRUSTEE: [], STEWARD: []},
        'NYM_role__':
            {TRUSTEE: [], TGB: [], STEWARD: [], TRUST_ANCHOR: []},
        'NYM_role_{}_'.format(TRUSTEE):
            {TRUSTEE: []},
        'NYM_role_{}_'.format(TGB):
            {TRUSTEE: []},
        'NYM_role_{}_'.format(STEWARD):
            {TRUSTEE: []},
        'NYM_role_{}_'.format(TRUST_ANCHOR):
            {TRUSTEE: []},
        'NYM_verkey_<any>_<any>':
            {r: [OWNER] for r in ValidRoles},
        'NODE_services__[VALIDATOR]':
            {STEWARD: [OWNER, ]},
        'NODE_services_[VALIDATOR]_[]':
            {TRUSTEE: [], STEWARD: [OWNER, ]},
        'NODE_node_ip_<any>_<any>':
            {STEWARD: [OWNER, ]},
        'NODE_node_port_<any>_<any>':
            {STEWARD: [OWNER, ]},
        'NODE_client_ip_<any>_<any>':
            {STEWARD: [OWNER, ]},
        'NODE_client_port_<any>_<any>':
            {STEWARD: [OWNER, ]},
        'POOL_UPGRADE_action__start':
            {TRUSTEE: [], TGB: []},
        'POOL_UPGRADE_action_start_cancel':
            {TRUSTEE: [], TGB: []}
    }

    @staticmethod
    def isValidRole(role) -> bool:
        return role in Authoriser.ValidRoles

    @staticmethod
    def getRoleFromName(roleName) -> bool:
        if not roleName:
            return None
        return Roles[roleName].value

    @staticmethod
    def isValidRoleName(roleName) -> bool:
        if not roleName:
            return True

        try:
            Authoriser.getRoleFromName(roleName)
        except KeyError:
            return False

        return True

    @staticmethod
    def authorised(typ, field, actorRole, oldVal=None, newVal=None,
                   isActorOwnerOfSubject=None) -> (bool, str):
        oldVal = '' if oldVal is None else \
            str(oldVal).replace('"', '').replace("'", '')
        newVal = '' if newVal is None else \
            str(newVal).replace('"', '').replace("'", '')
        key = '_'.join([typ, field, oldVal, newVal])
        if key not in Authoriser.AuthMap:
            key = '_'.join([typ, field, '<any>', '<any>'])
            if key not in Authoriser.AuthMap:
                msg = "key '{}' not found in authorized map". \
                    format(key)
                logger.error(msg)
                return False, msg
        roles = Authoriser.AuthMap[key]
        if actorRole not in roles:
            return False, '{} not in allowed roles {}'.format(actorRole, roles)
        roleDetails = roles[actorRole]
        if len(roleDetails) == 0:
            return True, ''
        else:
            r = OWNER in roleDetails and isActorOwnerOfSubject
            msg = '' if r else 'Only owner is allowed'
            return r, msg
