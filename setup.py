"""
Setup configuration for character-agent-integration package.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_file(filename):
    """Read file contents."""
    with open(os.path.join(os.path.dirname(__file__), filename), encoding='utf-8') as f:
        return f.read()

setup(
    name='character-agent-integration',
    version='1.0.0',
    author='SuperInstance Team',
    author_email='contact@superinstance.ai',
    description='Integration layer connecting character personalities with AI agent architecture',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/superinstance/character-agent-integration',
    packages=find_packages(exclude=['tests', 'tests.*', 'examples', 'docs']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.8',
    install_requires=[
        'character-library>=1.0.0',
        'hierarchical-memory>=1.0.0',
        'numpy>=1.20.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=3.0.0',
            'black>=22.0.0',
            'flake8>=4.0.0',
            'mypy>=0.950',
        ],
        'docs': [
            'sphinx>=4.5.0',
            'sphinx-rtd-theme>=1.0.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'character-agent=character_agent_integration.cli:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords='ai agent character personality emotion memory integration',
    project_urls={
        'Bug Reports': 'https://github.com/superinstance/character-agent-integration/issues',
        'Source': 'https://github.com/superinstance/character-agent-integration',
        'Documentation': 'https://character-agent-integration.readthedocs.io/',
    },
)
