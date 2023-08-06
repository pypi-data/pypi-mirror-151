__all__ = ('NewUserActionPoint',)

from expressmoney.api import *

SERVICE = 'partners'
APP = 'actions'


class NewUserActionCreateContract(Contract):
    http_referer = serializers.URLField()


class NewUserActionReadContract(Contract):
    created = serializers.DateTimeField()
    referral = serializers.IntegerField(min_value=1)


class NewUserActionID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'new_user_action'


class NewUserActionPoint(ListPointMixin, CreatePointMixin, ContractPoint):
    _point_id = NewUserActionID()
    _create_contract = NewUserActionCreateContract
    _read_contract = NewUserActionReadContract
    _sort_by = 'created'
