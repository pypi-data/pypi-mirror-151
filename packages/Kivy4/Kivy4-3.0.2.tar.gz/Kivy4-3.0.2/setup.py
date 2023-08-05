import setuptools

with open("README.md", "r") as fh:
    description = fh.read()

setuptools.setup(
    name="Kivy4",
    version="3.0.2",
    author="Eshqol Development",
    author_email="support@eshqol.com",
    packages=["kivy4"],
    description="This package allows you to create Kivy projects faster with a pre-made kivy template.",
    long_description=description,
    long_description_content_type="text/markdown",
    license='MIT',
    python_requires='>=3.7',
    install_requires=['kivy==2.0.0', 'kivymd', 'darkdetect', 'screeninfo', 'pyperclip', 'winshell', 'pywin32']
)

#Eshqol_Development