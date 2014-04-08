from setuptools import setup, find_packages
setup(name='ascet-filer-teaser',
        version='0.1',
        description='filer-teaser',
        #long_description=readme,
        author="Michael Brown",
        author_email="michael@ascetinteractive.com",
        packages=find_packages(),
        include_package_data=True,
           # package_data={'':[
           #   'templates/cms/*',
           #   'templates/cms_pageimage/*',
           #   ]},
        install_requires=[
           'django-filer==0.9.5',
            ],
        zip_safe=False,
        )
