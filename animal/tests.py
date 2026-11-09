from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from animal.models import Animal

class AnimalListViewTests(TestCase):
    def setUp(self):
        Animal.objects.create(
            name="Buddy",
            gender="M",
            personality_desc="Friendly and playful",
            coloration="Brown",
            age=2,
            breed="Mixed",
            hair_type="SHORT",
            medical_desc="Healthy and vaccinated",
            available='available',
        )
        Animal.objects.create(
            name="Luna",
            gender="F",
            personality_desc="Calm and affectionate",
            coloration="White",
            age=3,
            breed="Cat",
            hair_type="LONG",
            medical_desc="Needs checkup",
            available='available',
        )
        Animal.objects.create(
            name="Shadow",
            gender="M",
            personality_desc="Shy",
            coloration="Black",
            age=1,
            breed="Cat",
            hair_type="SHORT",
            medical_desc="Recovering",
            available='unavailable',
        )

    def test_animal_list_page_loads(self):
        response = self.client.get(reverse("animal_list"))
        self.assertEqual(response.status_code, 200)

    def test_only_available_animals_are_displayed(self):
        response = self.client.get(reverse("animal_list"))
        self.assertContains(response, "Buddy")
        self.assertContains(response, "Luna")
        self.assertNotContains(response, "Shadow")

    def test_template_used(self):
        response = self.client.get(reverse("animal_list"))
        self.assertTemplateUsed(response, "shelter_project/animal_listing.html")

    def test_animal_profile_shows_details(self):
        animal = Animal.objects.get(name="Buddy")

        response = self.client.get(
            reverse("animal_detail", args=[animal.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "shelter_project/animal_detail.html")
        self.assertContains(response, "Friendly and playful")
        self.assertContains(response, "Brown")
        self.assertContains(response, "Healthy and vaccinated")

    def test_unavailable_animal_profile_returns_404(self):
        animal = Animal.objects.get(name="Shadow")

        response = self.client.get(
            reverse("animal_detail", args=[animal.id])
        )

        self.assertEqual(response.status_code, 404)

    def test_filters_animals_by_breed(self):
        response = self.client.get(reverse("animal_list"), {"breed": "Cat"})

        self.assertContains(response, "Luna")
        self.assertNotContains(response, "Buddy")
        self.assertNotContains(response, "Shadow")

    def test_searches_by_exact_match(self):
        response = self.client.get(reverse("animal_list"), {"name": "Shadow"})

        self.assertContains(response, "Shadow")
        self.assertNotContains(response, "Buddy")
        self.assertNotContains(response, "Luna")

    def test_searches_animals_by_case_insensitive_partial_name(self):
        response = self.client.get(reverse("animal_list"), {"name": "UN"})

        self.assertContains(response, "Luna")
        self.assertNotContains(response, "Buddy")
        self.assertNotContains(response, "Shadow")

    def test_search_combines_with_other_filters(self):
        response = self.client.get(
            reverse("animal_list"), {"name": "u", "breed": "Mixed"}
        )

        self.assertContains(response, "Buddy")
        self.assertNotContains(response, "Luna")
        self.assertNotContains(response, "Shadow")

    def test_filters_animals_by_gender(self):
        response = self.client.get(reverse("animal_list"), {"gender": "F"})

        self.assertContains(response, "Luna")
        self.assertNotContains(response, "Buddy")

    def test_filters_animals_by_inclusive_age_range(self):
        response = self.client.get(
            reverse("animal_list"), {"min_age": "2", "max_age": "3"}
        )

        self.assertContains(response, "Buddy")
        self.assertContains(response, "Luna")
        self.assertNotContains(response, "Shadow")

    def test_combines_filters(self):
        response = self.client.get(
            reverse("animal_list"),
            {"breed": "Cat", "gender": "F", "min_age": "3", "max_age": "3"},
        )

        self.assertContains(response, "Luna")
        self.assertNotContains(response, "Buddy")

    def test_invalid_age_range_shows_validation_error(self):
        response = self.client.get(
            reverse("animal_list"), {"min_age": "4", "max_age": "2"}
        )

        self.assertContains(response, "Maximum age must be at least the minimum age.")
        self.assertContains(response, "Buddy")
        self.assertContains(response, "Luna")


class AnimalCreateViewTests(TestCase):
    def setUp(self):
        self.employee = get_user_model().objects.create_user(
            username="employee",
            password="test-password",
            is_staff=True,
        )
        self.customer = get_user_model().objects.create_user(
            username="customer",
            password="test-password",
        )
        self.animal_data = {
            "name": "New Friend",
            "gender": "F",
            "personality_desc": "Gentle and curious",
            "coloration": "Gray",
            "age": "4",
            "breed": "Domestic Shorthair",
            "hair_type": "SHORT",
            "medical_desc": "Healthy",
        }

    def test_anonymous_users_are_redirected_to_login(self):
        response = self.client.get(reverse("animal_create"))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('animal_create')}",
        )

    def test_customers_cannot_access_add_animal_page(self):
        self.client.force_login(self.customer)

        response = self.client.get(reverse("animal_create"))

        self.assertEqual(response.status_code, 403)

    def test_employee_can_add_animal(self):
        self.client.force_login(self.employee)

        response = self.client.post(reverse("animal_create"), self.animal_data)

        self.assertRedirects(response, reverse("animal_list"))
        animal = Animal.objects.get(name="New Friend")
        self.assertTrue(animal.available)

    def test_superuser_can_add_animal(self):
        manager = get_user_model().objects.create_superuser(
            username="manager",
            password="test-password",
            email="manager@example.com",
        )
        self.client.force_login(manager)

        response = self.client.post(reverse("animal_create"), self.animal_data)

        self.assertRedirects(response, reverse("animal_list"))
        self.assertTrue(Animal.objects.filter(name="New Friend").exists())

    def test_animal_list_shows_add_link_only_to_employee(self):
        self.client.force_login(self.employee)
        employee_response = self.client.get(reverse("animal_list"))
        self.assertContains(employee_response, reverse("animal_create"))

        self.client.force_login(self.customer)
        customer_response = self.client.get(reverse("animal_list"))
        self.assertNotContains(customer_response, reverse("animal_create"))

        self.client.logout()
        anonymous_response = self.client.get(reverse("animal_list"))
        self.assertNotContains(anonymous_response, reverse("animal_create"))

    def test_cannot_add_animal_when_50_are_available(self):
        self.client.force_login(self.employee)
        for index in range(50):
            Animal.objects.create(
                name=f"Available {index}",
                gender="M",
                personality_desc="Friendly",
                coloration="Brown",
                age=1,
                breed="Mixed",
                hair_type="SHORT",
                medical_desc="Healthy",
                available='available',
            )

        response = self.client.post(reverse("animal_create"), self.animal_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "maximum of 50 available animals")
        self.assertFalse(Animal.objects.filter(name="New Friend").exists())

    def test_unavailable_animals_do_not_count_toward_limit(self):
        self.client.force_login(self.employee)
        for index in range(50):
            Animal.objects.create(
                name=f"Unavailable {index}",
                gender="M",
                personality_desc="Friendly",
                coloration="Brown",
                age=1,
                breed="Mixed",
                hair_type="SHORT",
                medical_desc="Healthy",
                available='unavailable',
            )

        response = self.client.post(reverse("animal_create"), self.animal_data)

        self.assertRedirects(response, reverse("animal_list"))
        self.assertEqual(Animal.objects.filter(available='available').count(), 1)