
from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


def install_requirements():
    return [package_string.strip() for package_string in open('requirements.txt', 'r')]



setup(
    name='reformedcatutils',
    version="0.0.1",
    description="Helper functions for ReformedCat Project",
    long_description="Helper functions for ReformedCat Project",
    long_description_content_type='text/markdown',
    classifiers=[
      "Natural Language :: Chinese (Traditional)",
      "Natural Language :: Chinese (Simplified)",
      "Natural Language :: English",
      "Topic :: Software Development :: Libraries :: Python Modules",
      "Topic :: Software Development :: Version Control :: Git",
      "Topic :: Scientific/Engineering :: Artificial Intelligence",
      "Intended Audience :: Religion",
      "Programming Language :: Python :: 3.7",
      "Programming Language :: Python :: 3.8",
      "Programming Language :: Python :: 3.9",
      "Programming Language :: Python :: 3.10",
      "Intended Audience :: Science/Research",
      "Intended Audience :: Developers",
    ],
    keywords="Bible, Scripture, catechism",
    url="https://github.com/stephenhky/ReformedCatUtils",
    author="Kwan-Yuet Ho",
    author_email="stephenhky@yahoo.com.hk",
    license='LGPL',
    packages=[
        'reformedcatutils'
    ],
    install_requires=install_requirements(),
    tests_require=[
      'unittest2'
    ],
    # scripts=[],
    include_package_data=True,
    test_suite="test",
    zip_safe=False
)
