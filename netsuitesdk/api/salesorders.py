from collections import OrderedDict
from sqlite3.dbapi2 import Date

from .base import ApiBase
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class SalesOrders(ApiBase):
    SIMPLE_FIELDS = [
        'canHaveStackable',
        'ccApproved',
        'excludeCommission',
        'getAuth',
        'ignoreAvs',
        'isMultiShipTo',
        'isRecurringPayment',
        'isTaxable',
        'paypalProcess',
        'revRecOnRevCommitment',
        'saveOnAuthDecline',
        'shipComplete',
        'shipIsResidential',
        'syncPartnerTeams',
        'syncSalesTeams',
        'taxDetailsOverride',
        'taxRegOverride',
        'toBeEmailed',
        'toBeFaxed',
        'toBePrinted',
        'tranIsVsoeBundle',
        'vsoeAutoCalc',
        'customFieldList',
        'actualShipDate',
        'ccExpireDate',
        'endDate',
        'nextBill',
        'paymentEventDate',
        'revRecEndDate',
        'revRecStartDate',
        'salesEffectiveDate',
        'shipDate',
        'startDate',
        'taxPointDate',
        'tranDate',
        'validFrom',
        'altHandlingCost',
        'altSalesTotal',
        'altShippingCost',
        'balance',
        'deferredRevenue',
        'discountTotal',
        'estGrossProfit',
        'estGrossProfitPercent',
        'exchangeRate',
        'giftCertApplied',
        'handlingCost',
        'handlingTax1Rate',
        'oneTime',
        'recognizedRevenue',
        'recurAnnually',
        'recurMonthly',
        'recurQuarterly',
        'recurWeekly',
        'requiredDepositAmount',
        'requiredDepositDue',
        'requiredDepositPercentage',
        'shippingCost',
        'shippingTax1Rate',
        'subTotal',
        'tax2Total',
        'taxRate',
        'taxTotal',
        'total',
        'totalCostEstimate'
    ]

    RECORD_REF_FIELDS = [
        'billAddressList',
        'billingSchedule',
        'class',
        'createdFrom',
        'creditCard',
        'creditCardProcessor',
        'currency',
        'customForm',
        'department',
        'discountItem',
        'drAccount',
        'entity',
        'entityTaxRegNum',
        'fxAccount',
        'handlingTaxCode',
        'intercoTransaction',
        'job',
        'leadSource',
        'location',
        'messageSel',
        'nexus',
        'opportunity',
        'partner',
        'paymentMethod',
        'paymentOption',
        'paymentProcessingProfile',
        'promoCode',
        'revRecSchedule',
        'salesGroup',
        'salesRep',
        'shipAddressList',
        'shipMethod',
        'shippingTaxCode',
        'subsidiary',
        'subsidiaryTaxRegNum',
        'taxItem',
        'terms',
    ]

    READ_ONLY_FIELDS = ['subTotal', 'balance', 'discountTotal', 'giftCertApplied', 'total', 'exchangeRate']

    READ_ONLY_ITEM_FIELDS = ['quantityAvailable', 'quantityBackOrdered', 'quantityBilled', 'quantityCommitted', 'quantityFulfilled', 'quantityOnHand', 'quantityPacked', 'quantityPicked']

    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='SalesOrder')


    def post(self, data) -> OrderedDict:
        if data.externalId in ['', None, 0, [], {}]:
            raise ValueError("externalId is required")

        sales_order = self.ns_client.SalesOrder(externalId=data.externalId)

        self.build_simple_fields(self.SIMPLE_FIELDS, data, sales_order)

        self.build_record_ref_fields(self.RECORD_REF_FIELDS, data, sales_order)

        #self.build_custom_fields(data, sales_order)

        self.remove_readonly(sales_order, self.READ_ONLY_FIELDS)

        if hasattr(data, 'itemList'):
            sales_order.itemList = data.itemList

            for item in data.itemList['item']:
                for field in self.READ_ONLY_ITEM_FIELDS:
                    item[field] = None

        logger.info('able to create salesorder = %s', sales_order)
        return self.ns_client.upsert(sales_order)
