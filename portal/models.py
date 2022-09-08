from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    GENDERS = (
        ('M','Male'),
        ('F', 'Female')
    )
    ROLES = (
        ('staff', 'staff'),
        ('student', 'student')
    )
    gender = models.CharField(max_length=10, choices=GENDERS, blank=True)
    role = models.CharField(max_length=10, choices=ROLES, default=ROLES[1][1])
    phone = models.CharField(max_length=12, blank=True)
    other_names = models.CharField(max_length=60, blank=True)
    photo = models.ImageField(blank=True, null=True, upload_to="uploads/users/", default="uploads/users/default.png")

class PendingPhoto(models.Model):
    photo = models.ImageField(upload_to="uploads/users/")
    user = models.OneToOneField(User, editable=True, on_delete=models.CASCADE)

class Staff(User):
    class Meta:
        verbose_name = 'Staff'
    STAFFROLES = (
        ('cleaner', 'Cleaner'),
        ('teacher', 'Teacher'),
        ('headteacher', 'Head Teacher'),
        ('norole', 'No Role'),
        ('security', 'Security'),
    )
    staff_role = models.CharField(max_length=20, choices=STAFFROLES)
    date_employed = models.DateField()
    salary = models.IntegerField(blank=True, null=True)

class ClassFees(models.Model):
    class Meta:
        verbose_name_plural = "Classes fees"
    classes = (
        ('Creche', 'Creche'),
        ('PreKg', 'PreKg'),
        ('Kindergarten', 'Kindergarten'),
        ('Nursery 1', 'Nursery 1'),
        ('Nursery 2', 'Nursery 2'),
        ('Grade 1', 'Grade 1'),
        ('Grade 2', 'Grade 2'),
        ('Grade 3', 'Grade 3'),
        ('Grade 4', 'Grade 4'),
        ('Grade 5', 'Grade 5'),
    )
    name = models.CharField(max_length=30, choices=classes)
    new_fee = models.IntegerField(default=0)
    return_fee = models.IntegerField(default=0)

class Class(models.Model):
    class Meta:
        verbose_name_plural = "Classes"
    classes = (
        ('Creche', 'Creche'),
        ('PreKg', 'PreKg'),
        ('Kindergarten', 'Kindergarten'),
        ('Nursery 1', 'Nursery 1'),
        ('Nursery 2', 'Nursery 2'),
        ('Grade 1', 'Grade 1'),
        ('Grade 2', 'Grade 2'),
        ('Grade 3', 'Grade 3'),
        ('Grade 4', 'Grade 4'),
        ('Grade 5', 'Grade 5'),
    )
    name = models.CharField(max_length=30, choices=classes)
    subclass = models.CharField(max_length=30, null=True, blank=True)
    teacher = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)

class Student(User):
    class Meta:
        verbose_name = 'Student'
    current_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)
    date_admitted = models.DateField()
    dob = models.DateField()
