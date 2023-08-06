import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="stocklib",
    version="2.1.1",
    description="Get real-time stock data!",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/SammmE/StockLib",
    author="SammmE",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    packages=["stocklib"],
    include_package_data=True,
    install_requires=["beautifulsoup4", "requests"],
)
