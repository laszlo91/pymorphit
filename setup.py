import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pymorphit-laszlo94",
    version="0.0.1",
    description="A simple NLP library for Italian",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/laszlo91/pymorphit",
    #packages=setuptools.find_packages(),
    packages=['pymorphit'],
    package_dir={'pymorphit': 'pymorphit'},
    package_data={'pymorphit': ['morphit/morphit.pkl']},
    #include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)