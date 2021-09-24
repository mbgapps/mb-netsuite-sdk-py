from .base import ApiBase
from netsuitesdk.internal.utils import PaginatedSearch
import logging

logger = logging.getLogger(__name__)

class CashSales(ApiBase):

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
