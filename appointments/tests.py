from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import CustomerProfile, User


from animal.models import Animal
from appointments.models import Appointment

class AppointmentCreateViewTests(TestCase):
    def setUp(self):
        self.customer = User.objects.create(
            username= "testuser1",
            email= "testuser1@gmail.com",
            password= "TestUser1Pass",
        )
        CustomerProfile.objects.create(
            user= self.customer,
            phone_number= "+12781234567",
            address_line_1= "123 Home St",
            address_line_2= "apt 7",
            city= "Irving",
            state= "Texas",
            postal_code= "75060"
        )
        Animal.objects.create(
            name="Luna",
            animal_type="Cat",
            gender="Female",
            personality_desc="Calm and affectionate",
            coloration="White",
            age=3,
            breed="Cat",
            hair_type="Long",
            medical_desc="Needs checkup",
            available='available',
        )
        Animal.objects.create(
            name="Brave",
            animal_type="Cat",
            gender="Male",
            personality_desc="Calm and affectionate",
            coloration="Orange",
            age=3,
            breed="Cat",
            hair_type="Long",
            medical_desc="Needs checkup",
            available='available',
        )
        Animal.objects.create(
            name="Shadow",
            animal_type="Cat",
            gender="Male",
            personality_desc="Shy",
            coloration="Black",
            age=1,
            breed="Cat",
            hair_type="Short",
            medical_desc="Recovering",
            available='unavailable',
        )


    # Test when the customer is logged in, they can create an appointment
    def test_appointment_create_page_customer_login_loads(self):
        self.client.force_login(self.customer)
        animal = Animal.objects.get(name="Luna")
        response = self.client.get(reverse("appointment_create", args=[animal.id]))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        self.client.force_login(self.customer)
        animal = Animal.objects.get(name="Luna")
        response = self.client.get(reverse("appointment_create", args=[animal.id]))
        self.assertTemplateUsed(response, "appointments/appointment_form.html")
        self.assertContains(response, "Luna")

    # Test when the customer is logged out, they should not be able to create an appointment
    def test_appointment_create_page_customer_logout_loads(self):
        animal = Animal.objects.get(name="Luna")
        response = self.client.get(reverse("appointment_create", args=[animal.id]))
        self.assertEqual(response.status_code, 302)

    # Verify appointment can be made.
    def test_create_appointment(self):
        self.client.force_login(self.customer)
        animal = Animal.objects.get(name="Luna")
        response = self.client.post(reverse("appointment_create", args=[animal.id]),
            {
                "appointment_date": "11/20/2026",
                "appointment_time": "09:00",
            }
        )
        self.assertRedirects(response, reverse("customer_appointments"))

    # Verify appointment can be made for unavilable animals.
    def test_create_appointment(self):
        self.client.force_login(self.customer)
        animal = Animal.objects.get(name="Shadow")
        response = self.client.post(reverse("appointment_create", args=[animal.id]),
            {
                "appointment_date": "11/20/2026",
                "appointment_time": "09:00",
            }
        )
        self.assertEqual(response.status_code, 404)

    # Try to make an appointment on past date, you should not be able to.
    def test_past_appointment_date(self):
        self.client.force_login(self.customer)
        animal = Animal.objects.get(name="Luna")
        response = self.client.post(reverse("appointment_create", args=[animal.id]),
            {
                "appointment_date": "11/18/2026",
                "appointment_time": "09:00",
            }
        )
        self.assertContains(response, "past")

    # Try to make an appointment on past time on today, you should not be able to.
    def test_past_appointment_time(self):
        self.client.force_login(self.customer)
        animal = Animal.objects.get(name="Luna")
        response = self.client.post(reverse("appointment_create", args=[animal.id]),
            {
                "appointment_date": "11/19/2026",
                "appointment_time": "09:00",
            }
        )
        self.assertContains(response, "past")

    # Try to make an appointment on at a time and day of another appointment, you should not be able to.
    def test_multiple_appointment_time_date(self):
        self.client.force_login(self.customer)
        animal = Animal.objects.get(name="Luna")
        response = self.client.post(reverse("appointment_create", args=[animal.id]),
            {
                "appointment_date": "11/21/2026",
                "appointment_time": "09:00",
            }
        )
        animal = Animal.objects.get(name="Brave")
        response = self.client.post(reverse("appointment_create", args=[animal.id]),
            {
                "appointment_date": "11/21/2026",
                "appointment_time": "09:00",
            }
        )
        self.assertContains(response, "already booked")

    # Try to make an appointment with no date and time, you should not be able to.
    def test_no_info_appointment_date(self):
        self.client.force_login(self.customer)
        animal = Animal.objects.get(name="Luna")
        response = self.client.post(reverse("appointment_create", args=[animal.id]),
            {
                "appointment_date": "",
                "appointment_time": "",
            }
        )
        self.assertContains(response, "This field is required")

    # Verify appointment page shows for a customer properly if it has an appointment.
    def test_appointment_page_with_booked_animal(self):
        self.client.force_login(self.customer)
        animal = Animal.objects.get(name="Luna")
        response = self.client.post(reverse("appointment_create", args=[animal.id]),
            {
                "appointment_date": "11/20/2026",
                "appointment_time": "09:00",
            }
        )
        response = self.client.get(reverse("customer_appointments"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Luna")

    # Verify appointment page shows for a customer properly if it has no appointments.
    def test_appointment_page_with_no_booked_animal(self):
        self.client.force_login(self.customer)
        response = self.client.get(reverse("customer_appointments"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "any upcoming")
        

    # def test_appointment_create_page_customer_login_loads(self):
    #     self.client.force_login(self.customer)
    #     animal = Animal.objects.get(name="Luna")
    #     response = self.client.get(reverse("appointment_create", args=[animal.id]))
    #     self.assertEqual(response.status_code, 200)

