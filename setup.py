from setuptools import setup, find_packages

setup(
    name='scaffy',
    version='0.0.0',
    description='Simple but powerful creator of directory structures based on templates',
    long_description='Read the README',
    author='Federico Stra',
    author_email='stra.federico@gmail.com',
    packages=find_packages(),
    install_requires=[
        'appdirs>=1.4.3',
        'PyYAML'],
    extras_require={
        'test': ['coverage']
    },
    entry_points={
        'console_scripts': [
            'scaffy=scaffy:main',
        ],
    },
)
