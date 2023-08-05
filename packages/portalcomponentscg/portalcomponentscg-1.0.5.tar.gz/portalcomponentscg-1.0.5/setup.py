from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="portalcomponentscg",
    version="1.0.5",
    description="Components para o portal de clientes CG.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/ramirooliveiracg/cgcomponents",
    author="Gabriel Dalacorte",
    author_email="gnunes.servico@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["portalcomponentscg"],
    include_package_data=True,
    install_requires=["requests"],
)