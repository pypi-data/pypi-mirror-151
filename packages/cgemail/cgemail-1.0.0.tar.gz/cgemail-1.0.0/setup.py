from setuptools import setup


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="cgemail",
    version="1.0.0",
    description="Lib de envio de e-mail.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/ramirooliveiracg/cgemail",
    author="Gabriel Dalacorte e Rogerio Filho",
    author_email="gnunes.servico@gmail.com, crofilho2@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["cgemail"],
    include_package_data=True,
    install_requires=["requests"],
)