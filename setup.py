from setuptools import setup, find_packages

setup(
    name="game-ping-optimizer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "psutil>=5.9.6",
        "numpy>=1.26.2",
        "matplotlib>=3.8.2",
        "requests>=2.31.0",
    ],
    entry_points={
        "console_scripts": [
            "game-ping-optimizer=src.main:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool for monitoring and optimizing game server ping",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/game-ping-optimizer",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
)
