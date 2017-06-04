from setuptools import setup, find_packages

setup(
    name="grorg",
    version='0.1',
    py_modules=['grorg'],
    packages=find_packages(),
    install_requires=[
        'Click',
        'PyOrgMode'
    ],
    entry_points='''
        [console_scripts]
        grorg = grorg.grorg:cli
    ''',
)
