# Yggdrasil
#### Concept
The yggdrasil library is meant to facilitate the distribution of scripts into production through the definition of apps.
Conceptually, each app is defined as:
- Name: Characterises the app to be installed / uninstalled
- Source code: Source code of the project that must be accessed
- Entry points: Entry points of the project
- Virtual environment: environment to run the app within

Through its API, yggdrasil gives your means to seamlessly switch between several virtual environments while having an 
easy way to call your home-made scripts from the command line.

#### Getting started
Before using the tool to create apps, yggdrasil needs an initial set up.
First, install the package (either from PyPI or from Github):
```commandline
pip install ud-yggdrasil
pip install git+https://www.github.com/um-ed/ud-yggdrasil.git
```

Then, create the base folder structure to install yggdrasil into:
```shell script
yggdrasil seed
```
If a path is set up as environment variable (*YGGDRASIL_ROOT*), the folders structure will be created there.
If not, it will be created under the user's *Documents* folder.
To make each app easily callable from the command line, it's also recommended to add the 
*Yggdrasil\Scripts* full path to the *Path* environment variable.

That's it, you're ready to create your first application!

#### Applications requirements
The definition of apps is done through the settings.yaml file (under Yggdrasil\settings). The library gives the possibility
to either install apps that are only stored locally (local apps hereafter) or hosted online in a git repository (web apps
hereafter).
The settings file is automatically created when running *seed*, already prefilled with dummy examples for local & web setups.
If in doubt / altered locally, it can also be found under this repository (yggdrasil\data\template_settings.yaml).
To be able to create an application, the core project will also need to define:
- A requirements.txt file with the project's dependencies, located at the source of the package / project directory
- For web-based apps, the project will need to define entry points in the setup.py file

#### Yggdrasil commands
Yggdrasil can be called either from shell or from python. From shell:
```commandline
yggdrasil seed # Creates a seed for yggdrasil
yggdrasil create app_name # Installs an app for the given name
yggdrasil remove app_name # Uninstalls an app for the given name
yggdrasil show app_name # Show information related to the app name provided
```
*(Further parametrisation available, details with -h)*

From python:
```python
import yggdrasil as ygg
ygg.seed() # Creates a seed for yggdrasil
ygg.create("app_name") # Installs an app for the given name
ygg.remove("app_name") # Uninstalls an app for the given name
ygg.show("app_name") # Show information related to the app name provided
```

After an application is installed through yggdrasil (and provided the yggdrasil scripts' path was added
to the *Path* environment variable), you will be able to call the project's entry points
directly from the command line:
```commandline
app_name
```

Any feedback welcome!