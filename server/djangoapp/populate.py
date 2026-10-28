from .models import CarMake, CarModel


def initiate():
    car_make_data = [
        {"name": "Nissan", "description": "Great cars. Japanese technology"},
        {"name": "Mercedes", "description": "Luxury performance. German engineering"},
        {"name": "Audi", "description": "Vorsprung durch Technik. German technology"},
        {"name": "Kia", "description": "Movement that inspires. Korean technology"},
        {"name": "Toyota", "description": "Reliability and innovation. Japanese engineering"},
        {"name": "Honda", "description": "The power of dreams. Advanced mobility"},
        {"name": "Ford", "description": "Built Ford Tough. American craftsmanship"},
    ]

    car_make_instances = {}
    for data in car_make_data:
        make, _ = CarMake.objects.get_or_create(
            name=data['name'],
            defaults={'description': data['description']}
        )
        car_make_instances[data['name']] = make

    car_model_data = [
        {"name": "Pathfinder", "type": "SUV", "year": 2023, "make": "Nissan"},
        {"name": "Qashqai", "type": "SUV", "year": 2023, "make": "Nissan"},
        {"name": "XTRAIL", "type": "SUV", "year": 2023, "make": "Nissan"},
        {"name": "A-Class", "type": "SEDAN", "year": 2023, "make": "Mercedes"},
        {"name": "C-Class", "type": "SEDAN", "year": 2023, "make": "Mercedes"},
        {"name": "E-Class", "type": "SEDAN", "year": 2023, "make": "Mercedes"},
        {"name": "GLE", "type": "SUV", "year": 2023, "make": "Mercedes"},
        {"name": "A4", "type": "SEDAN", "year": 2023, "make": "Audi"},
        {"name": "A5", "type": "COUPE", "year": 2023, "make": "Audi"},
        {"name": "A6", "type": "SEDAN", "year": 2023, "make": "Audi"},
        {"name": "Q5", "type": "SUV", "year": 2023, "make": "Audi"},
        {"name": "Sorrento", "type": "SUV", "year": 2023, "make": "Kia"},
        {"name": "Carnival", "type": "MINIVAN", "year": 2023, "make": "Kia"},
        {"name": "Cerato", "type": "SEDAN", "year": 2023, "make": "Kia"},
        {"name": "Corolla", "type": "SEDAN", "year": 2023, "make": "Toyota"},
        {"name": "Camry", "type": "SEDAN", "year": 2023, "make": "Toyota"},
        {"name": "RAV4", "type": "SUV", "year": 2023, "make": "Toyota"},
        {"name": "Kluger", "type": "SUV", "year": 2023, "make": "Toyota"},
        {"name": "Civic", "type": "SEDAN", "year": 2023, "make": "Honda"},
        {"name": "CR-V", "type": "SUV", "year": 2023, "make": "Honda"},
        {"name": "Explorer", "type": "SUV", "year": 2023, "make": "Ford"},
        {"name": "Mustang", "type": "COUPE", "year": 2023, "make": "Ford"},
    ]

    for data in car_model_data:
        CarModel.objects.get_or_create(
            name=data['name'],
            car_make=car_make_instances[data['make']],
            defaults={
                'type': data['type'],
                'year': data['year']
            }
        )
