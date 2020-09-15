
from datetime import datetime, timezone
import setuptools

def construct_package_version():

    current_date = datetime.now(tz=timezone.utc)

    return f'{current_date.year}.{current_date.month}.{current_date.day}'

def package_details():

    package_name = 'python-windscribe'
    
    repo_url = 'https://github.com/Dayzpd/Python-Windscribe'
    
    author = 'dayzpd'
    
    package_license = 'MIT'
    
    classifiers = [
        'Intended Audience :: Developers',
        'License :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ]

    requirements = [
        'attrs>=19.0.0',
        'loguru>=0.5.0',
        'pexpect>=4.0.0',
    ]

    return {
        'author'           : author,
        'classifiers'      : classifiers,
        'license'          : package_license,
        'name'             : package_name,
        'packages'         : setuptools.find_packages(include=[ 'windscribe' ]),
        'url'              : repo_url,
        'version'          : construct_package_version(),
        'install_requires' : requirements,
    }

setuptools.setup(**package_details())