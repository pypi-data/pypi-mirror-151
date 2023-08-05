from setuptools import setup

if __name__ == '__main__':
    setup(
        package_data={'repository_generator': 
            [ 
                'Templates/default/Template/.gitignore',
                'Templates/default/Template/README.md', 
                'Templates/jameskabbes/Template/.gitignore',
                'Templates/jameskabbes/Template/README.md', 
            ]
            }


    )