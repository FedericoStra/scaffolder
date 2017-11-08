from setuptools import setup, find_packages

setup(
    name='scaffy',
    version='0.0.0',
    description='Simple creator of directory structures',
    long_description='Read the README',
    author='Federico Stra',
    author_email='stra.federico@gmail.com',
    packages=find_packages(),
    install_requires=['PyYAML'],
    extras_require={
        'test': ['coverage']
    },
    entry_points={
        'console_scripts': [
            'scaffy=scaffy:main',
        ],
    },
    )
