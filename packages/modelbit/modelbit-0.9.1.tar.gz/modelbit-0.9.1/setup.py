from setuptools import setup  # type: ignore
from setuptools.command.install import install
import os, json, shutil


class PostInstallCommand(install):

  def run(self):
    install.run(self)
    from jupyter_client.kernelspec import KernelSpecManager
    from IPython.utils.tempdir import TemporaryDirectory
    kernel_json = {
        "argv": ["python", "-m", "modelbit.kernel", "-f", "{connection_file}"],
        "display_name": "Modelbit Cloud (Python 3)",
        "language": "python",
        "interrupt_mode": "message"
    }
    with TemporaryDirectory() as td:
      os.chmod(td, 0o755)
      with open(os.path.join(td, 'kernel.json'), 'w') as f:
        json.dump(kernel_json, f, sort_keys=True)
      for fileName in ['logo-32x32.png', 'logo-64x64.png']:
        shutil.copy(os.path.join(os.getcwd(), fileName), os.path.join(td, fileName))
      ksm = KernelSpecManager()
      ksm.install_kernel_spec(td, 'modelbit', user=True, replace=True)  # type: ignore


setup(
    name='modelbit',
    version='0.9.1',
    description='Python package to connect Jupyter notebooks to Modelbit',
    url='https://www.modelbit.com',
    author='Modelbit',
    author_email='tom@modelbit.com',
    license='MIT',
    packages=['modelbit', 'pyaes'],
    setup_requires=['jupyter-client', 'ipython'],
    package_data={"modelbit": ["*.pyi"]},
    data_files=[("", ["logo-32x32.png", "logo-64x64.png"])],
  # Note: Keep these deps in sync with snowpark config
    install_requires=[
        'pycryptodomex', 'pandas', 'tqdm', 'requests', 'types-requests', 'ipython', 'ipykernel', 'grpcio',
        'protobuf', 'types-protobuf', 'types-pkg-resources'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: IPython',
        'Framework :: Jupyter',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft',
        'Programming Language :: Python :: 3',
    ],
    cmdclass={'install': PostInstallCommand})
