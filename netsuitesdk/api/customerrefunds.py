from collections import OrderedDict

from zeep.wsdl.definitions import Operation
from netsuitesdk.internal.utils import PaginatedSearch
from sys import intern

from .base import ApiBase
import logging

logger = logging.getLogger(__name__)

class CustomerRefunds(ApiBase):
    SIMPLE_FIELDS = [
        'ccApproved',
        'ccIsPurchaseCardBin',
        'ccProcessAsPurchaseCard',
        'chargeIt',
        'toBePrinted',
        'ccExpireDate',
        'createdDate',
        'lastModifiedDate',
        'tranDate',
        'validFrom',
        'balance',
        'exchangeRate',
        'total',
        'address',
        'ccName',
        'ccNumber',
        'ccStreet',
        'ccZipCode',
        'currencyName',
        'debitCardIssueNo',
        'memo',
        'pnRefNum',
        'status',
        'tranId',
        'transactionNumber'
    ]

    RECORD_REF_FIELDS = [
        'account',
        'arAcct',
        'class',
        'creditCard',
        'creditCardProcessor',
        'currency',
        'customer',
        'customForm',
        'department',
        'location',
        'paymentMethod',
        'postingPeriod',
        'subsidiary',
        'voidJournal'
    ]

    READ_ONLY_FIELDS = ['internalId', 'balance', 'overdueBalance', 'representingSubsidiary',
                        'monthlyClosing', 'balance', 'overdueBalance', 'unbilledOrders', 'depositBalance',
                        'aging', 'aging1', 'aging2', 'aging3', 'aging4', 'lastModifiedDate', 'dateCreated',
                        'defaultAddress', 'entityStatus', 'receivablesAccount',
                        'currencyList']


    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='CustomerRefund')

    def blank(self, externalId) -> OrderedDict:

        blank = OrderedDict()
        blank.externalId = externalId
        blank.customFieldList = self.ns_client.CustomFieldList([])
        blank.subsidiary = self.ns_client.RecordRef(**({'internalId': '2'}))
        blank.account = self.ns_client.RecordRef(**({'internalId': '1'}))
        blank.paymentMethod = self.ns_client.RecordRef(**({'internalId': '1'}))

        return blank

    def create_from_deposit(self, internal_id):

        rref = self.ns_client.RecordRef(**({'internalId': str(internal_id),
                                            'type': 'customerDeposit'}))
        init_ref = self.ns_client.InitializeRef(type='customerDeposit', internalId=str(internal_id))
        init_rec = self.ns_client.InitializeRecord(type='customerRefund', reference=init_ref)
        refund = self.ns_client.request('initialize', initializeRecord=init_rec)

        return refund

    def get_from_deposits(self, internal_ids):

        searchValues=[]

        if isinstance(internal_ids, list):
            for id in internal_ids:
                rref = self.ns_client.RecordRef(**({'internalId': str(id), 'type': 'customerDeposit'}))
                searchValues.append(rref)
        else:
            rref = self.ns_client.RecordRef(**({'internalId': str(internal_ids), 'type': 'customerDeposit'}))
            searchValues.append(rref)

        search_field = self.ns_client.SearchMultiSelectField(searchValue=searchValues, operator="anyOf")
        record_field = self.ns_client.SearchEnumMultiSelectField(searchValue="_customerRefund", operator="anyOf")
        bs = self.ns_client.basic_search_factory('Transaction', appliedToTransaction=search_field, type=record_field)

        paginated_search = PaginatedSearch(client=self.ns_client,
                                            type_name='Transaction',
                                            basic_search=bs,
                                            pageSize=20)
        return self._paginated_search_to_generator(paginated_search=paginated_search)


    def post(self, data) -> OrderedDict:

        customerrefund = self.ns_client.CustomerRefund(externalId=data.externalId)

        self.build_simple_fields(self.SIMPLE_FIELDS, data, customerrefund)

        self.build_record_ref_fields(self.RECORD_REF_FIELDS, data, customerrefund)

        self.build_custom_fields(data, customerrefund)

        self.remove_readonly(customerrefund,self.READ_ONLY_FIELDS)

        if hasattr(data, 'applyList'):
            customerrefund.applyList = data.applyList

        if hasattr(data, 'depositList'):
            customerrefund.depositList = data.depositList

        logger.debug('able to create customer = %s', customerrefund)
        res = self.ns_client.upsert(customerrefund)
        return self._serialize(res)
