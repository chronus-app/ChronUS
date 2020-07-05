from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from core.validators import validate_minutes
from core.degrees_extractor import get_degrees


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Student(models.Model):
    description = models.TextField(blank=True)
    profile_image = models.ImageField(blank=True)
    rating_count = models.PositiveIntegerField(blank=True, null=True, default=0)
    accumulated_rating = models.PositiveIntegerField(blank=True, null=True, default=0)
    available_time = models.DecimalField(blank=True, null=True, default=1, max_digits=6, decimal_places=2, validators=[MinValueValidator(0), validate_minutes])
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    @property
    def average_rating(self):
        return round((self.accumulated_rating/self.rating_count)*2)/2 if self.rating_count != 0 else 0
    
    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class CollaborationRequest(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    requested_time = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.25), validate_minutes])
    deadline = models.DateField()
    publication_date = models.DateField(auto_now_add=True)
    applicant = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='applicant_collaboration_requests')
    offerers = models.ManyToManyField(Student, blank=True, related_name='offerer_collaboration_requests')


class Collaboration(models.Model):
    IN_PROGRESS = 'IP'
    CANCELLED = 'CA'
    PENDING_FINAL = 'PF'
    FINISHED = 'FI'
    STATUS_CHOICES = [
        (IN_PROGRESS, 'In progress'),
        (CANCELLED, 'Cancelled'),
        (PENDING_FINAL, 'Pending final'),
        (FINISHED, 'Finished')
    ]
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    requested_time = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.25), validate_minutes])
    deadline = models.DateField()
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, blank=True, default='IP')
    applicant = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='applicant_collaborations')
    collaborator = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='collaborator_collaborations')


class Competence(models.Model):
    name = models.CharField(max_length=100)
    students = models.ManyToManyField(Student, blank=True, related_name='competences')
    collaboration_requests = models.ManyToManyField(CollaborationRequest, blank=True, related_name='competences')
    collaborations = models.ManyToManyField(Collaboration, blank=True, related_name='competences')

    def __str__(self):
        return self.name


class Degree(models.Model):
    FIRST = '1'
    SECOND = '2'
    THIRD = '3'
    FOURTH = '4'
    FIFTH = '5'
    SIXTH = '6'
    HIGHER_GRADE_CHOICES = [
        (FIRST, '1st'),
        (SECOND, '2nd'),
        (THIRD, '3rd'),
        (FOURTH, '4th'),
        (FIFTH, '5th'),
        (SIXTH, '6th')
    ]
    name = models.CharField(max_length=3, choices=get_degrees())
    higher_grade = models.CharField(blank=True, max_length=1, choices=HIGHER_GRADE_CHOICES)
    finished = models.BooleanField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='degrees')
