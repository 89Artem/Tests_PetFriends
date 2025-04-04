import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder

class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru/'

    def get_api_key(self, email: str, password: str) -> json:
        """Получает ключ авторизации."""
        headers = {'Content-Type': 'application/json'}
        data = {'email': email, 'password': password}

        res = requests.post(self.base_url + 'api/key', headers=headers, data=json.dumps(data))

        # Отладочный вывод
        print(f"Status Code: {res.status_code}")
        print(f"Response Text: {res.text}")

        return res.status_code, res.json()

    def create_pet_simple(self, auth_key: json, name: str, animal_type: str, age: int) -> json:
        """Добавляет информацию о новом питомце без фото."""
        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=json.dumps(data))
        return res.status_code, res.json()

    def set_photo(self, auth_key: json, pet_id: str, photo_path: str) -> json:
        """Добавляет фото питомца."""
        headers = {'auth_key': auth_key['key']}
        with open(photo_path, 'rb') as file:
            files = {'pet_photo': file}
            res = requests.post(self.base_url + f'api/pets/set_photo/{pet_id}', headers=headers, files=files)

        return res.status_code, res.json()