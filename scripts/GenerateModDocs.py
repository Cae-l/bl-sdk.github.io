#!/usr/bin/python
import os
import sys
import requests
import json
import datetime
import bleach


class Mod:
    ValidLicenses = {
        "GNU AGPLv3": "agpl-3.0",
        "GNU GPLv3": "gpl-3.0",
        "GNU LGPLv3": "lgpl-3.0",
        "Mozilla License 2.0": "mpl-2.0",
        "Apache 2.0": "apache-2.0",
        "MIT": "mit",
        "Boost Software License 1.0": "bsl-1.0",
        "Unlicense": "unlicense",
        "zlib": "zlib",
        "MIT No Attribution": "mit-0",
        "Creative Commons Attribution Share Alike 4.0 International": "cc-by-sa-4.0",
        "cc-by-sa-4.0": "cc-by-sa-4.0",
        "Creative Commons Attribution 4.0 International": "cc-by-4.0",
        "cc-by-4.0": "cc-by-4.0",
    }

    # All of the allowed tags that can be stored in a Mod's description
    # Any other tags will be removed by the HTML sanitizer
    AllowedTags = [
        "a",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "strong",
        "em",
        "p",
        "ul",
        "ol",
        "li",
        "br",
        "sub",
        "sup",
        "hr",
        "img",
        "blockquote",
        "code",
        "video",
    ]

    # A dictionary of allowed attributes for the HTML sanitizer
    # See: https://bleach.readthedocs.io/en/latest/clean.html#as-a-dict
    AllowedAttributes = {
        "a": ["href", "rel"],  # Links can have an href
        "img": ["src", "alt"],  # Images can have src and alt
    }

    Name = ""  # Name of the given mod
    Authors = []  # Authors of the given mod
    Tagline = ""  # Short-form description of the given mod
    Description = ""  # A longer explanation, can be equal to Tagline
    Types = []  # What the mod's types are in the mod manager

    IssuesLink = ""  # A link to the mod's issue page or a discord tag or nothing, optional
    SourceCode = ""  # Link to the mod's source code, optional

    LatestVersion = ""  # The latest version number for the given mod
    Versions = {}  # All available versions of this mod
    Requirements = {}  # All pre-requisites for this mod

    Supports = []  # A list representing the games that this mod currently supports
    License = []  # An optional list of what license the mod is currently licensed as.

    Date = datetime.datetime.now().isoformat()  # The current time in ISO-8601 format, used for "Last Updated"

    def ConvertStringToFile(self, string):
        return "".join([ch if ch.isalnum() else "" for ch in string])

    def __init__(self, modObject, bSoftExceptions):
        print(f"Creating new mod with mod object: {modObject}")
        try:
            self.Name = modObject["name"]

            # Support both `"authors":["xyz","abc"]` and `"authors":"xyz"`
            if isinstance(modObject["authors"], list):
                self.Authors = modObject["authors"]
            elif isinstance(modObject["authors"], str):
                self.Authors = [modObject["authors"]]

            if "description" in modObject:
                self.Description = modObject["description"]
            elif "tagline" in modObject:
                self.Description = modObject["tagline"]

            # Mods are optionally allowed to have a tagline, otherwise it will be equal to the description
            if "tagline" in modObject:
                self.Tagline = modObject["tagline"]
            elif "description" in modObject:
                self.Tagline = self.Description

            if "issues" in modObject:
                self.IssuesLink = modObject["issues"]

            if "source" in modObject:
                self.SourceCode = modObject["source"]

            # Do this assertion in order to avoid latest not being a string and versions not being a dict
            assert isinstance(modObject["latest"], str) and isinstance(modObject["versions"], dict)

            self.LatestVersion = modObject["latest"]
            self.Versions = modObject["versions"]

            if "requirements" in modObject:
                self.Requirements = modObject["requirements"]

            assert isinstance(modObject["supports"], list)

            self.Supports = modObject["supports"]

            if "license" in modObject:
                self.License = modObject["license"]

            if "types" in modObject:
                self.Types = modObject["types"]

            self.Description = bleach.clean(
                self.Description,
                tags=self.AllowedTags,
                attributes=self.AllowedAttributes,
                strip=True,
            ).replace('"', "'")

            if "license" in modObject:
                assert modObject["license"] in self.ValidLicenses
                self.License = [modObject["license"], self.ValidLicenses[modObject["license"]]]

        except Exception as ex:
            if bSoftExceptions:
                return None
            else:
                raise ex

    def ConvertToMarkdown(self):
        with open("./DefaultMod.md", "r", encoding="utf-8") as DefaultMod:
            NewText = "".join(DefaultMod.readlines())  # Create a whole file of the default text

        NewText = NewText.replace('authors: ""', f'authors: "{", ".join(self.Authors)}"')  # Add the author flag
        NewText = NewText.replace('title: ""', f"title: {self.Name}")  # Add mod name
        NewText = NewText.replace('version: ""', f'version: "{self.LatestVersion}"')  # Add latest version
        NewText = NewText.replace('supported: ""', f'supported: "{" + ".join(self.Supports)}"')  # Add supported
        NewText = NewText.replace('tagline: ""', f'tagline: "{self.Tagline}"')  # Add tagline
        NewText = NewText.replace('description: ""', f'description: "{self.Tagline}"')  # Add embed desc
        NewText = NewText.replace('longDescription: ""', f'longDescription: "{self.Description}"')  # Add full desc
        NewText = NewText.replace("categories: []", f"categories: {str(self.Types)}")  # Add types

        NewText = NewText.replace(
            "requirements: []",
            f'requirements: {[(m + " " + self.Requirements[m][:2] + " " + self.Requirements[m][2:]) for m in self.Requirements]}',
        )  # This is a bit janky since it takes in a dictionary and then we add spaces between `[MOD]>=[VER]`
        NewText = NewText.replace(
            "requirementTitles: []", f"requirementTitles: {[self.ConvertStringToFile(m) for m in self.Requirements]}"
        )
        NewText = NewText.replace('issues: ""', f'issues: "{str(self.IssuesLink)}"')  # Add an issues link if available
        NewText = NewText.replace(
            'download: ""', f'download: "{self.Versions[self.LatestVersion]}"'
        )  # Add download link
        NewText = NewText.replace('date: ""', f"date: {self.Date}Z")  # Add ISO8601 time stamp date

        NewText = NewText.replace("requirementTitles: []", f'requirementTitles: [{""}]')

        NewText = NewText.replace('license: ["", ""]', f"license: {self.License}")

        # Strip all non-alphanumeric characters out for the URL
        NewFileName = self.ConvertStringToFile(self.Name) + ".md"

        print(f"Writing {self.Name} to _mods/{NewFileName}")
        with open(f"../_mods/{NewFileName}", "w+") as outFile:
            outFile.write(NewText)


def RequestJSONFromPage(url, bSoftExceptions):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"{url} returned {response.status_code}!")
        if bSoftExceptions:
            return None
        else:
            raise Exception("URL returned incorrect status code!")
    elif response.status_code == 200:
        try:
            JSONData = json.loads(response.text)
            assert "mods" in JSONData  # Make sure that the returned JSON contains a "mods" dictionary
            return JSONData
        except Exception as ex:
            if bSoftExceptions:
                return None
            else:
                raise ex


def GenerateModDocs(bSoftExceptions=True):
    # Delete all of the files in _mods/ to allow for mods to be deleted from repositories
    for file in os.listdir("../_mods"):
        os.remove(os.path.join("../_mods", file))

    print(f"Generating mod docs; bSoftExceptions == {bSoftExceptions}")
    with open("./RepoInfo.json") as repoFile:
        repositoryInfo = json.load(repoFile)

    print(f"List of repositories: {repositoryInfo}")

    for repository in repositoryInfo:
        print(f"Parsing repository: {repository}")
        modsData = RequestJSONFromPage(repository, bSoftExceptions)
        allMods = []
        for modData in modsData["mods"]:
            modObject = Mod(modData, bSoftExceptions)
            modObject.ConvertToMarkdown()
            allMods += [modObject]


if len(sys.argv) > 1 and sys.argv[1] == "--hard":
    GenerateModDocs(False)
else:
    GenerateModDocs()