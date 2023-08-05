from setuptools import setup

if __name__ == '__main__':
    setup(
        package_data={'pypi_builder': 
        [ 
            'Templates/default/Template/src/{{name}}/__init__.py',
            'Templates/default/Template/src/{{name}}/__main__.py',
            'Templates/default/Template/LICENSE', 
            'Templates/default/Template/MANIFEST.in',
            'Templates/default/Template/pyproject.toml', 
            'Templates/default/Template/requirements.txt',
            'Templates/default/Template/setup.cfg',
            'Templates/default/Template/setup.py',
        ]
        }
    )

