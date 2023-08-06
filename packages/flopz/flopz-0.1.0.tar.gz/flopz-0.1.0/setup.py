
from setuptools import setup, find_packages

setup(
    name='flopz',
    version='0.1.0',
    packages=find_packages(),
    url='https://github.com/Flopz-Project/flopz',
    license='Apache License',
    author='Noelscher Consulting GmbH',
    author_email='ferdinand@noelscher.com',
    description='flopz - Low Level Assembler and Firmware Instrumentation Toolkit',
    install_requires=['bitstring'],

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: iOS',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.7',
    ],
)
