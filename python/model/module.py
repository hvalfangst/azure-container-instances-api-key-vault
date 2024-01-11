from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class Hero:
    name: str
    hero_class: str
    hero_damage: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "Name": self.name,
            "Class": self.hero_class,
            "Damage": self.hero_damage
        }