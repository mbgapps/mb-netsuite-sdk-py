from netsuitesdk.internal.utils import PaginatedSearch
from .base import ApiBase
import logging

logger = logging.getLogger(__name__)

class CustomerDeposits(ApiBase):

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
