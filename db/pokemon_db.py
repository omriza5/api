
import boto3
from botocore.exceptions import ClientError

boto3.setup_default_session(profile_name="terraform")

class PokemonDB:
    def __init__(self, table_name="pokemons", region="us-west-2"):
        self.dynamodb = boto3.resource("dynamodb", region_name=region)
        self.table = self.dynamodb.Table(table_name)

    def add_pokemon(self, pokemon_id, name, abilities, image):
        try:
            response = self.table.put_item(
                Item={
                    "id": pokemon_id,
                    "name": name,
                    "abilities": abilities,
                    "image": image
                }
            )
            return response
        except ClientError as e:
            print(f"Error adding Pokémon: {e.response['Error']['Message']}")
            return None

    def get_pokemon_by_name(self, name):
        try:
            response = self.table.query(
                IndexName="name-index", 
                KeyConditionExpression=boto3.dynamodb.conditions.Key("name").eq(name)
            )
            return response.get("Items", [])
        except ClientError as e:
            print(f"Error fetching Pokémon: {e.response['Error']['Message']}")
            return None
        
    def get_all_pokemons(self):
            try:
                response = self.table.scan()
                return response.get("Items", [])
            except ClientError as e:
                print(f"Error fetching all Pokémon: {e.response['Error']['Message']}")
                return []