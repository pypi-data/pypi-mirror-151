import setuptools

setuptools.setup(
    name='group05', #库的名字
    version='0.0.1',#库的版本号，后续更新的时候只需要改版本号
    author='five',#名字
    author_email='854412413@qq.com',#邮箱
    description='第五小组的第三方库',#介绍
    long_descroption_content_type='text/markdown',
    url='https://github.com',
    packages=setuptools.find_packages(),
    cassifiers=[
        'Programming language:: Python ::3',
        'License :: OSI Approved :: MIT License',
        'OPerating System :: OS Independent'
    ],
)
