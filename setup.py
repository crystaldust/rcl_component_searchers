from setuptools import setup

package_name = 'rcl_component_searchers'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Zhen Ju',
    maintainer_email='juzhen@huawei.com',
    description='The ros2 component(dynamical loadable node) searchers',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
        'rclpy_components.searcher': [
            'class=rcl_component_searchers:PyEntryPointComponentSearcher'
        ],
        'rclcpp_components.searcher': [
            'class=rcl_component_searchers:AmentResourceComponentSearcher'
        ]
    },
)
