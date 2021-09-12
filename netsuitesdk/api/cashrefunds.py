from collections import OrderedDict

from .base import ApiBase
import logging

logger = logging.getLogger(__name__)

class CashRefunds(ApiBase):
    SIMPLE_FIELDS = [
        'ccApproved',
        'ccIsPurchaseCardBin',
        'ccProcessAsPurchaseCard',
        'chargeIt',
        'excludeCommission',
        'isTaxable',
        'payPalProcess',
        'refundCheck',
        'revRecOnRevCommitment',
        'syncPartnerTeams',
        'syncSalesTeams',
        'taxDetailsOverride',
        'taxRegOverride',
        'toBeEmailed',
        'toBeFaxed',
        'toBePrinted',
        'toPrint2',
        'tranIsVsoeBundle',
        'vsoeAutoCalc',
        'createdDate',
        'lastModifiedDate',
        'salesEffectiveDate',
        'taxPointDate',
        'tranDate',
        'validFrom',
        'altHandlingCost',
        'altShippingCost',
        'deferredRevenue',
        'discountTotal',
        'estGrossProfit',
        'estGrossProfitPercent',
        'exchangeRate',
        'giftCertApplied',
        'giftCertAvailable',
        'giftCertTotal',
        'handlingCost',
        'handlingTax1Rate',
        'recognizedRevenue',
        'shippingCost',
        'shippingTax1Rate',
        'subTotal',
        'tax2Total',
        'taxRate',
        'taxTotal',
        'total',
        'totalCostEstimate',
        'ccName',
        'ccNumber',
        'ccStreet',
        'ccZipCode',
        'checkNumber',
        'contribPct',
        'currencyName',
        'debitCardIssueNo',
        'discountRate',
        'dynamicDescriptor',
        'email',
        'fax',
        'handlingTax2Rate',
        'inputAuthCode',
        'inputReferenceCode',
        'memo',
        'message',
        'otherRefNum',
        'outputAuthCode',
        'outputReferenceCode',
        'paymentCardCsc',
        'payPalAuthId',
        'payPalStatus',
        'payPalTranId',
        'pnRefNum',
        'shippingTax2Rate',
        'source',
        'status',
        'tranId',
        'vatRegNum'  
    ]

    RECORD_REF_FIELDS = [
        'account',
        'billAddressList',
        'class',
        'createdFrom',
        'creditCard',
        'creditCardProcessor',
        'currency',
        'customForm',
        'department',
        'discountItem',
        'entity',
        'entityTaxRegNum',
        'giftCert',
        'handlingTaxCode',
        'job',
        'leadSource',
        'location',
        'messageSel',
        'nexus',
        'partner',
        'paymentMethod',
        'paymentOption',
        'paymentProcessingProfile',
        'postingPeriod',
        'promoCode',
        'salesGroup',
        'salesRep',
        'shipMethod',
        'shippingTaxCode',
        'subsidiary',
        'subsidiaryTaxRegNum',
        'taxItem',
    ]

    READ_ONLY_FIELDS = ['internalId', 'balance', 'overdueBalance', 'representingSubsidiary',
                        'monthlyClosing', 'balance', 'overdueBalance', 'unbilledOrders', 'depositBalance',
                        'aging', 'aging1', 'aging2', 'aging3', 'aging4', 'lastModifiedDate', 'dateCreated',
                        'defaultAddress', 'entityStatus', 'receivablesAccount',
                        'currencyList']


    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='CashRefund')

    def blank(self, externalId) -> OrderedDict:

        blank = OrderedDict()
        blank.externalId = externalId
        blank.customFieldList = self.ns_client.CustomFieldList([])
        blank.subsidiary = self.ns_client.RecordRef(**({'internalId': '2'}))
        blank.account = self.ns_client.RecordRef(**({'internalId': '1'}))
        blank.paymentMethod = self.ns_client.RecordRef(**({'internalId': '1'}))

        return blank

    def post(self, data) -> OrderedDict:

        cashrefund = self.ns_client.CashRefund(externalId=data.externalId)

        self.build_simple_fields(self.SIMPLE_FIELDS, data, cashrefund)

        self.build_record_ref_fields(self.RECORD_REF_FIELDS, data, cashrefund)

        self.build_custom_fields(data, cashrefund)

        self.remove_readonly(cashrefund,self.READ_ONLY_FIELDS)

        if hasattr(data, 'itemList'):
            cashrefund.itemList = data.itemList

        logger.debug('able to create customer = %s', cashrefund)
        res = self.ns_client.upsert(cashrefund)
        return self._serialize(res)
