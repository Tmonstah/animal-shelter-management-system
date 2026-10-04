from django.db import models

# Animal model
# TODO add option for picture, intake_day, adoption_day
#       animal_type
class Animal(models.Model):
    # Animals gender and hair type have predefined choices.
    MALE = "M"
    FEMALE = "F"
    LONG = "LONG"
    SHORT = "SHORT"
    MED = "MEDIUM"
    ANIMAL_GENDER_CHOICES = {MALE: "Male", FEMALE: "Female"}
    ANIMAL_HAIR_TYPE_CHOICES = {LONG: "Long", SHORT: "Short", MED: "Medium"}

    #id not needed because DJANGO creates a primary key ID automatically
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=6, choices=ANIMAL_GENDER_CHOICES)
    personality_desc = models.CharField(max_length=300)
    coloration = models.CharField(max_length=50)
    breed = models.CharField(max_length=50)
    hair_type = models.CharField(max_length=20, choices=ANIMAL_HAIR_TYPE_CHOICES)
    medical_desc = models.CharField(max_length=300)
    available = models.BooleanField(default=True)

def __str__(self):
    return self.name