from setuptools import setup, find_packages

setup(
    name="geometry",
    version="1.0.0",
    description="Probabilistic study of random point sampling on a square perimeter",
    author="gagli",
    python_requires=">=3.8",
    packages=find_packages(exclude=["tests*", ".venv*"]),
    install_requires=[
        "colorama>=0.4.6",
    ],
    extras_require={
        "dev": ["pytest>=7.0"],
    },
)
