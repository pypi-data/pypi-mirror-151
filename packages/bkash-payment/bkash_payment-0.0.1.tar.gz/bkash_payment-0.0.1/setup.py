import setuptools


requires = [
    'astroid==2.3.3',
    'certifi==2019.11.28',
    'chardet==3.0.4',
    'idna==2.8',
    'isort==4.3.21',
    'lazy-object-proxy==1.4.3',
    'mccabe==0.6.1',
    'requests==2.22.0',
    'six==1.13.0',
    'typed-ast',
    'urllib3==1.25.7',
    'wrapt==1.11.2'
]

setuptools.setup(
    name="bkash_payment",
    version="0.0.1",
    author="V3n0m",
    author_email="asfrabi15@gmail.com",
    description="Implements SSLCOMMERZ payment gateway in python based web apps.",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)