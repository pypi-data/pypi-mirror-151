'notypebuiltins package loader.'
__all__ = ['load']

def load():
    'Load the libraries from CPython Github repository. Then cache it to notypebuiltins.Lib'
    from . import log
    from os.path import isdir, dirname
    notypebuiltins_directory = dirname(__file__)

    if isdir(notypebuiltins_directory + '\\Lib'):
        log.info('Already exists.')
        return None
    from sys import version_info
    version_info = 'v' + str(version_info.major) + '.' + str(version_info.minor) + '.' + str(version_info.micro)
    log.info('Python version: %r'%version_info)
    version_info_raw = version_info[1:]
    log.info('Python raw version info: %r'%version_info_raw)

    from urllib.request import urlretrieve, urlopen

    url = 'https://github.com/python/cpython/releases/tag/{}'.format(version_info)
    log.info('Download from %r'%url)

    try:
        response = urlopen(url)
    except:
        log.info('Unexpected error occoured.')
        raise RuntimeError('Unsupported version: %r'%version_info)

    text = response.read().decode() # type: ignore
    
    archive_url = '/python/cpython/archive/refs/tags/{}.zip'.format(version_info)

    if archive_url not in text:
        raise RuntimeError('Unsupported version: %r'%version_info)

    archive_url = 'https://github.com{}'.format(archive_url)

    try:
        response = urlretrieve(archive_url)
    except:
        raise TypeError('Can\'t download source code from python github repository.')

    file = response[0]

    from zipfile import ZipFile
    from shutil import move, rmtree

    with ZipFile(file, 'r', allowZip64=True) as zipfile:
        zipfile.extractall(notypebuiltins_directory)

    zipfile.close()

    log.info('Moving file to notypebuiltins.Lib')
    move('%s\\cpython-%s\\Lib'%(notypebuiltins_directory, version_info_raw), notypebuiltins_directory + '\\Lib')
    rmtree('%s\\cpython-%s'%(notypebuiltins_directory, version_info_raw))

    from os import listdir

    with open('%s\\Lib\\__init__.py'%notypebuiltins_directory, 'a+', encoding='utf-8') as init_file:
        for file in listdir('%s\\Lib'%notypebuiltins_directory):
            if file in ('site-packages', '__phello__.foo.py'): # avoid errors
                continue
            if file.endswith('.py'):
                file = file[:-3]

            if file in ('this', '__phello__', 'antigravity'): # avoid easter eggs. But you can import it.
                continue

            log.info('Write module %r'%file)
            init_file.write('\ntry:\n\tfrom . import {}\nexcept:\n\tpass'.format(file))

    with open('%s\\Lib\\py.typed'%notypebuiltins_directory, 'w') as file:
        empty = ''
        file.write(empty)
    file.close()

    return None