import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import CarMake, CarModel


class CarModelTests(TestCase):
    def setUp(self):
        self.make = CarMake.objects.create(
            name="Toyota",
            description="Leading Japanese automaker"
        )
        self.model = CarModel.objects.create(
            car_make=self.make,
            name="Camry",
            type="SEDAN",
            year=2023
        )

    def test_car_make_creation(self):
        self.assertEqual(str(self.make), "Toyota")
        self.assertEqual(self.make.description, "Leading Japanese automaker")

    def test_car_model_creation(self):
        self.assertEqual(str(self.model), "Toyota Camry")
        self.assertEqual(self.model.car_make.name, "Toyota")
        self.assertEqual(self.model.type, "SEDAN")
        self.assertEqual(self.model.year, 2023)


class AuthenticationAPITests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_registration_and_login(self):
        # Test registration
        reg_data = {
            "userName": "ciuser",
            "password": "cipassword123",
            "firstName": "CI",
            "lastName": "Tester",
            "email": "ci@example.com"
        }
        res = self.client.post(
            "/djangoapp/register",
            data=json.dumps(reg_data),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, 200)
        json_resp = res.json()
        self.assertEqual(json_resp.get("status"), "Authenticated")
        self.assertEqual(json_resp.get("userName"), "ciuser")

        # Test login
        login_data = {
            "userName": "ciuser",
            "password": "cipassword123"
        }
        login_res = self.client.post(
            "/djangoapp/login",
            data=json.dumps(login_data),
            content_type="application/json"
        )
        self.assertEqual(login_res.status_code, 200)
        self.assertEqual(login_res.json().get("status"), "Authenticated")

        # Test logout
        logout_res = self.client.get("/djangoapp/logout")
        self.assertEqual(logout_res.status_code, 200)
        self.assertTrue(logout_res.json().get("success"))


class DealerAPITests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_cars(self):
        res = self.client.get("/djangoapp/get_cars")
        self.assertEqual(res.status_code, 200)
        self.assertIn("CarModels", res.json())
        self.assertGreater(len(res.json()["CarModels"]), 0)

    def test_get_dealers(self):
        res = self.client.get("/djangoapp/get_dealers")
        self.assertEqual(res.status_code, 200)
        self.assertIn("dealers", res.json())
