from setuptools import setup, find_packages

setup(
    name="ettayi",
    version="1.0.3",
    author="Apollo-Blaze",
    author_email="srichandsureshrocks@gmail.com",
    description="Ettayi Lang",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Apollo-Blaze/ettayi",  
    packages=find_packages(),
    install_requires=["lark-parser>=0.12.0"],  # Add other dependencies if needed
    entry_points={
        "console_scripts": [
            "ettayi=ettayi.cli:main",  
        ],
    },
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
