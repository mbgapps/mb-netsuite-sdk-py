from typing import OrderedDict
from .base import ApiBase
from netsuitesdk.internal.utils import PaginatedSearch
import logging

logger = logging.getLogger(__name__)

class CashSales(ApiBase):

    RECORD_REF_FIELDS = [
        'account',
        'billAddressList',
        'billingAccount',
        'billingSchedule',
        'class',
        'createdFrom',
        'creditCard',
        'creditCardProcessor',
        'currency',
        'customForm',
        'department',
        'discountItem',
        'entity',
        'expCostDiscount',
        'expCostTaxCode',
        'handlingTaxCode',
        'itemCostDiscount',
        'itemCostTaxCode',
        'job',
        'leadSource',
        'location',
        'messageSel',
        'opportunity',
        'partner',
        'paymentMethod',
        'postingPeriod',
        'promoCode',
        'revRecSchedule',
        'salesGroup',
        'salesRep',
        'shipAddressList',
        'shipMethod',
        'shippingTaxCode',
        'subsidiary',
        'taxItem',
        'timeDiscount',
        'timeTaxCode'
    ]

    SIMPLE_FIELDS = [
        'ccApproved',
        'ccIsPurchaseCardBin',
        'ccProcessAsPurchaseCard',
        'chargeIt',
        'excludeCommission',
        'expCostDiscprint',
        'expCostDiscTaxable',
        'ignoreAvs',
        'isRecurringPayment',
        'isTaxable',
        'itemCostDiscPrint',
        'itemCostDiscTaxable',
        'paypalProcess',
        'recurringBill',
        'revRecOnRevCommitment',
        'shipIsResidential',
        'syncPartnerTeams',
        'syncSalesTeams',
        'timeDiscPrint',
        'timeDiscTaxable',
        'toBeEmailed',
        'toBeFaxed',
        'toBePrinted',
        'tranIsVsoeBundle',
        'undepFunds',
        'vsoeAutoCalc',
        'ccExpireDate',
        'createdDate',
        'endDate',
        'lastModifiedDate',
        'revRecEndDate',
        'revRecStartDate',
        'salesEffectiveDate',
        'shipDate',
        'startDate',
        'tranDate',
        'validFrom',
        'altHandlingCost',
        'altShippingCost',
        'deferredRevenue',
        'discountTotal',
        'estGrossProfit',
        'estGrossProfitPercent',
        'exchangeRate',
        'expCostDiscAmount',
        'expCostDiscTax1Amt',
        'expCostTaxRate1',
        'expCostTaxRate2',
        'giftCertApplied',
        'handlingCost',
        'handlingTax1Rate',
        'itemCostDiscAmount',
        'itemCostDiscTax1Amt',
        'itemCostTaxRate1',
        'itemCostTaxRate2',
        'recognizedRevenue',
        'shippingCost',
        'shippingTax1Rate',
        'subTotal',
        'tax2Total',
        'taxRate',
        'taxTotal',
        'timeDiscAmount',
        'timeDiscTax1Amt',
        'timeTaxRate1',
        'timeTaxRate2',
        'total',
        'totalCostEstimate',
        'authCode',
        'ccName',
        'ccNumber',
        'ccSecurityCode',
        'ccStreet',
        'ccZipCode',
        'contribPct',
        'currencyName',
        'debitCardIssueNo',
        'discountRate',
        'email',
        'expCostDiscRate',
        'fax',
        'fob',
        'handlingTax2Rate',
        'itemCostDiscRate',
        'linkedTrackingNumbers',
        'memo',
        'message',
        'otherRefNum',
        'paypalAuthId',
        'payPalStatus',
        'payPalTranId',
        'pnRefNum',
        'shippingTax2Rate',
        'source',
        'status',
        'threeDStatusCode',
        'timeDiscRate',
        'trackingNumbers',
        'tranId',
        'vatRegNum',
        'itemList'
    ]

    READ_ONLY_FIELDS = [
        'createdDate',
        'lastModifiedDate',
        'subTotal',
        'tranId',
        'discountTotal',
        'giftCertApplied',
        'total',
        'exchangeRate'
    ]

    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='CashSale')

    def get_for_customer(self, customer_id):

        rref = self.ns_client.RecordRef(**({'externalId': str(customer_id), 'type': 'customer'}))
        search_field = self.ns_client.SearchMultiSelectField(searchValue=[rref], operator="anyOf")
        record_field = self.ns_client.SearchEnumMultiSelectField(searchValue="_cashSale", operator="anyOf")
        bs = self.ns_client.basic_search_factory('Transaction', customer=search_field, type=record_field)

        paginated_search = PaginatedSearch(client=self.ns_client,
                                            type_name='Transaction',
                                            basic_search=bs,
                                            pageSize=20)
        return self._paginated_search_to_generator(paginated_search=paginated_search)

    def delete(self, internalId):
        return super().delete('cashSale', internalId)

    def post(self, data) -> OrderedDict:

        cash_sale = self.ns_client.CashSale(externalId=data.externalId)

        self.build_simple_fields(self.SIMPLE_FIELDS, data, cash_sale)

        self.build_record_ref_fields(self.RECORD_REF_FIELDS, data, cash_sale)

        self.remove_readonly(cash_sale, self.READ_ONLY_FIELDS)

        logger.debug('able to create customer = %s', cash_sale)
        res = self.ns_client.upsert(cash_sale)
        return self._serialize(res)
