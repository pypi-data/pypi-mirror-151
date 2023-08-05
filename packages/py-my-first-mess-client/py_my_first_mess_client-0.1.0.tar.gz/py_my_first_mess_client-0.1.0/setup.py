from setuptools import setup, find_packages

setup(name="py_my_first_mess_client",
      version="0.1.0",
      description="Messenger Client",
      author="Max",
      author_email="gatts@mail.ru",
      packages=find_packages(),
      install_requires=["PyQt5", "sqlalchemy", "pycryptodome", "pycryptodomex"],
      )
