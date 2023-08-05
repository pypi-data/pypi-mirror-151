from setuptools import setup, find_packages


setup(
    name='graph_crypto_search',
    version='0.6',
    license='MIT',
    author="Aniket29-shiv",
    author_email='aniketchopade2971@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Aniket29-shiv/cryptography',
    keywords='graph_crypto_search project',
    install_requires=[
          'scikit-learn',
      ],

)