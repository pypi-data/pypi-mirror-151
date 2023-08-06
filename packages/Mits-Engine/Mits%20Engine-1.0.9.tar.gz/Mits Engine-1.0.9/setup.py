from setuptools import setup

setup(
    name="Mits Engine",
    version="1.0.9",
    description="Read the latest Real Python tutorials",
    long_description="https://github.com/mbcraft-exe/MitsEngine/blob/main/Mits%20Engine-1.0.2.tar.gz",
    long_description_content_type="text/markdown",
    url="https://github.com/mbcraft-exe/MitsEngine",
    author="MB Craft",
    author_email="mbcraft@orange.fr",
    license="MB INC",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["engine"],
    install_requires=["colorama"],
    entry_points={
        "console_scripts": [
            "mits=engine.__main__:code",
        ]
    },
)