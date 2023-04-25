from lxml import etree
from zeep import Plugin

class LoggingPlugin(Plugin):

    def ingress(self, envelope, http_headers, operation):
        print('response!')
        return envelope, http_headers

    def egress(self, envelope, http_headers, operation, binding_options):
        print('request!')
        return envelope, http_headers
