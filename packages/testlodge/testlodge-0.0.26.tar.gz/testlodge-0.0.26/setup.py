import setuptools


with open('README.md', 'r') as fin:
    long_description = fin.read()


setuptools.setup(
    name='testlodge',
    version='0.0.26',
    author='Kyle L. Davis',
    author_email='AceofSpades5757.github@gmail.com',
    url='https://github.com/AceofSpades5757/testlodge',
    license='MIT',
    description='Python client library for interacting with TestLodge.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src', 'testlodge': 'src/testlodge'},
    test_suite="tests",
    python_requires='>=3.8',
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: MIT License',
        "Operating System :: OS Independent",
    ],
)
