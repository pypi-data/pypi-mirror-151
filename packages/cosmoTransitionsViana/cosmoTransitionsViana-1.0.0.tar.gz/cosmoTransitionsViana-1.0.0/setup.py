from setuptools import setup

setup(
    name="cosmoTransitionsViana",
    version="1.0.0",
    packages=['cosmoTransitionsViana'],
    package_dir={'cosmoTransitions.examples': 'examples'},
    description=(
        "A package for analyzing finite or zero-temperature cosmological "
        "phase transitions driven by single or multiple scalar fields."
    ),
    author="J. Viana",
    author_email="jfvvchico@hotmail.com",
    url="https://github.com/vollous/CosmoTransitionsViana",
    install_requires=['numpy>=1.8', 'scipy>=0.11'],
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)
