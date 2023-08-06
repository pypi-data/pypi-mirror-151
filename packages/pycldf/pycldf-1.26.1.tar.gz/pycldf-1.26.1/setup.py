from setuptools import setup, find_packages


setup(
    name='pycldf',
    version='1.26.1',
    author='Robert Forkel',
    author_email='robert_forkel@eva.mpg.de',
    description='A python library to read and write CLDF datasets',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords='',
    license='Apache 2.0',
    url='https://github.com/cldf/pycldf',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'cldf=pycldf.__main__:main',
        ],
    },
    platforms='any',
    python_requires='>=3.7',
    install_requires=[
        'csvw>=1.10',
        'clldutils>=3.9',
        'uritemplate>=3.0',
        'python-dateutil',
        'pybtex',
    ],
    extras_require={
        'catalogs': [
            'cldfcatalog',
            'pyglottolog',
            'pyconcepticon',
        ],
        'dev': ['tox', 'flake8', 'wheel>=0.36', 'twine'],
        'test': [
            'cldfcatalog',
            'pyglottolog',
            'pyconcepticon',
            'pytest>=5',
            'pytest-mock',
            'pytest-cov',
            'coverage>=4.2',
        ],
        'docs': [
            'sphinx',
            'sphinx-autodoc-typehints',
            'sphinx-rtd-theme',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
