from collections import OrderedDict

from .base import ApiBase
import logging
from netsuitesdk.internal.exceptions import NetSuiteRequestError

logger = logging.getLogger(__name__)

class TransferOrders(ApiBase):
    SIMPLE_FIELDS = [
        'tranDate',
        'itemList',
    ]

    RECORD_REF_FIELDS = [
        'subsidiary',
        'location',
        'transferLocation',
        'customForm',
    ]

    READ_ONLY_FIELDS = []

    READ_ONLY_ITEM_FIELDS = [
    ]

    SIMPLE_ITEM_FIELDS = [
        'quantityAvailable',
        'quantityOnHand',
        'quantityBackOrdered',
        'quantityCommitted',
        'quantityFulfilled',
        'quantityPacked',
        'quantityPicked',
        'quantityReceived',
        'quantity',
    ]

    RECORD_REF_ITEM_FIELDS = [
        'item',
    ]

    def __init__(self, ns_client):
        ApiBase.__init__(self, ns_client=ns_client, type_name='TransferOrder')

    def get_by_internal_id(self, internalId):
        return self.ns_client.get('TransferOrder', internalId=internalId)

    def get_by_external_id(self, externalId):
        return self.ns_client.get('TransferOrder', externalId=externalId)

    def post(self, externalId, data) -> OrderedDict:
        if externalId in ['', None, 0, [], {}]:
            raise ValueError("externalId is required")
        
        transfer_order = self.ns_client.TransferOrder(externalId=externalId)

        self.build_mb_simple_fields(self.SIMPLE_FIELDS, data, transfer_order)
        self.build_mb_record_ref_fields(self.RECORD_REF_FIELDS, data, transfer_order)
        self.build_mb_custom_fields(data, transfer_order)
        self.remove_readonly(transfer_order, self.READ_ONLY_FIELDS)

        if 'itemList' in data:
            items = []
            for item in data['itemList']['item']:
                wsdl_item = self.ns_client.TransferOrderItem()
                self.build_mb_simple_fields(self.SIMPLE_ITEM_FIELDS, item, wsdl_item)
                self.build_mb_record_ref_fields(self.RECORD_REF_ITEM_FIELDS, item, wsdl_item)
                self.build_mb_custom_fields(item, wsdl_item)
                items.append(wsdl_item)

            transfer_order.itemList = self.ns_client.TransferOrderItemList(item=items)

        self.ns_client.upsert(transfer_order)
        # try:
        #     exists = True
        #     self.ns_client.get('TransferOrder', externalId=externalId)
        # except NetSuiteRequestError:
        #     exists = False
        #     self.logger.warning('TransferOrder not found for externalId {} - attempting to add it'.format(externalId))
        #     # if sales order not found and the status is cancelled, just return and don't do anything
        #     # if data['orderStatus'] == '_cancelled':
        #     #     self.logger.warning('Cancelled SalesOrder not found - not adding externalId {}'.format(externalId))
        #     #     return None

        # if exists:
        #     return self.ns_client.update(transfer_order)
        # else:
        #     return self.ns_client.add(transfer_order)
