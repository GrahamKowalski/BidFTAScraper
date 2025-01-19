from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="BidFTAScraper",
    version="0.1.0",
    author="Graham Kowalski",
    description="A scraper for BidFTA.com auction listings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GrahamKowalski/BidFTAScraper",
    packages=find_packages(exclude=["tests*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "beautifulsoup4>=4.9.0",
        "pandas>=1.2.0"
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "flake8>=3.9.0",
            "black>=21.0",
            "mypy>=0.900"
        ]
    }
)