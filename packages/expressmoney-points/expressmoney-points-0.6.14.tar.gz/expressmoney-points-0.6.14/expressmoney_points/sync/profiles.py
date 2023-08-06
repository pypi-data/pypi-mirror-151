__all__ = ('ProfilePoint',)

from expressmoney.api import *

SERVICE = 'sync'


class ProfileReadContract(Contract):
    user_profile = serializers.IntegerField(min_value=1)
    created = serializers.DateTimeField(allow_null=True)


class ProfileID(ID):
    _service = SERVICE
    _app = 'profiles'
    _view_set = 'profile'


class ProfilePoint(ListPointMixin, ContractPoint):
    _point_id = ProfileID()
    _read_contract = ProfileReadContract
    _sort_by = 'created'
    _cache_enabled = False
