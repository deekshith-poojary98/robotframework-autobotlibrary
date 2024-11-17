from setuptools import setup, find_packages


with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name="robotframework-autobotlibrary",
    version="1.0.0",
    description="Robot Framework library wrapper for PyAutoGUI.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deekshith-poojary98/robotframework-autobotlibrary",
    author="Deekshith Poojary",
    maintainer="Deekshith Poojary",
    author_email="deekshithpoojary355@gmail.com",
    license='BSD-3-Clause License',
    packages=find_packages(),
    python_requires=">=3.6",
    keywords="gui desktop testing testautomation robotframework robotframework-autobotlibrary",
    install_requires=[
        'opencv-python',
        'PyAutoGUI==0.9.54',
        'robotframework>=5.0.1'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        'Framework :: Robot Framework :: Library',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing'
    ],
)
