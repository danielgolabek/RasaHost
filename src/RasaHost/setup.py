import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rasa-host",
    version="0.3.0",
    author="Daniel Golabek",
    author_email="daniel.golabek@gmail.com",
    description="UI for Rasa",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danielgolabek/RasaHost",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "Flask",
        "Flask-SocketIO",
        "SQLAlchemy",
        "urllib3",
        "coloredlogs",
    ]
)