import versioneer
from setuptools import setup, find_packages


with open('requirements.txt', 'r') as file:
    REQUIREMENTS = file.readlines()

with open('README.md', 'r') as file:
    long_description = file.read()


setup(
    name='drb-topic-sentinel5',
    description='sentinel-5 topic for DRB Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='GAEL Systems',
    author_email='drb-python@gael.fr',
    url='https://gitlab.com/drb-python/topics/sentinel-5',
    python_requires='>=3.8',
    install_requires=REQUIREMENTS,
    packages=find_packages(exclude=['tests', 'tests.*']),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.8",
    ],
    package_data={
        'drb_topic_sentinel5': ['cortex.yml'],
        'drb_topic_sentinel5.level1': ['cortex.yml'],
        'drb_topic_sentinel5.level2': ['cortex.yml'],
        'drb_topic_sentinel5.auxiliary': ['cortex.yml']
    },
    data_files=[('.', ['requirements.txt'])],
    entry_points={
        'drb.impl': [
            'sentinel5=drb_topic_sentinel5',
            'sentinel5_l1=drb_topic_sentinel5.level1',
            'sentinel5_l2=drb_topic_sentinel5.level2',
            'sentinel5_aux=drb_topic_sentinel5.auxiliary'
        ]
    },
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass()
)
