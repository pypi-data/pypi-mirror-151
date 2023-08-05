from setuptools import setup

setup(
    name='notypebuiltins',
    version='1.0.0',
    description='Load not typed modules from cpython github repository.',
    long_description='# Example\n```python\nimport notypebuiltins\nnotypebuiltins.loader.load()\nfrom notypebuiltins.Lib import abc\n```',
    long_description_content_type='text/markdown',
    packages=['notypebuiltins'],
    author='LUA9',
    maintainer='LUA9'
)