import setuptools
import pathlib
from qbeast.utils import __version__

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setuptools.setup(
    name="qbeast-cli",
    version=__version__,
    author="Qbeast",
    description="A command line interface for qbeast-sharing",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "qbeast = qbeast.main:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=["click", "requests"]
)
