from setuptools import setup, find_packages

setup(name = "Moshu_QtMesseger_client",
      version = "0.01",
      description = "QtMesseger_client",
      author = "Vladislav K.",
      author_email = "boer5678@gmail.com",
      url = "http://www.gb.ru/",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )