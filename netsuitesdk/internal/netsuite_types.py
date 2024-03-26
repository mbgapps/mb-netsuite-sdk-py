"""
Declares all NetSuite types which are available through attribute lookup `ns.<type>`
of a :class:`~netsuitesdk.client.NetSuiteClient` instance `ns`.
"""

COMPLEX_TYPES = {
    'ns0': [
        'BaseRef',
        'GetAllRecord',
        'GetAllResult',
        'Passport',
        'RecordList',
        'RecordRef',
        'ListOrRecordRef',
        'SearchResult',
        'SearchEnumMultiSelectField',
        'SearchStringField',
        'SearchMultiSelectField',
        'SearchDateField',
        'SearchLongField',
        'Status',
        'StatusDetail',
        'TokenPassport',
        'TokenPassportSignature',
        'WsRole',
        'DateCustomFieldRef',
        'CustomFieldList',
        'DoubleCustomFieldRef',
        'StringCustomFieldRef',
        'CustomRecordRef',
        'SelectCustomFieldRef',
        'BooleanCustomFieldRef',
        'InitializeRecord',
        'InitializeRef'
    ],

    # ns4: https://webservices.netsuite.com/xsd/platform/v2017_2_0/messages.xsd
    'ns4': [
        'ApplicationInfo',
        'GetAllRequest',
        'GetRequest',
        'GetResponse',
        'GetAllResponse',
        'PartnerInfo',
        'ReadResponse',
        'SearchPreferences',
        'SearchResponse',
        'DeleteRequest',
        'DeleteListRequest',
        'InitializeRequest'
    ],

    # https://webservices.netsuite.com/xsd/platform/v2017_2_0/common.xsd
    'ns5': [
        'AccountSearchBasic',
        'Address',
        'CustomerSearchBasic',
        'JobSearchBasic',
        'LocationSearchBasic',
        'TransactionSearchBasic',
        'VendorSearchBasic',
        'SubsidiarySearchBasic',
        'EmployeeSearchBasic',
        'FolderSearchBasic',
        'FileSearchBasic',
        'CustomRecordSearchBasic',
        'CustomListSearchBasic',
        'TermSearchBasic',
    ],

    # urn:relationships.lists.webservices.netsuite.com
    'ns13': [
        'CustomerAddressbook', 'CustomerAddressbookList',
        'Customer', 'CustomerSearch',
        'Vendor', 'VendorSearch',
        'Job', 'JobSearch',
        'VendorAddressbook', 'VendorAddressbookList',
    ],

    # urn:accounting_2017_2.lists.webservices.netsuite.com
    # https://webservices.netsuite.com/xsd/lists/v2017_2_0/accounting.xsd
    'ns17': [
        'Account', 'AccountSearch',
        'ExpenseCategory', 'ExpenseCategorySearch',
        'AccountingPeriod',
        'Classification', 'ClassificationSearch',
        'Department', 'DepartmentSearch',
        'Location', 'LocationSearch',
        'Subsidiary', 'SubsidiarySearch',
        'VendorCategory', 'VendorCategorySearch',
        'Term', 'TermSearch','InventoryItem',
        'InventoryItemBinNumber','InventoryItemBinNumberList'

    ],

    'ns19': [
        'Invoice',
        'InvoiceItem',
        'InvoiceItemList',
        'TransactionSearch',
        'ItemFulfillment',
        'SalesOrder',
        'SalesOrderItem',
        'SalesOrderItemList',
        'CashSale'
    ],

    # urn:purchases_2017_2.transactions.webservices.netsuite.com
    # https://webservices.netsuite.com/xsd/transactions/v2017_2_0/purchases.xsd
    'ns21': [
        'VendorBill',
        'VendorBillExpense',
        'VendorBillExpenseList',
        'VendorBillItem',
        'VendorBillItemList',
        'VendorPayment',
        'VendorPaymentApplyList',
        'VendorPaymentCredit',
        'VendorPaymentCreditList',
        'VendorPaymentApply',
        'PurchaseOrder',
        'ItemReceipt',
        'PurchaseOrderItemList'
    ],

    # urn:customers_2019_1.transactions.webservices.netsuite.com
    'ns23': [
        'CustomerRefund', 'CustomerRefundApply', 'CustomerRefundApplyList', 'CustomerRefundDeposit',
        'CustomerRefundDepositList', 'CustomerDeposit', 'CustomerDepositApply', 'CustomerDepositApplyList',
        'CashRefund'
    ],

    # urn:general_2019_2.transactions.webservices.netsuite.com
    # https://webservices.netsuite.com/xsd/transactions/v2019_2_0/general.xsd
    'ns31': [
        'JournalEntry',
        'JournalEntryLine',
        'JournalEntryLineList',
    ],

    'ns32': [
        'CustomRecord',
        'CustomRecordCustomField',
        'CustomRecordSearch',
        'CustomListSearch',
        'CustomRecordType'
    ],

    # https://webservices.netsuite.com/xsd/lists/v2019_2_0/employees.xsd
    'ns34': [
        'EmployeeSearch',
        'Employee'
    ],

    # urn:employees_2019_2.transactions.webservices.netsuite.com
    # https://webservices.netsuite.com/xsd/transactions/v2019_2_0/employees.xsd
    'ns38': [
        'ExpenseReport',
        'ExpenseReportExpense',
        'ExpenseReportExpenseList',
    ],
    'ns11': [
        'FolderSearch',
        'Folder',
        'File',
        'FileSearch'
    ],

    # urn:inventory_2023_2.transactions.webservices.netsuite.com
    # https://webservices.netsuite.com/xsd/transactions/v2023_2_0/inventory.xsd
    'ns29': [
        'TransferOrder',
        'TransferOrderItem',
        'TransferOrderItemList',
    ],
}

SIMPLE_TYPES = {
    # ns1: view-source:https://webservices.netsuite.com/xsd/platform/v2017_2_0/coreTypes.xsd
    'ns1': [
        'RecordType',
        'GetAllRecordType',
        'SearchRecordType',
        'SearchEnumMultiSelectFieldOperator',
        'SearchStringFieldOperator',
        'SearchDateFieldOperator',
        'SearchLongFieldOperator'
    ],
}



# NAMESPACES from NS with correct prefix
# {
#     'xsd': 'http://www.w3.org/2001/XMLSchema', 
#     'ns0': 'urn:core_2023_2.platform.webservices.netsuite.com', 
#     'ns1': 'urn:types.core_2023_2.platform.webservices.netsuite.com', 
#     'ns2': 'urn:types.faults_2023_2.platform.webservices.netsuite.com', 
#     'ns3': 'urn:faults_2023_2.platform.webservices.netsuite.com', 
#     'ns4': 'urn:messages_2023_2.platform.webservices.netsuite.com', 
#     'ns5': 'urn:common_2023_2.platform.webservices.netsuite.com', 
#     'ns6': 'urn:types.common_2023_2.platform.webservices.netsuite.com', 
#     'ns7': 'urn:scheduling_2023_2.activities.webservices.netsuite.com', 
#     'ns8': 'urn:types.scheduling_2023_2.activities.webservices.netsuite.com', 
#     'ns9': 'urn:communication_2023_2.general.webservices.netsuite.com', 
#     'ns10': 'urn:types.communication_2023_2.general.webservices.netsuite.com', 
#     'ns11': 'urn:filecabinet_2023_2.documents.webservices.netsuite.com', 
#     'ns12': 'urn:types.filecabinet_2023_2.documents.webservices.netsuite.com', 
#     'ns13': 'urn:relationships_2023_2.lists.webservices.netsuite.com', 
#     'ns14': 'urn:types.relationships_2023_2.lists.webservices.netsuite.com', 
#     'ns15': 'urn:support_2023_2.lists.webservices.netsuite.com', 
#     'ns16': 'urn:types.support_2023_2.lists.webservices.netsuite.com', 
#     'ns17': 'urn:accounting_2023_2.lists.webservices.netsuite.com', 
#     'ns18': 'urn:types.accounting_2023_2.lists.webservices.netsuite.com', 
#     'ns19': 'urn:sales_2023_2.transactions.webservices.netsuite.com', 
#     'ns20': 'urn:types.sales_2023_2.transactions.webservices.netsuite.com', 
#     'ns21': 'urn:purchases_2023_2.transactions.webservices.netsuite.com', 
#     'ns22': 'urn:types.purchases_2023_2.transactions.webservices.netsuite.com', 
#     'ns23': 'urn:customers_2023_2.transactions.webservices.netsuite.com', 
#     'ns24': 'urn:types.customers_2023_2.transactions.webservices.netsuite.com', 
#     'ns25': 'urn:financial_2023_2.transactions.webservices.netsuite.com', 
#     'ns26': 'urn:types.financial_2023_2.transactions.webservices.netsuite.com', 
#     'ns27': 'urn:bank_2023_2.transactions.webservices.netsuite.com',
#     'ns28': 'urn:types.bank_2023_2.transactions.webservices.netsuite.com', 
#     'ns29': 'urn:inventory_2023_2.transactions.webservices.netsuite.com', 
#     'ns30': 'urn:types.inventory_2023_2.transactions.webservices.netsuite.com', 
#     'ns31': 'urn:general_2023_2.transactions.webservices.netsuite.com', 
#     'ns32': 'urn:customization_2023_2.setup.webservices.netsuite.com', 
#     'ns33': 'urn:types.customization_2023_2.setup.webservices.netsuite.com', 
#     'ns34': 'urn:employees_2023_2.lists.webservices.netsuite.com', 
#     'ns35': 'urn:types.employees_2023_2.lists.webservices.netsuite.com', 
#     'ns36': 'urn:website_2023_2.lists.webservices.netsuite.com', 
#     'ns37': 'urn:types.website_2023_2.lists.webservices.netsuite.com', 
#     'ns38': 'urn:employees_2023_2.transactions.webservices.netsuite.com', 
#     'ns39': 'urn:types.employees_2023_2.transactions.webservices.netsuite.com', 
#     'ns40': 'urn:marketing_2023_2.lists.webservices.netsuite.com', 
#     'ns41': 'urn:types.marketing_2023_2.lists.webservices.netsuite.com', 
#     'ns42': 'urn:demandplanning_2023_2.transactions.webservices.netsuite.com', 
#     'ns43': 'urn:types.demandplanning_2023_2.transactions.webservices.netsuite.com', 
#     'ns44': 'urn:supplychain_2023_2.lists.webservices.netsuite.com', 
#     'ns45': 'urn:types.supplychain_2023_2.lists.webservices.netsuite.com'
# }
