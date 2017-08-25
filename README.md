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

#### As in-memory db
Each class located in `gigantic.dao.hero` and `gigantic.dao.translation` acts as a singleton for class instances, which are held in the class' `__dataset__` attribute map which contains `resource_id: resource_instance` key value pairs..

`model.Hero.__dataset__` for example will list all heroes, to find a specific hero by 'resource id' you can do `model.Hero.__dataset__['Adept']` where `Adept` is the hero ID for Aisling.

You can use list comprehension to filter and relate the data very quickly thanks to the small size of the datasets, for example to get all skills for Aisling it would be as simple as:

`aisling_skills = [skill for skill in model.Skill.__dataset__.values() if skill.hero == 'Adept']`

##### More complete example with translations

    from gigantic.parser import parse_heroes, parse_translations
    from gigantic.dao.hero import *
    from gigantic.dao.translation import *
    
    if __name__ == '__main__':
        parse_heroes('/absolute/path/to/Config/Heroes')
        parse_translations('/absolute/path/to/Localization')
        for hero in Hero.__dataset__.values():
            translation = HeroTranslation.__dataset__['INT'][hero.section_id]
            print("{0} ({1})".format(translation.display_name, hero.id))
