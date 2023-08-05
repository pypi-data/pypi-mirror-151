from setuptools import setup, find_packages

with open('README.md', 'r') as file:
    desc = file.read()

setup(
    name='paleocirc',
    packages=find_packages(include=['paleocirc']),
    url='https://github.com/xFranciB/paleocirc',
    download_url='https://github.com/xFranciB/paleocirc/archive/refs/tags/v1.1.2.tar.gz',
    version='1.1.2',
    description='API web scraping per ottenere circolari dal sito dell\'I.T.I.S. Paleocapa di Bergamo',
    author='xFranciB',
    license='MIT',
    long_description=desc,
    long_description_content_type='text/markdown',
    install_requires=['requests', 'aiohttp', 'asyncio', 'beautifulsoup4', 'pdf2image', 'pywin32']
)