from setuptools import setup

setup(
    name="grorg",
    version='0.1',
    py_modules=['grorg'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        grorg=grorg:cli
    ''',
)
