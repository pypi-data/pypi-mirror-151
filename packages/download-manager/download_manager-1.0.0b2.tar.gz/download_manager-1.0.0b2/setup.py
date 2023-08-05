import versioneer
from setuptools import find_packages, setup

with open('requirements.txt') as f:
    REQUIREMENTS = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='download_manager',
    packages=['download_manager',
              'download_manager.source',
              'download_manager.destination',
              'download_manager.database',
              'download_manager.progress',
              'download_manager.run',
              'download_manager.storage',
              ],
    description='Download Manager',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='GAEL Systems',
    author_email='drb-python@gael.fr',
    url='https://gitlab.com/drb-python/tools/download-manager',
    install_requires=REQUIREMENTS,
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    use_scm_version=True,
    data_files=[('.', ['requirements.txt'])],
    entry_points={
        'console_scripts': [
            'download_manager=download_manager.cli:cli'
        ]
    },
    project_urls={
        'Source': 'https://gitlab.com/drb-python/tools/download-manager',
    }
)
