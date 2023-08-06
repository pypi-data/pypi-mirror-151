import setuptools

with open("README.md", "r", encoding="utf-8") as README:
    long_description = README.read()

setuptools.setup(
    name='pytba-captcha',
    version='0.0.1',
    description='Implement a CAPTCHA system with pyTelegramBotAPI',
    author= 'SOHAM DATTA',
    author_email='dattasoham805@gmail.com',
    url = 'https://github.com/TECH-SAVVY-GUY/telebot-captcha',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=['telebot', 'telegram', 'pyTelegramBotAPI', 'captcha'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=['pytba_captcha'],
    package_dir={'':'src'},
    install_requires = [
        'pyTelegramBotAPI',
        'redis'
    ]
)