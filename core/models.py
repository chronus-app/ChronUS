from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from core.validators import validate_minutes
from core.degrees_extractor import get_degrees


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Student(models.Model):
    """University student"""
    description = models.TextField(blank=True)
    profile_image = models.ImageField(blank=True)
    rating_count = models.PositiveIntegerField(blank=True, null=True, default=0)
    accumulated_rating = models.PositiveIntegerField(blank=True, null=True, default=0)
    available_time = models.DecimalField(blank=True, null=True, default=1, max_digits=6, decimal_places=2, validators=[MinValueValidator(0), validate_minutes])
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    @property
    def average_rating(self):
        """Returns the student's average rating calculated from the 
        rating count and the accumulated rating"""
        return round((accumulated_rating/rating_count)*2)/2 if rating_count != 0 else 0


class CollaborationRequest(models.Model):
    """Collaboration request that students may publish"""
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    requested_time = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.15), validate_minutes])
    deadline = models.DateTimeField()
    image = models.ImageField()
    publication_date = models.DateField(auto_now=True)
    applicant = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='applicant_collaboration_requests')
    offerers = models.ManyToManyField(Student, blank=True, related_name='offerer_collaboration_requests')


class Collaboration(models.Model):
    """Collaboration that students exchange"""
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
    requested_time = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.15), validate_minutes])
    deadline = models.DateTimeField()
    image = models.ImageField()
    publication_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES)
    applicant = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='applicant_collaborations')
    collaborator = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='collaborator_collaborations')


class Competence(models.Model):
    """Competence that a user can have"""
    name = models.CharField(max_length=100)
    students = models.ManyToManyField(Student, blank=True, related_name='competences')
    collaboration_requests = models.ManyToManyField(CollaborationRequest, blank=True, related_name='competences')
    collaborations = models.ManyToManyField(Collaboration, blank=True, related_name='competences')


class Degree(models.Model):
    """Univerisity degree"""
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
    name = models.CharField(max_length=1, choices=get_degrees())
    higher_grade = models.CharField(blank=True, max_length=1, choices=HIGHER_GRADE_CHOICES)
    finished = models.BooleanField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='degrees')

    def clean(self):
        if self.finished == false and self.higher_grade == '':
            raise ValidationError('The higher grade must not be blank')

        if self.finished == true and self.higher_grade is not '':
            raise ValidationError('You cannot specify a higher grade if the degree is finished')