from setuptools import setup

# setup()

# All Dependencies are described in setup.cfg
# This is just a placeholder file for backwards compatibility
import versioneer
setup(version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
)