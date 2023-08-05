# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['minswap_oura']

package_data = \
{'': ['*']}

install_requires = \
['blockfrost-python==0.4.4']

setup_kwargs = {
    'name': 'minswap-oura',
    'version': '0.1.1',
    'description': '',
    'long_description': '# Translated to python from JS, source: https://github.com/minswap/blockfrost-adapter/blob/main/README.md?plain=1\n\nModified to work with Oura and mongoDB\n- [x] Get current pair price\n- [ ] Get historical pair price\n\n\n# Minswap Blockfrost Adapter\n\n## Features\n\n- [x] Get current pair price\n- [x] Get historical pair price\n- [ ] Calculate trade price and price impact\n- [ ] Create orders and submit to Blockfrost\n\n## Install\n\n- Pypi: `pip install minswap`\n\n## Examples\n\n### Example 1: Get current price of MIN/ADA pool\n\n```python\nfrom minswap import BlockfrostAdapter, NetworkId\n\nadapter = BlockfrostAdapter(\n  projectId="<your_project_id>",\n  networkId=NetworkId.MAINNET,\n)\n\npage = 1\nwhile True:\n    pools = adapter.getPools(page=page)\n\n    if len(pools) == 0:\n        # last page\n        break\n\n    minAdaPool = next((pool for pool in pools if pool.assetA == "lovelace" and pool.assetB=="29d222ce763455e3d7a09a665ce554f00ac89d2e99a1a83d267170c64d494e"), None)\n\n    if minAdaPool:\n        min, ada = adapter.getPoolPrice(pool=minAdaPool)\n        print(f\'ADA/MIN price: {min}; MIN/ADA price: {ada}\')\n        print(f\'ADA/MIN pool ID: {minAdaPool.id}\')\n        break\n\n```\n\n### Example 2: Get historical prices of MIN/ADA pool\n\n```python\nfrom minswap import BlockfrostAdapter, NetworkId\n\nadapter = BlockfrostAdapter(\n  projectId="<your_project_id>",\n  networkId=NetworkId.MAINNET,\n)\n\nMIN_ADA_POOL_ID = "6aa2153e1ae896a95539c9d62f76cedcdabdcdf144e564b8955f609d660cf6a2"\n\nhistory = adapter.getPoolHistory(id=MIN_ADA_POOL_ID)\n\nfor historyPoint in history:\n    pool = adapter.getPoolInTx(txHash=historyPoint.txHash)\n    if not pool:\n        raise Exception("pool not found")\n    \n    price0, price1 = adapter.getPoolPrice(\n        pool,\n        decimalsA=6,\n        decimalsB=6,\n    )\n    print(f\'{historyPoint.time}: {price0} ADA/MIN, {price1} MIN/ADA`)\n\n```',
    'author': 'Samuel Ostholm',
    'author_email': 'kalltrum@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sostholm/minswap',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
