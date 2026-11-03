from setuptools import setup

package_name = 'calcul_position'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='agilex',
    maintainer_email='agilex@todo.todo',
    description='Calcul la position',
    license='Calcul la position',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'odom_node = calcul_position.odom_node:main'
        ],
    },
)
