from setuptools import setup, find_packages

setup(name="sever_Novikov",
      version="0.0.1",
      description="sever_Novikov",
      author="Novikov",
      author_email="nyb4eg@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
