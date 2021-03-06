import os
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext as _build_ext
from setuptools.command.install   import install   as _install
import subprocess

PKG = 'graphy'

def make_louvain():
    print()
    print("*** Running make on Louvain code...")
    subprocess.call('cd graphy/external/SurpriseMeCPM ; make', shell=True)
    print()
    print()

class install(_install):
    def run(self):
      make_louvain()
      _install.run(self)

# http://stackoverflow.com/questions/19919905/how-to-bootstrap-numpy-installation-in-setup-py
class build_ext(_build_ext):
    def run(self):
      make_louvain()
      _build_ext.run(self)

    def finalize_options(self):
        _build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        __builtins__.__NUMPY_SETUP__ = False
        import numpy as np
        self.include_dirs.append(np.get_include())

def read(fname):
  c_dir = os.path.dirname(os.path.realpath(__file__))
  return open(c_dir + '/' + fname).read()

exec(read(PKG + '/version.py'))

download_url = "https://github.com/artemyk/%s/tarball/master#egg="%PKG + \
               "%s-%s.tar.gz" % (PKG, __version__)

cython_modules = [ ]

try:
    from Cython.Build import cythonize
    ext_modules = cythonize([os.path.join(PKG, s+'.pyx') 
    	                     for s in cython_modules])

except ImportError:
    ext_modules = [Extension(PKG+'.'+s, [os.path.join(PKG, s+'.c')]) 
                   for s in cython_modules]

REQUIRED_NUMPY = 'numpy>=1.6'
required_packages = [
    REQUIRED_NUMPY,
    'scipy>=0.13',
    'six>=1.8.0',
    'networkx',
    'python-igraph',
]
tests_require = [
    'coverage>=3.7.0',
    'sphinx>=1.0.0',
    'matplotlib',
]

setup(name=PKG,
      version=__version__,
      description='Dynamical systems for Python',
      author='Artemy Kolchinsky',
      author_email='artemyk@gmail.com',
      url='https://github.com/artemyk/'+PKG,
      packages=[PKG],
      setup_requires=[REQUIRED_NUMPY,"setuptools_git>=0.3"],
      install_requires=required_packages,
      tests_require=tests_require,
      license="GPL",
      long_description=read('README.md'),
      download_url=download_url,
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
      ],
      cmdclass=dict(build_ext=build_ext, install=install),
      ext_modules=ext_modules,
      include_package_data=True,
      exclude_package_data={'': ['.gitignore','.travis.yml']},
      zip_safe=True,
     )
