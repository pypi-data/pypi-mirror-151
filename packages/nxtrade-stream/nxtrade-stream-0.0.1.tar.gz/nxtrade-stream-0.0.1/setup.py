import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nxtrade-stream",
    version="0.0.1",
    license='MIT',
    author="Dhanasekaran",
    author_email="dhanasekaran.sj@iouring.com",
    description="Iouring nxtrade test",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
          'websocket-client',
    ],
)