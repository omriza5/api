from typing import Dict,Self

class Pokemon:
    def __init__(self,id: str,name: str,abilities: list[str],image:str) -> None:
        self.id = id
        self.name = name
        self.abilities = abilities
        self.image = image
    
    
    def to_dict(self) -> Self:
        return {
            'id': self.id,
            'name': self.name,
            'abilities': self.abilities,
            'image' : self.image
        }
    
    @classmethod
    def from_api(cls, data: Dict) -> 'Pokemon':
        id = data['id']
        name = data['name']
        abilities = [ability['ability']['name'] for ability in data['abilities']]
        image = data['sprites']["front_default"]
        return cls(id, name, abilities,image)
    
    def __str__(self):
        return f"Pokémon {self.name} (ID: {self.id}), Abilities: {', '.join(self.abilities)}"
    