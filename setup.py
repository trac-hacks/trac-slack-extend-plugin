from setuptools import find_packages, setup

setup(
    name='TracSlackExtend',
    version='0.1.0',
    packages=find_packages(exclude=['*.tests*']),
    entry_points={
        'trac.plugins': [
            'trac_slack_extend = trac_slack_extend',
        ],
    },
    url='',
    license='',
    author='krassi',
    author_email='krasimir.nikolov1994@gmail.com',
    description=''
)