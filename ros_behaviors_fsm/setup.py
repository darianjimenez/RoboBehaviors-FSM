from setuptools import find_packages, setup

package_name = "ros_behaviors_fsm"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="rohanbendapudi",
    maintainer_email="datanteater@gmail.com",
    description="TODO: Package description",
    license="TODO: License declaration",
    extras_require={
        "test": [
            "pytest",
        ],
    },
    entry_points={
        "console_scripts": ["drive_arch = ros_behaviors_fsm.drive_arch:main"],
        "console_scripts": ["bump_detector = ros_behaviors_fsm.bump_detector:main"],
        "console_scripts": ["people_follow = ros_behaviors_fsm.follower:main"],
    },
)
