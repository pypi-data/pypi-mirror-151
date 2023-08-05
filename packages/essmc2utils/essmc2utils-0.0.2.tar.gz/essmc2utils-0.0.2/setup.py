import setuptools


def get_long_description():
    with open('README.md') as f:
        long_description = f.read()
    return long_description


def get_version():
    version_path = "essmc2utils/version.py"
    with open(version_path) as f:
        exec(compile(f.read(), version_path, "exec"))
    return locals()['__version__']


def get_requirements():
    with open("requirements.txt") as f:
        return f.read().splitlines()


required = get_requirements()

setuptools.setup(
    name="essmc2utils",
    version=get_version(),
    author="Logistic1994",
    author_email="logistic1994@gmail.com",
    description="A standalone python package for essmc2.",
    keywords="registry, file_systems",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/Logistic1994/essmc2-utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=required,
)
