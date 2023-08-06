# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nemoize']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nemoize',
    'version': '0.1.0',
    'description': 'Decorator utility to memoize a class, function, or method',
    'long_description': '# nemoize\nSimple Python Memoizer decorator for classes, functions, and methods.\n\n# Installation\nnemoize is available on PyPi\n\n```commandline\npython3 -m pip install nemoize\n```\n\nOr you can install manually via the built distribution (wheel)/source dist from [PyPi](pypi.org/project/nemoize) or [github](https://github.com/spoorn/nemoize).\n\n\n# How to Use\n\nImport\n\n```python\nfrom nemoize import memoize\n```\n\nThen use the `@memoize` decorator on various entities as seen below\n\n### Using on a Class\n\n```python\n@memoize\nclass Test:\n    def __init__(self, value):\n        self._value = value\n\n    @property\n    def value(self):\n        return self._value\n```\n\n### Using on a function\n\n```python\n@memoize\ndef test_func():\n    return "hoot"\n```\n\n### Using on an instance method\n\n```python\nclass Owl:\n    def __init__(self):\n        self.food = 1337\n        pass\n\n    @memoize(max_size)\n    def eat(self, num):\n        self.food -= num\n```\n\n## Configuration\n\nThere are also various configuration parameters to `memoize()`:\n\n- `@memoize(max_size=13)` : Max number of entries to keep in the cache: \n- `@memoize(cache_exceptions=True)` : Also cache exceptions, so any raised Exceptions will be the exact same Exception instance: \n- `@memoize(max_size=13, cache_exceptions=True)` : Together\n- `@memoize(arg_hash_function=str)` : Changes the hash function on arg and each keyword-arg to use the str() function, which can make lists "hashable"\n\n# Testing\nThe unit tests in `test/unit/test_memoize.py` run through various use cases of using the @memoize annotation on classes, functions, and instance methods.\n\n# Benchmarking\nThere is a benchmarking utility under [`benchmark/`](https://github.com/spoorn/nemoize/tree/main/benchmark) that is used for benchmarking nemoize performance against other options and non-memoized scenarios.\n\nExample numbers:\n\n```commandline\nBenchmark test for Memoized vs Non-memoized classes with [1000] computations in their__init__() methods for [1000000] iterations\nNon-memoized class creation + empty method call average time (ms): 0.01550699806213379\nMemoized class creation + empty method call average time (ms): 0.0012589995861053468\n\nBenchmark test for @memoize, non-memoized, a @simplified_memoize, and @functools.lru_cache comparison usingfunction calculating fibonacci sum for [100] fib numbers, for [10000000] iterations\n@simplified_memoize fib average time (ms): 0.0001555999994277954\n@memoize fib average time (ms): 4.4699978828430175e-05\n@memoize(cache_exceptions=True) (to avoid delegation to functools.lru_cache) fib average time (ms): 0.00034309999942779544\n@functools.lru_cache fib average time (ms): 4.440000057220459e-05\n```',
    'author': 'spoorn',
    'author_email': 'spookump@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/spoorn/nemoize',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
