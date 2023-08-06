from setuptools import setup, find_packages

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='psaopt',
    version='0.0.1',
    packages=find_packages(),
    description='Template to register pypi.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['system', 'file', 'time'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'numpy',
        'pandas',
        'openpyxl',
        'distributed'
    ],
    python_requires='>=3.10'
)
