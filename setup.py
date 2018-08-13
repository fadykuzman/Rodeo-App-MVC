from setuptools import setup, find_packages

setup(
    name='RODEO_APP_MVC',
    version='0.0.1',
    author='Fady Kuzman',
    author_email='f.s.a.kuzman@gmail.com',
    description='GUI for Iorodeo Potentiostat on Linux',
    url='https://github.com/fadykuzman/Rodeo-App-MVC',
    license='MIT',
    packages=find_packages(),
    install_requires=['iorodeo-potentiostat',
                      'numpy', 'matplotlib',
                      'psycopg2'],
    python_requires='>=3.6',
    entry_poits={
        'console_scripts': [
            'rodeoapp = rodeo_app:main'
        ]}
)
