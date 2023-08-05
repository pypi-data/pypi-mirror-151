import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mopa",
    version="0.2.3b0",
    author="Jacob Kravits",
    author_email="kravitsjacob@gmail.com",
    description="Library for interactive multi-objective power amplifier design",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kravitsjacob/mopa",
    project_urls={
        "Bug Tracker": "https://github.com/kravitsjacob/mopa/issues",
    },
    install_requires=[
        'pandas',
        'hiplot',
        'dash',
        'dash-bootstrap-components'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
)
