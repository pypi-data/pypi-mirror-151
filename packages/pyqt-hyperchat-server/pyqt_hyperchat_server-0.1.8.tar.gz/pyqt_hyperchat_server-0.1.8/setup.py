from setuptools import setup, find_packages

setup(name="pyqt_hyperchat_server",
      version="0.1.8",
      description="pyqt_hyperchat_server",
      author="Wrexan",
      author_email="fwrexan@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
