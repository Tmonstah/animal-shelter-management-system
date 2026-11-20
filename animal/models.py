from django.db import models

# Animal model
class Animal(models.Model):
    # Animals gender and hair type have predefined choices.
    ANIMAL_GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]

    ANIMAL_HAIR_TYPE_CHOICES = [
        ("Long", "Long"),
        ("Short", "Short"),
        ("Medium", "Medium"),
    ]

    STATUS_CHOICES = [
        
        ("available", "Available"),
        ("pending", "Pending"),
        ("unavailable", "Unavailable"),
        ("adopted", "Adopted"),
    
    ]

    #id not needed because DJANGO creates a primary key ID automatically
    name = models.CharField(max_length=50)
    animal_type = models.CharField(max_length=50)
    gender = models.CharField(max_length=6, choices=ANIMAL_GENDER_CHOICES)
    personality_desc = models.CharField(max_length=300)
    coloration = models.CharField(max_length=50)
    age = models.IntegerField(default=0)
    breed = models.CharField(max_length=50)
    hair_type = models.CharField(max_length=20, choices=ANIMAL_HAIR_TYPE_CHOICES)
    medical_desc = models.CharField(max_length=300)
    available = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default = "available",
        )
    image = models.ImageField(
        upload_to='animal_pictures/',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.name} (id: {self.id})"

def __str__(self):
    return self.name