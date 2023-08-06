__all__ = ('PartnerServicePoint',)

from expressmoney.api import *

SERVICE = 'partners'


class PartnerReadContract(Contract):
    created = serializers.DateTimeField()
    user_id = serializers.IntegerField(min_value=1)
    code = serializers.CharField(max_length=8)


class PartnerServiceID(ID):
    _service = SERVICE
    _app = 'partners'
    _view_set = 'partner_service'


class PartnerServicePoint(ListPointMixin, ContractPoint):
    _point_id = PartnerServiceID()
    _read_contract = PartnerReadContract
    _sort_by = 'created'
    _cache_enabled = False
