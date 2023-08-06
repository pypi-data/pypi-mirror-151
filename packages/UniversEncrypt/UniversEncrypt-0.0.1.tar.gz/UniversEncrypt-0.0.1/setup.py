import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(

	name="UniversEncrypt",

	version="0.0.1",

	author="IvanIvanov",

	author_email="ivanko@gmail.com",

	description="This is Best encrypt in the world!",
	
	long_description=long_description,

	long_description_content_type="text/markdown",
	
	url="",

	packages=setuptools.find_packages(),
	
	classifiers=[
		"Programming Language :: Python :: 3.8",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
    
	python_requires='>=3.6',
)