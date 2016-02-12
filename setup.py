from setuptools import setup, find_packages

setup(name="ninjapic",
      version="0.1.0",
      packages=find_packages(),
      entry_points={
          "gui_scripts": [
              "ninjapic = app.__main__:main"
          ]
      },
      )
