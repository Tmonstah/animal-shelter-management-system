from django.test import TestCase
from django.urls import reverse
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
            available=True,
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
            available=True,
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
            available=False,
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

    def test_filters_animals_by_breed(self):
        response = self.client.get(reverse("animal_list"), {"breed": "Cat"})

        self.assertContains(response, "Luna")
        self.assertNotContains(response, "Buddy")
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