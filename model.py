from dataclasses import dataclass, fields
from typing import List


@dataclass
class YamlConfigImport:
    dir: str
    excludes: List[str]
    flatten: List[str]
    pullup: List[str]


@dataclass
class YamlConfig:
    root: str
    target: str
    includes: List[str]
    imports: List[YamlConfigImport]

    @classmethod
    def init_from_yaml(cls, yaml_as_dict):
        imports = []
        for im in yaml_as_dict["imports"]:
            imports += [YamlConfigImport(
                dir=im["dir"],
                excludes=im["excludes"],
                flatten=im["flatten"],
                pullup=im["pullup"]
            )]
        return YamlConfig(
            root=yaml_as_dict["root"],
            target=yaml_as_dict["target"],
            includes=yaml_as_dict["includes"],
            imports=imports
        )
