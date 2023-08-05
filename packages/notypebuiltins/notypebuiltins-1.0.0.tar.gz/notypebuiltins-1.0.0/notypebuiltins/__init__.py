'''
Before you use this package, please follow this code and then import it.
```python
import notypebuiltins
notypebuiltins.loader.load() # It loads all of cpython packages.
```
'''
__all__ = ['loader']
log = __import__('logging').getLogger(__name__)

from . import loader

try:
    from . import Lib # type: ignore
    __all__.append('Lib')
except:
    pass