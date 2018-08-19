from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='TinkerTest',
    version='0.1.1',
    packages=find_packages(),
    url='https://github.com/austinv11/tinkertest',
    project_urls={
        'Bug Reports': 'https://github.com/austinv11/tinkertest/issues',
        # 'Funding': 'https://donate.pypi.org',
        # 'Say Thanks!': 'http://saythanks.io/to/example',
        'Source': 'https://github.com/austinv11/tinkertest/',
    },
    license='Apache License 2.0',
    author='austinv11',
    author_email='austinv11@gmail.com',
    description='TinkerTest is a tool designed to make data validation fun!',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Unit",
        "Topic :: Utilities",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    keywords='testing test annotations validation',
    entry_points={  # Optional
            'console_scripts': [
                'tinkertest=tinkertest:main',
            ],
        },
)
