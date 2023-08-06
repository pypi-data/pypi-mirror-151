# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hugedict', 'hugedict.parallel']

package_data = \
{'': ['*']}

install_requires = \
['lbry-rocksdb-optimized>=0.8.1,<0.9.0',
 'loguru>=0.6.0',
 'orjson>=3.6.8,<4.0.0',
 'pybloomfiltermmap3>=0.5.5,<0.6.0',
 'tqdm>=4.64.0,<5.0.0',
 'zstandard>=0.17.0,<0.18.0']

setup_kwargs = {
    'name': 'hugedict',
    'version': '1.4.0',
    'description': 'A dictionary-like object that is friendly with multiprocessing and uses key-value databases (e.g., RocksDB) as the underlying storage.',
    'long_description': '# hugedict ![PyPI](https://img.shields.io/pypi/v/hugedict)\n\nA dictionary-like object that is friendly with multiprocessing and uses key-value databases (e.g., RocksDB) as the underlying storage.\n\n## Installation\n\n```bash\npip install hugedict\n```\n\n## Usage\n\n```python\nfrom hugedict.rocksdb import RocksDBDict\n\n# replace K and V for the types you are using\nmapping: Dict[K, V] = RocksDBDict(\n    dbpath,  # path to db file\n    create_if_missing=create_if_missing,  # whether to create database if missing\n    read_only=read_only,  # open database in read only mode\n    deser_key=bytes.decode,  # decode the key from bytes\n    ser_key=str.encode,  # encode the key to bytes\n    deser_value=bytes.decode,  # decode the value from bytes\n    ser_value=str.encode,  # encode the value from bytes\n    db_options=db_options,  # other rocksdb options\n)\n```\n',
    'author': 'Binh Vu',
    'author_email': 'binh@toan2.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/binh-vu/hugedict',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
