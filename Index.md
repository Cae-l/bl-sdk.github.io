---
layout: main
---

**Page Contents**
* TOC
{:toc}

This is the main page for the PythonSDK Mod Database.
The [PythonSDK](https://github.com/bl-sdk/PythonSDK) is an Unreal Engine plugin allowing you to write plugins in Python to interact directly with UE objects.
This opens up many new avenues for modding, from simply allowing modifying dynamically generated objects to letting modders run arbitrary game functions whenever they please.

Currently it supports:
- Borderlands 2
- Borderlands: The Pre-Sequel

## SDK Installation

If you're a video guide type person, [apple1417](https://github.com/apple1417) made a video guide:
![yt](https://www.youtube.com/embed/nvTYjFjQ-HI)

But if you're more of a text guide style person:

1. Download the [latest release](https://github.com/bl-sdk/PythonSDK/releases/latest) on Github
![PythonSDK Download Page](/assets/images/posts/installation1.png)
2. Open `PythonSDK.zip`. It should contain 4 items:
![PythonSDK.zip Contents](/assets/images/posts/installation2.png)
3. Locate your game's files. In Steam, this can be done by right-clicking on the game in your library, selecting "Properties," then in the "Local Files" section, clicking "Browse":
![Steam Contextual Menu](/assets/images/posts/installation3.png) ![Steam Local Files Properties](/assets/images/posts/installation4.png)
4. In the game's files, navigate to the `Binaries`, then the `Win32` folder. This folder should contain the `.exe` for your game (i.e. `Borderlands2.exe` or `BorderlandsPreSequel.exe`).
5. Copy the 4 items from `PythonSDK.zip` **exactly as they** are to the `Win32` folder. Note that `pythonXX.zip` should *not* be un-zipped:
![Win32 Folder Contents](/assets/images/posts/installation5.png)
6. If you had previously installed an older version of the SDK, delete any old files that weren't overwritten by the ones in the latest `PythonSDK.zip`.
7. You are done, and may launch the game (if it is running, relaunch it now). You should see a "Mods" menu in the main menu!
8. If the SDK fails to run with the files correctly in place as described above, you may need to [download and install Microsoft Visual C++ Redistributable](https://aka.ms/vs/16/release/vc_redist.x86.exe).

## Mod Installation
Installing mods is even simpler than installing the SDK itself.

In order to install SDK mods, all you need to do is:

1. Download the mod itself, usually this will be a zip file
![Mod Download Link](/assets/images/posts/mod-install1.png)
2. Then you can extract the mod folder itself to `Win32/Mods` (See: [Step 5](/#sdk-installation))
![Extracted Mod Folder](/assets/images/posts/mod-install2.png)
3. In the root of this new mod folder, there should be an `__init__.py` file
  - Depending on the mod, there might be other files in the mod folder, but `__init__.py` is required.
![`__init__.py`](/assets/images/posts/mod-install3.png)
4. Certain mods may have requirements, you can see them by looking at the `Requirements` header
  - You follow the same steps as you did with installing the main mod as any of the requirements.
5. More advanced mods could have some extra steps needed to install them, you should always read through the `Description` section of the mod page to make sure that you've installed the mod properly!

## Development

Using the Unreal Engine console, you can use a few extra console commands added in by the PythonSDK:
- `py <PYTHON STATEMENT>`, using this will run arbitrary python code
- `pyexec <PYTHON FILE>`, execute an arbitrary python file

The PythonSDK itself passes a ton of functions over to the Python interface.
All of these are included in the `unrealsdk` module which you can import from a python script.

### Writing SDK Mods


### Adding to the Database
In order to add your mods to this database, you need to create a JSON file and host it somewhere, following the format like:
```json
{
  "mods": [
    {
      "name": "[Mod Name]",
      "authors": "[Mod Author]",
      "description": "[Description, can include HTML/Markdown]",
      "tagline": "[Optional: A short description of the mod, if not available will pull from `description`]",
      "types": ["[Mod Types]"],
      "supports": ["[Supported Games ie `[\"BL2\", \"TPS\"]`]"],
      "issues": "[Optional] A link to your issues report page",
      "source": "[Optional] Link to the source code",
      "latest": "[LATEST VERSION]",
      "versions": {
        "[Latest Version]": "[Version Link]",
        "[Old Version]": "[Old Version Link]"
      },
      "[OPTIONAL] requirements": {
        "[Requirement]": ">=[VERSION]"
      }
    }
  ]
}
```
If you want to add more mods to be displayed in the database, add to the `mods` array following the same format

Then you can make a [Pull Request](https://github.com/bl-sdk/bl-sdk.github.io/pulls) and edit `https://github.com/bl-sdk/bl-sdk.github.io/blob/master/scripts/RepoInfo.json` to include the **direct** link to your hosted JSON file.