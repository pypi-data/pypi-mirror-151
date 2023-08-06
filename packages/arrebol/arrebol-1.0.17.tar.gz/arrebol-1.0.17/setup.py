from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

requirements = [
    #'pycep_correios>=5.0.0',
    'requests>=2.10.1',
]

VERSION = (1, 0, 17)     # (1, 0, 7, 'dev0')
__version__ = '.'.join(map(str, VERSION))

setup(
    name='arrebol',  # Nome (não precisa ser o nome do repositório, nem de qualquer pasta...)
    version=__version__,
    author='Michel Metran',
    author_email='michelmetran@gmail.com',
    description='Test Conda',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/traquitanas/arrebol',
    package_dir = {'': 'src'}, # Our packages live under src but src is not a package itself
    packages=find_packages('src', exclude=['test']),
    install_requires=requirements,
    keywords='python, endereço aleatorio, address',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: Portuguese',
        'Intended Audience :: Developers',
    ],
)
