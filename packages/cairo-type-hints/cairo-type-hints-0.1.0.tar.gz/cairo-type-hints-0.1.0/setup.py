from setuptools import setup, find_packages

setup(
    include_package_data=True,
    name="cairo-type-hints",
    version="0.1.0",
    author="Chris Baker",
    author_email="lxufimdu@pm.me",
    description="Generate type hints for Cairo lang",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/playmint/cairo-type-hints",
    packages=find_packages(),
    license="LICENSE",
    requires=["lark"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development"
    ]
)
