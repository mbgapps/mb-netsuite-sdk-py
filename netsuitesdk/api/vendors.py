from collections import OrderedDict

from .base import ApiBase
import logging

logger = logging.getLogger(__name__)


class Vendors(ApiBase):
    SIMPLE_FIELDS = [
        'accountNumber',
        'addressbookList',
        'altEmail',
        'altName',
        'altPhone',
        'balance',
        'balancePrimary',
        'bcn',
        'billPay',
        'comments',
        'companyName',
        'creditLimit',
        'currencyList',
        'dateCreated',
        'defaultAddress',
        'eligibleForCommission',
        'email',
        'emailPreference',
        'emailTransactions',
        'entityId',
        'fax',
        'faxTransactions',
        'firstName',
        'giveAccess',
        'globalSubscriptionStatus',
        'homePhone',
        'internalId',
        'is1099Eligible',
        'isAccountant',
        'isInactive',
        'isJobResourceVend',
        'isPerson',
        'laborCost',
        'lastModifiedDate',
        'lastName',
        'legalName',
        'middleName',
        'mobilePhone',
        'openingBalance',
        'openingBalanceDate',
        'password',
        'password2',
        'phone',
        'phoneticName',
        'predConfidence',
        'predictedDays',
        'pricingScheduleList',
        'printOnCheckAs',
        'printTransactions',
        'purchaseOrderAmount',
        'purchaseOrderQuantity',
        'purchaseOrderQuantityDiff',
        'receiptAmount',
        'receiptQuantity',
        'receiptQuantityDiff',
        'requirePwdChange',
        'rolesList',
        'salutation',
        'sendEmail',
        'subscriptionsList',
        'taxIdNum',
        'taxRegistrationList',
        'title',
        'unbilledOrders',
        'unbilledOrdersPrimary',
        'url',
        'vatRegNumber',
        'nullFieldList',
    ]

    RECORD_REF_FIELDS = [
        'currency',
        'category',
        'customForm',
        'defaultTaxReg',
        'expenseAccount',
        'image',
        'incoterm',
        'openingBalanceAccount',
        'payablesAccount',
        'taxItem',
        'terms',
    ]

    READ_ONLY_FIELDS = [
        'internalId',
        'balance',
        'defaultAddress',
        'balancePrimary',
        'unbilledOrdersPrimary',
        'currencyList'
    ]

    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='Vendor')

    def blank(self, externalId) -> OrderedDict:

        blank = OrderedDict()
        blank.externalId = externalId
        blank.customFieldList = self.ns_client.CustomFieldList([])
        blank.subsidiary = self.ns_client.RecordRef(**({'internalId': 2}))

        return blank


    def post(self, data) -> OrderedDict:
        assert data['externalId'], 'missing external id'
        vendor = self.ns_client.Vendor(externalId=data['externalId'])

        self.remove_readonly(data, self.READ_ONLY_FIELDS)

        if 'subsidiary' in data and data['subsidiary'] is not None:
            vendor['subsidiary'] = self.ns_client.RecordRef(**(data['subsidiary']))
        else:
            vendor['subsidiary'] = self.ns_client.RecordRef(**({'internalId': 1}))

        self.build_simple_fields(self.SIMPLE_FIELDS, data, vendor)

        self.build_record_ref_fields(self.RECORD_REF_FIELDS, data, vendor)
        
        self.build_custom_fields(data, vendor)

        logger.debug('able to create vendor = %s', vendor)
        res = self.ns_client.upsert(vendor)
        return self._serialize(res)
