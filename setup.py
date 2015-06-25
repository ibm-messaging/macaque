from setuptools import setup

def readme():
	with open('README.md') as f:
		return f.read()

setup(name='macaque',
	version='0.1',
	description='Flask style library for microservices with MQ Light',
	long_description=readme(),
	keywords='mqlight amqp microservices',
	url='http://github.com/ibmmessaging/macaque',
	author='Al S-M',
	author_email='asm@uk.ibm.com',
	license='EPL',
	packages=['macaque'],
	install_requires=[
		"mqlight"
	],
	zip_safe=False)

