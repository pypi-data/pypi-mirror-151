from setuptools import setuptools

setuptools.setup(
	name="Mits Engine",
	version="1.0.6",
	license="MB INC",
	authors= ["MB Craft"],
	author_email="mbcraft@orange.fr",
	description="MITS is a basic devlopement system (based on Python).",
	long_description="Don't install Mits alone, it needs Mits Reader to be used.",
	download_url = "https://github.com/mbcraft-exe/MitsEngine/blob/main/Mits%20Engine-1.0.2.tar.gz",
	url = 'https://github.com/mbcraft-exe/MitsEngine/',
	keywords=["Mits", "MITS"],
	packages=["Engine"],
	classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: PyPy'],
    python_requires='>=3.8.0'
	)