import os
from setuptools import setup

setup(
    name="ReprDynamics",
    version="0.1.5",
    description="Visualization of representation dynamics",
    author="Noah",
    author_email="Noah.Barrett@dal.ca",
    packages=['ReprDynamics'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'click==7.1.2',
        'numpy',
        'opencv-python==4.5.2.52',
        "Pillow",
        'scikit-image',
        'scikit-learn==0.24.2',
        "scipy",
        'torch==1.8.1',
        "torchvision",
        'flask'
      ],
    classifiers=[
            'Intended Audience :: Science/Research',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python :: 3.9',
        ],

    entry_points={
        "console_scripts": ["ReprDynamics = app:run"]
    },
)