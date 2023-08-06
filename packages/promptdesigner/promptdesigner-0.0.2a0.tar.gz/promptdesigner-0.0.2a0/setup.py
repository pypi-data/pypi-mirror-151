from setuptools import find_packages, setup

_REQUIRED = ['openai', 'fpdf', 'Pillow', 'promptdesignerdataset']
_EXTRAS = []
setup(
    name='promptdesigner',
    version='0.0.2a',
    packages=find_packages(),
    install_requires=_REQUIRED,
    # extras_require=_EXTRAS,
    url='http://www.example.com/it',
    license='MIT',
    classifiers=[
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.9",
        ],
    author='Patrizio Bellan',
    include_package_data=True,
    long_description='this is a long description',
    long_description_content_type='text/x-rst',
    author_email='patrizio.bellan@gmail.com',
    description='my test'
)
