from setuptools import setup, find_packages

# python setup.py check
# python setup.py sdist
# or python setup.py sdist --format=zip
# twine upload dist/crazy-*.tar.gz

setup(
    name="crazy",
    version="0.0.2",
    keywords=["dao", "mysql"],
    description="crazy simple and powerful",
    long_description="crazy simple and powerful",
    long_description_content_type='text/markdown',
    python_requires=">=3.5.0",
    license="MIT Licence",
    author="Daqian",
    author_email="daqian.zhang@adalytyx.ai",
    url="https://adalytyx.ai",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'redis',
        'PyMySQL',
        'DBUtils',
        'cryptography'
    ],
    platforms="any",
    scripts=[],
    zip_safe=False

)
