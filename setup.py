from setuptools import find_packages, setup

setup(
    name='GamePlusEditor',
    description='A gui game maker written in python',
    version='0.0.1',
    url='https://github.com/IndividualCoder/GamePlus-Editor',
    author='Prince',
    author_email='IndividualCoder@gmail.com',
    license='MIT',
    keywords='game development',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'panda3d',
        'panda3d-gltf',
        'pillow',
        'pyperclip',
        'screeninfo',
        'psutil'
    ],

    python_requires='>=3.10',
)
