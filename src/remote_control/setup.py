from setuptools import find_packages, setup

package_name = 'remote_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'adafruit-pca9685'],
    zip_safe=True,
    maintainer='newslab',
    maintainer_email='newslab@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'remote_control = remote_control.remote_control:main'
        ],
    },
)
