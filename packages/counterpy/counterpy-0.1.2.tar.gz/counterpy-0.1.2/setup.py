from setuptools import find_packages, setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.rst").read_text(encoding="utf-8")

setup(
    name='counterpy',
    packages=find_packages(where='src'),
    version='0.1.2',
    description='Simple CLI cantus firmus generator based on a genetic algorithm',
    author='Matias Ceau',
    author_email="matias@ceau.net",
    long_description=long_description,
    entry_points={'console_scripts': ['counterpy=counterpy.counterpy:main']},
    #long_description_content_type="text/markdown",
    include_package_data=True,
    license='GPLv3',
    url="https://github.com/matias-ceau/counterpy",
    install_requires=['numpy','pandas', 'scipy', 'playsound'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS",
    ],
    keywords="counterpoint, cantus firmus, genetic algorithm",
    # setup_requires=['pytest-runner'],
    # tests_require=['pytest'],
    test_suite='tests',
    package_dir={'': 'src'}
)
