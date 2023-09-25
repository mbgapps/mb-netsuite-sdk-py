import setuptools
from version import VERSION


with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='mbnetsuitesdk',
    version=VERSION,
    author='Monolith Brands',
    author_email='support@monolithbrands.com',
    description='Python SDK for accessing the NetSuite SOAP webservice',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['netsuite', 'api', 'python', 'sdk'],
    url='https://github.com/mbgapps/mb-netsuite-sdk-py',
    packages=setuptools.find_packages(),
    install_requires=['zeep'],
    classifiers=[
        'Topic :: Internet :: WWW/HTTP',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
