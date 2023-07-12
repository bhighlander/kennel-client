from .location_requests import get_single_location
from .customer_requests import get_single_customer

ANIMALS = [
    {
        "id": 1,
        "name": "Snickers",
        "species": "Dog",
        "locationId": 1,
        "customerId": 3,
        "status": "Admitted"
    },
    {
        "id": 2,
        "name": "Roman",
        "species": "Dog",
        "locationId": 1,
        "customerId": 2,
        "status": "Admitted"
    },
    {
        "id": 3,
        "name": "Blue",
        "species": "Cat",
        "locationId": 2,
        "customerId": 1,
        "status": "Admitted"
    }
]


def get_all_animals():
    return ANIMALS

def get_single_animal(id):
    requested_animal = None
    for animal in ANIMALS:
        if animal["id"] == id:
            requested_animal = animal

            location = get_single_location(requested_animal["id"])
            customer = get_single_customer(requested_animal["id"])

            requested_animal["location"] = location
            requested_animal["customer"] = customer

            requested_animal.pop("locationId", None)
            requested_animal.pop("customerId", None)

    return requested_animal

def create_animal(animal):
    max_id = ANIMALS[-1]["id"]
    new_id = max_id + 1
    animal["id"] = new_id
    ANIMALS.append(animal)
    return animal

def delete_animal(id):
    animal_index = -1
    for index, animal in enumerate(ANIMALS):
        if animal["id"] == id:
            animal_index = index
    if animal_index >= 0:
        ANIMALS.pop(animal_index)

def update_animal(id, new_animal):
    for index, animal in enumerate(ANIMALS):
        if animal["id"] == id:
            ANIMALS[index] = new_animal
            break
