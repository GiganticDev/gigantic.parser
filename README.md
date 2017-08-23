# Gigantic Parser Module

A Module to Parse Data from *Motiga's* **Gigantic**


## Installation:

#### During Production:
```
pip install .
```

#### During development:
```
pip install -e .[development]
```

## Usage

#### To get json
Run `python -m gigantic.parser` in the 'RxGame' directory of your gigantic folder and it will print out json parsed output.
You may use `python -m gigantic.parser > target_file.json` to output this to a file.


#### As in-memory db
The models located in the `gigantic.dao.model` can be used as a sort of in-memory database and filtered using list comprehension. All istances of those classes are stored in the class attribute `__dataset__`, which is a global map.

`model.Hero.__dataset__` for example will list all heroes, to find a specific hero by 'resource id' you can do `model.Hero.__dataset__['Adept']` where `Adept` is the hero ID for Aisling.

To retrieve all skills for Aisling as the project currently does you could use list comprehension on the Skill dataset singleton.

`aisling_skills = [skill for skill in model.Skill.__dataset__.values() if skill.hero == 'Adept']`
