import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='ThreadingWrapper',
    version='0.0.1',
    description='A threading wrapper which can be used quickly to run tasks in parallel',
    url='https://github.com/thedly/pythreading-wrapper',
    author='Tejas Hedly',
    author_email='tejas.hedly@gmail.com',
    license='GNU GENERAL PUBLIC LICENSE',
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    python_requires=">=3.6",
)
