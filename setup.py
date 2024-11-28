from setuptools import setup, find_packages

setup(
    name="ettayi",
    version="1.0.0",
    author="Your Name",
    author_email="your_email@example.com",
    description="Ettayi Language Interpreter",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourgithubusername/ettayi",  # Update with your GitHub repo
    packages=find_packages(),
    install_requires=["lark-parser>=0.12.0"],  # Add other dependencies if needed
    entry_points={
        "console_scripts": [
            "ettayi=ettayi.cli:main",  # Maps the `ettayi` command to `main` in cli.py
        ],
    },
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
