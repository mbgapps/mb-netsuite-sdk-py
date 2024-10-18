from collections import OrderedDict
from sqlite3.dbapi2 import Date

from .base import ApiBase
import logging
from datetime import datetime
from netsuitesdk.internal.exceptions import NetSuiteRequestError

logger = logging.getLogger(__name__)

class SalesOrders(ApiBase):
    SIMPLE_FIELDS = [
        'billingAddress',
        # 'canHaveStackable',
        # 'ccApproved',
        # 'excludeCommission',
        # 'getAuth',
        # 'ignoreAvs',
        # 'isMultiShipTo',
        # 'isRecurringPayment',
        # 'isTaxable',
        # 'paypalProcess',
        # 'revRecOnRevCommitment',
        # 'saveOnAuthDecline',
        # 'shipComplete',
        # 'shipIsResidential',
        # 'syncPartnerTeams',
        # 'syncSalesTeams',
        # 'taxDetailsOverride',
        # 'taxRegOverride',
        # 'toBeEmailed',
        # 'toBeFaxed',
        # 'toBePrinted',
        # 'tranIsVsoeBundle',
        # 'vsoeAutoCalc',
        # 'customFieldList',
        # 'actualShipDate',
        # 'ccExpireDate',
        # 'endDate',
        # 'nextBill',
        # 'paymentEventDate',
        # 'revRecEndDate',
        # 'revRecStartDate',
        # 'salesEffectiveDate',
        'shippingAddress',
        'shipDate',
        'startDate',
        # 'taxPointDate',
        'tranDate',
        # 'validFrom',
        # 'altHandlingCost',
        # 'altSalesTotal',
        # 'altShippingCost',
        # 'balance',
        # 'deferredRevenue',
        # 'discountTotal',
        # 'estGrossProfit',
        # 'estGrossProfitPercent',
        # 'exchangeRate',
        # 'giftCertApplied',
        # 'handlingCost',
        # 'handlingTax1Rate',
        # 'oneTime',
        # 'recognizedRevenue',
        # 'recurAnnually',
        # 'recurMonthly',
        # 'recurQuarterly',
        # 'recurWeekly',
        # 'requiredDepositAmount',
        # 'requiredDepositDue',
        # 'requiredDepositPercentage',
        # 'shippingCost',
        # 'shippingTax1Rate',
        # 'subTotal',
        # 'tax2Total',
        # 'taxRate',
        # 'taxTotal',
        'total',
        # 'totalCostEstimate',
        'otherRefNum',
        'itemList',
        'memo',
        'tranId'
    ]

    RECORD_REF_FIELDS = [
        # 'billAddressList',
        # 'billingSchedule',
        'class',
        # 'createdFrom',
        # 'creditCard',
        # 'creditCardProcessor',
        # 'currency',
        'customForm',
        # 'department',
        # 'discountItem',
        # 'drAccount',
        'entity',
        # 'entityTaxRegNum',
        # 'fxAccount',
        # 'handlingTaxCode',
        # 'intercoTransaction',
        # 'job',
        # 'leadSource',
        'location',
        # 'messageSel',
        # 'nexus',
        # 'opportunity',
        # 'partner',
        # 'paymentMethod',
        # 'paymentOption',
        'paymentProcessingProfile',
        # 'promoCode',
        # 'revRecSchedule',
        # 'salesGroup',
        # 'salesRep',
        # 'shipAddressList',
        'shipMethod',
        # 'shippingTaxCode',
        'subsidiary',
        # 'subsidiaryTaxRegNum',
        # 'taxItem',
        # 'terms',
    ]

    READ_ONLY_FIELDS = ['subTotal', 'balance', 'discountTotal', 'giftCertApplied', 'total', 'exchangeRate', 'status']

    READ_ONLY_ITEM_FIELDS = [
        'quantityAvailable', 
        'quantityBackOrdered', 
        'quantityBilled', 
        'quantityCommitted', 
        'quantityFulfilled', 
        'quantityOnHand', 
        'quantityPacked', 
        'quantityPicked'
    ]

    SIMPLE_ITEM_FIELDS = [
        'amount',
        'quantity',
        'internalId',
        'isClosed'
    ]

    RECORD_REF_ITEM_FIELDS = [
        'item',
        'price',
        'inventoryLocation',
        'inventorySubsidiary',
    ]

    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='SalesOrder')

    def get_by_internal_id(self, internalId):
        return self.ns_client.get('SalesOrder', internalId=internalId)

    def get_by_external_id(self, externalId):
        return self.ns_client.get('SalesOrder', externalId=externalId)

    def post(self, externalId, data) -> OrderedDict:
        if externalId in ['', None, 0, [], {}]:
            raise ValueError("externalId is required")
        
        sales_order = self.ns_client.SalesOrder(externalId=externalId)

        self.build_mb_simple_fields(self.SIMPLE_FIELDS, data, sales_order)
        self.build_mb_record_ref_fields(self.RECORD_REF_FIELDS, data, sales_order)
        self.build_mb_custom_fields(data, sales_order)
        self.remove_readonly(sales_order, self.READ_ONLY_FIELDS)

        if 'orderStatus' in data:
            sales_order.orderStatus = data['orderStatus']

        if 'itemList' in data:
            items = []
            for item in data['itemList']['item']:
                # for field in self.READ_ONLY_ITEM_FIELDS:
                #     item[field] = None
                wsdl_item = self.ns_client.SalesOrderItem()
                self.build_mb_simple_fields(self.SIMPLE_ITEM_FIELDS, item, wsdl_item)
                self.build_mb_record_ref_fields(self.RECORD_REF_ITEM_FIELDS, item, wsdl_item)
                self.build_mb_custom_fields(item, wsdl_item)
                items.append(wsdl_item)

            sales_order.itemList = self.ns_client.SalesOrderItemList(item=items)

        try:
            exists = True
            self.ns_client.get('SalesOrder', externalId=externalId)
        except NetSuiteRequestError:
            exists = False
            self.logger.warning('SalesOrder not found for externalId {} - attempting to add it'.format(externalId))
            # if sales order not found and the status is cancelled, just return and don't do anything
            if data['orderStatus'] == '_cancelled':
                self.logger.warning('Cancelled SalesOrder not found - not adding externalId {}'.format(externalId))
                return None

        # NS won't allow you to set order status to cancelled
        # if data['orderStatus'] == '_cancelled':
        #     sales_order.orderStatus = None

        # print(sales_order)

        if exists and data['orderStatus'] != '_cancelled':
            self.logger.warning('SalesOrder already exists - not adding externalId {}'.format(externalId))
            return None

        if exists and data['orderStatus'] == '_cancelled':
            self.logger.warning('Cancelling SalesOrder for externalId {}'.format(externalId))
            sales_order.orderStatus = None
            return self.ns_client.update(sales_order)
        else:
            return self.ns_client.add(sales_order)

    def update(self, externalId, data) -> OrderedDict:
        if externalId in ['', None, 0, [], {}]:
            raise ValueError("externalId is required")
        
        sales_order = self.ns_client.SalesOrder(externalId=externalId)

        self.build_mb_simple_fields(self.SIMPLE_FIELDS, data, sales_order)
        self.build_mb_record_ref_fields(self.RECORD_REF_FIELDS, data, sales_order)
        self.build_mb_custom_fields(data, sales_order)
        self.remove_readonly(sales_order, self.READ_ONLY_FIELDS)

        if 'orderStatus' in data:
            sales_order.orderStatus = data['orderStatus']

        if 'itemList' in data:
            items = []
            for item in data['itemList']['item']:
                # for field in self.READ_ONLY_ITEM_FIELDS:
                #     item[field] = None
                wsdl_item = self.ns_client.SalesOrderItem()
                self.build_mb_simple_fields(self.SIMPLE_ITEM_FIELDS, item, wsdl_item)
                self.build_mb_record_ref_fields(self.RECORD_REF_ITEM_FIELDS, item, wsdl_item)
                self.build_mb_custom_fields(item, wsdl_item)
                items.append(wsdl_item)

            sales_order.itemList = self.ns_client.SalesOrderItemList(item=items)

        return self.ns_client.update(sales_order)
