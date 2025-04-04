import os
import pytest
from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()

@pytest.fixture
def auth_key():
    status, key = pf.get_api_key(valid_email, valid_password)
    assert status == 200
    return key

@pytest.fixture
def create_pet(auth_key):
    """Создание питомца"""
    pet_photo = os.path.join(os.path.dirname(__file__), 'images/sam.jpg')  # Исправлено на __file__
    name = 'Барбоскин'
    animal_type = 'двортерьер'
    age = 4  # Возраст как целое число

    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    return result

def test_create_pet_simple_with_valid_data(auth_key):
    """Проверяем создание питомца с корректными данными"""
    status, result = pf.create_pet_simple(auth_key, 'Мурзик', 'Кот', 3)  # Возраст как целое число
    assert status == 200
    assert result['name'] == 'Мурзик'

def test_create_pet_simple_without_name(auth_key):
    """Проверяем создание питомца без имени (некорректный случай)"""
    status, result = pf.create_pet_simple(auth_key, '', 'Кот', 3)  # Возраст как целое число
    assert status == 400  # Ожидаем ошибку из-за отсутствия имени

def test_create_pet_simple_with_negative_age(auth_key):
    """Проверяем создание питомца с отрицательным возрастом (некорректный случай)"""
    status, result = pf.create_pet_simple(auth_key, 'Мурка', 'Кошка', -1)  # Возраст как целое число
    assert status == 400  # Ожидаем ошибку из-за некорректного возраста

def test_add_photo_to_pet(auth_key, create_pet):
    """Проверяем возможность добавления фото к питомцу"""
    pet_id = create_pet['id']
    pet_photo = os.path.join(os.path.dirname(__file__), 'images/sam.jpeg')  # Исправлено на __file__

    status, result = pf.add_photo_to_pet(auth_key, pet_id, pet_photo)
    assert status == 200
    assert 'pet_photo' in result

def test_add_photo_to_nonexistent_pet(auth_key):
    """Проверяем добавление фото к несуществующему питомцу (некорректный случай)"""
    nonexistent_pet_id = '12345'
    pet_photo = os.path.join(os.path.dirname(__file__), 'images/sam.jpeg')  # Исправлено на __file__

    status, result = pf.add_photo_to_pet(auth_key, nonexistent_pet_id, pet_photo)
    assert status == 404  # Ожидаем ошибку из-за несуществующего питомца

def test_create_multiple_pets(auth_key):
    """Проверяем создание нескольких питомцев"""
    pets_data = [
        {'name': 'Рекс', 'animal_type': 'Собака', 'age': 5},  # Изменено на целое число
        {'name': 'Шарик', 'animal_type': 'Собака', 'age': 3},  # Изменено на целое число
        {'name': 'Котяра', 'animal_type': 'Кошка', 'age': 2},  # Изменено на целое число
        {'name': 'Тигр', 'animal_type': 'Тигр', 'age': 4},      # Изменено на целое число
        {'name': 'Лео', 'animal_type': 'Лев', 'age': 6}          # Изменено на целое число
    ]

    for pet in pets_data:
        status, result = pf.create_pet_simple(auth_key, pet['name'], pet['animal_type'], pet['age'])
        assert status == 200
        assert result['name'] == pet['name']

def test_create_pet_with_special_characters(auth_key):
    """Проверяем создание питомца с именем, содержащим специальные символы"""
    status, result = pf.create_pet_simple(auth_key, '@#$%^&*()', 'Кот', 3)  # Возраст как целое число
    assert status == 200
    assert result['name'] == '@#$%^&*()'

def test_add_photo_with_invalid_format(auth_key, create_pet):
    """Проверяем добавление фото с некорректным форматом (некорректный случай)"""
    pet_id = create_pet['id']
    invalid_photo_path = os.path.join(os.path.dirname(__file__), 'images/invalid_format.txt')  # Некорректный файл

    status, result = pf.add_photo_to_pet(auth_key, pet_id, invalid_photo_path)
    assert status == 400  # Ожидаем ошибку из-за некорректного формата файла

def test_add_multiple_photos_to_pet(auth_key, create_pet):
    """Проверяем возможность добавления нескольких фото к питомцу"""
    pet_id = create_pet['id']

    for i in range(3):  # Добавляем три фотографии
        pet_photo = os.path.join(os.path.dirname(__file__), f'images/sam{i + 1}.jpg')
        status, result = pf.add_photo_to_pet(auth_key, pet_id, pet_photo)
        assert status == 200
        assert 'pet_photo' in result

def test_create_pet_with_empty_animal_type(auth_key):
    """Проверяем создание питомца без указания типа животного (некорректный случай)"""
    status, result = pf.create_pet_simple(auth_key, 'Бобик', '', 2)  # Пустой тип животного
    assert status == 400  # Ожидаем ошибку из-за отсутствия типа животного