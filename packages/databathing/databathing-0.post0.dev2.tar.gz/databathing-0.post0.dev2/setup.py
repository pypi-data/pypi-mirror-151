import setuptools
import versioneer

NAME = 'databathing'

setuptools.setup(
    name=NAME,
    version='0.1.0',
    description="build spark job based on query",
    author="Jiazhen Zhu",
    author_email="jason.jz.zhu@gmail.com",
    classifiers=["Development Status :: 3 - Alpha","Topic :: Software Development :: Libraries","Topic :: Software Development :: Libraries :: Python Modules","Programming Language :: SQL","Programming Language :: Python :: 3.7","Programming Language :: Python :: 3.8","Programming Language :: Python :: 3.9","License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)"],
    license="MIT",
    cmdclass=versioneer.get_cmdclass(),
    packages=setuptools.find_packages(),
    install_requires=[
          'mo-sql-parsing',
      ],
    # entry_points={
    #     'console_scripts': [

    #     ],
    # },
)
