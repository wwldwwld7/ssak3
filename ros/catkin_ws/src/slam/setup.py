from setuptools import setup

package_name = 'slam'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/rros2 esource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='SSAFY',
    maintainer_email='dark6ro@naver.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'talker = slam.publisher_member_function:main',
            'listener = slam.subscriber_member_function:main',
            'broadcaster = slam.static_turtle_tf2_broadcaster:main',
            'slam = slam.slam:main',
            'odom_test = slam.odom_test:main',
            'wall_tracking = slam.wall_tracking:main'
        ],
    },
)
