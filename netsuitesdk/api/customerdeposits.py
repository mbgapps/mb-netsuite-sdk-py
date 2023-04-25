from typing import OrderedDict
from netsuitesdk.internal.utils import PaginatedSearch
from .base import ApiBase
import logging

logger = logging.getLogger(__name__)

class CustomerDeposits(ApiBase):

    READ_ONLY_FIELDS = [
        'createdDate',
        'lastModifiedDate',
        'subTotal',
        'tranId',
        'discountTotal',
        'giftCertApplied',
        'total',
        'exchangeRate',
        'currency'
    ]

    RECORD_REF_FIELDS = [
        'account',
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
        'salesOrder',
        'subsidiary',
    ]

    SIMPLE_FIELDS = [
        'ccApproved',
        'ccIsPurchaseCardBin',
        'ccProcessAsPurchaseCard',
        'chargeIt',
        'ignoreAvs',
        'isRecurringPayment',
        'undepFunds',
        'applyList',
        'ccExpireDate',
        'createdDate',
        'lastModifiedDate',
        'tranDate',
        'validFrom',
        'exchangeRate',
        'payment',
        'authCode',
        'ccName',
        'ccNumber',
        'ccSecurityCode',
        'ccStreet',
        'ccZipCode',
        'checkNum',
        'currencyName',
        'debitCardIssueNo',
        'memo',
        'pnRefNum',
        'softDescriptor',
        'status',
        'threeDStatusCode',
        'payment'
    ]

    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='CustomerDeposit')

    def get_from_sales_order(self, external_id):

        so_rref = self.ns_client.RecordRef(**({'externalId': str(external_id), 'type': 'salesOrder'}))
        search_field = self.ns_client.SearchMultiSelectField(searchValue=[so_rref], operator="anyOf")
        bs = self.ns_client.basic_search_factory('Transaction', salesOrder=search_field)

        paginated_search = PaginatedSearch(client=self.ns_client,
                                            type_name='Transaction',
                                            basic_search=bs,
                                            pageSize=20)
        return self._paginated_search_to_generator(paginated_search=paginated_search)

    def get_undeposited(self):

        so_rref = self.ns_client.RecordRef(**({'internalId': 122}))
        search_field = self.ns_client.SearchMultiSelectField(searchValue=[so_rref], operator="anyOf")
        bs = self.ns_client.basic_search_factory('Transaction', account=search_field)

        paginated_search = PaginatedSearch(client=self.ns_client,
                                            type_name='Transaction',
                                            basic_search=bs,
                                            pageSize=1000)
        return self._paginated_search_to_generator(paginated_search=paginated_search)

    def delete(self, internalId):
        return super().delete('customerDeposit', internalId)

    def post(self, data) -> OrderedDict:

        customer_deposit = self.ns_client.CustomerDeposit(externalId=data['externalId'])

        self.build_simple_fields(self.SIMPLE_FIELDS, data, customer_deposit)

        self.build_record_ref_fields(self.RECORD_REF_FIELDS, data, customer_deposit)
    
        self.build_custom_fields(data, customer_deposit)

        self.remove_readonly(customer_deposit, self.READ_ONLY_FIELDS)

        logger.debug('able to create customer = %s', customer_deposit)
        res = self.ns_client.upsert(customer_deposit)
        return self._serialize(res)