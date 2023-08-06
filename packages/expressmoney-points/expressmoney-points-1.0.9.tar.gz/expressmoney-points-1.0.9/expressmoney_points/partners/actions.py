__all__ = ('NewUserActionPoint', 'FirstLoanActionPoint')

from expressmoney.api import *

SERVICE = 'partners'
APP = 'actions'


class NewUserActionCreateContract(Contract):
    pass


class NewUserActionReadContract(Contract):
    created = serializers.DateTimeField()
    referral = serializers.IntegerField(min_value=1)


class FirstLoanActionCreateContract(Contract):
    pass


class FirstLoanActionReadContract(NewUserActionReadContract):
    pass


class NewUserActionID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'new_user_action'


class FirstLoanActionID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'first_loan_action'


class NewUserActionPoint(ListPointMixin, CreatePointMixin, ContractPoint):
    _point_id = NewUserActionID()
    _create_contract = NewUserActionCreateContract
    _read_contract = NewUserActionReadContract
    _sort_by = 'created'


class FirstLoanActionPoint(ListPointMixin, CreatePointMixin, ContractPoint):
    _point_id = FirstLoanActionID()
    _create_contract = FirstLoanActionCreateContract
    _read_contract = FirstLoanActionReadContract
    _sort_by = 'created'
