from setuptools import setup

if __name__ == '__main__':
    setup(
        package_data={'smart_documentation': 
        [ 
            'Templates/default/Template/docs/_static/*.css',
            'Templates/default/Template/docs/_templates/*.rst',
            'Templates/default/Template/docs/*.py',
            'Templates/default/Template/docs/*.rst',
            'Templates/default/Template/docs/Makefile',
            'Templates/default/Template/docs/make.bat',
            'Templates/github_workflows_yml/Template/.github/workflows/*.yml',
        ]
        }
    )