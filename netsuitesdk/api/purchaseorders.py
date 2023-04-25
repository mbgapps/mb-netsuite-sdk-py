from collections import OrderedDict
from sqlite3.dbapi2 import Date

from .base import ApiBase
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class PurchaseOrders(ApiBase):

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
        'approvalStatus',
        'billAddressList',
        'class',
        'createdFrom',
        'currency',
        'customForm',
        'department',
        'employee',
        'entity',
        'intercoTransaction',
        'location',
        'nextApprover',
        'purchaseContract',
        'shipAddressList',
        'shipMethod',
        'shipTo',
        'subsidiary',
        'terms',
    ]

    SIMPLE_FIELDS = [
        'shipIsResidential',
        'supervisorApproval',
        'toBeEmailed',
        'toBeFaxed',
        'toBePrinted',
        'createdDate',
        'dueDate',
        'lastModifiedDate',
        'shipDate',
        'tranDate',
        'availableVendorCredit',
        'exchangeRate',
        'subTotal',
        'tax2Total',
        'taxTotal',
        'total',
        'currencyName',
        'email',
        'fax',
        'fob',
        'linkedTrackingNumbers',
        'memo',
        'message',
        'otherRefNum'
        'source',
        'status',
        'trackingNumbers',
        'tranId',
        'vatRegNum',
        'itemList',
    ]

    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='PurchaseOrder')

    def post(self, data) -> OrderedDict:

        purchase_order = self.ns_client.PurchaseOrder(externalId=data['externalId'])

        self.build_simple_fields(self.SIMPLE_FIELDS, data, purchase_order)

        self.build_record_ref_fields(self.RECORD_REF_FIELDS, data, purchase_order)
    
        self.build_custom_fields(data, purchase_order)

        self.remove_readonly(purchase_order, self.READ_ONLY_FIELDS)

        logger.debug('able to create po = %s', purchase_order)
        res = self.ns_client.upsert(purchase_order)
        return self._serialize(res)