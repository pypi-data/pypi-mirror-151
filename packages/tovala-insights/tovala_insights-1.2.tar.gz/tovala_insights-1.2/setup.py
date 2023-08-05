import os
import setuptools

BASE_DIR = os.path.dirname(__file__)

with open(os.path.join(BASE_DIR, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_packages = [x.strip() for x in all_reqs]

version_filename = os.path.join(BASE_DIR, "version.py")

package_info = {}
with open(version_filename) as f:
    exec(f.read(), package_info)

setuptools.setup(version = package_info["__version__"], install_requires = install_packages)
