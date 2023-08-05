from setuptools import setup, find_packages

setup(name="client_Novikov",
      version="0.0.1",
      description="client_Novikov",
      author="Novikov",
      author_email="nyb4eg@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
