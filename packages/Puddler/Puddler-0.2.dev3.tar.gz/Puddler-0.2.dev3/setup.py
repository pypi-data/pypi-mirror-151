from distutils.core import setup

setup(
    name='Puddler',
    version='0.2.dev3',
    packages=['puddler'],
    license='GNU General Public License v3.0',
    url="https://github.com/Vernoxvernax/Puddler",
    author="VernoxVernax",
    author_email="vernoxvernax@gmail.com",
    install_requires=[
        "python-mpv",
        "python-mpv-jsonipc",
        "requests",
        "appdirs",
        "getch"
    ],
    description="Emby/Jellyfin command line client, powered by mpv.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
