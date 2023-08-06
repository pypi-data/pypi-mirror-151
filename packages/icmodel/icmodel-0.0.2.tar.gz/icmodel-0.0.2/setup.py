from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
def _process_requirements():
    packages = open('requirements.txt').read().strip().split('\n')
    requires = []
    for pkg in packages:
        if pkg.startswith('git+ssh'):
            return_code = os.system('pip install {}'.format(pkg))
            assert return_code == 0, 'error, status_code is: {}, exit!'.format(return_code)
        else:
            requires.append(pkg)
    return requires
setup(
    name='icmodel',
    version='0.0.2',
    python_requires='>=3.6.0',
    author='qycai',
    author_email='cai_quanyou@gibh.ac.cn',
    url='https://github.com/JiekaiLab/development_time_predict',
    description='development_time_predict',
    
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['icmodel'],
    entry_points={},
    install_requires=_process_requirements(),
    classifiers=[
    'License :: OSI Approved :: MIT License',

    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    ],
    include_package_data=True,
    package_data =
    { 'model' : # NOTE: package/folder name, not pip name
    [ 'model/*.model'
    , 'model/*.npy'
    ]
    }
)