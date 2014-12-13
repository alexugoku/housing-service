from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class Dorm(models.Model):
    name = models.CharField(max_length=40)
    room_numbers = models.IntegerField(default=0) # classic rooms
    social_room_numbers = models.IntegerField(default=0) # rooms for social cases
    faculty = models.CharField('Faculty', max_length=40)
    description = models.TextField()
    picture = models.FileField(upload_to='uploads')
    map_latitude = models.FloatField(('Latitude'), blank=True, null=True)
    map_longitude = models.FloatField(('Longitude'), blank=True, null=True)

    application_dorms = models.ForeignKey('Application')

class Room(models.Model):
    number = models.CharField(max_length=10)
    size = models.IntegerField(default=0)
    floor = models.IntegerField(default=0)

    dorm = models.ForeignKey(Dorm)

class Application(models.Model):
    publication_date = models.DateTimeField()
    #dorms = models.OneToOneField(Dorm) # de ce? strike 1!
    student = models.OneToOneField('Student')
    attachments = models.ManyToManyField('Document')
    STATUS = ('New', 'Saved', 'Sent', 'Seen', 'Rejected', 'Accepted')
    STATUS_CHOICES = zip(STATUS,STATUS)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='New')
    comment = models.TextField()


class UserManager(BaseUserManager):
    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, last_login=now,
                          is_active=True, is_staff=is_staff,
                          is_superuser=is_superuser,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)



class Student(AbstractBaseUser):
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    county = models.CharField(max_length=30)
    address = models.CharField(max_length=60)
    email = models.EmailField(max_length=40, unique=True)
    grade = models.IntegerField(default=0)
    social_case = models.BooleanField(default=False) # social cases are treated separately
    year = models.IntegerField(default=1)
    selfie = models.FileField(upload_to='uploads')
#    previous_room = models.ForeignKey(Room, related_name='last_year_students') # crashes with current_room

    current_room = models.ForeignKey('Room', related_name='this_year_students', null=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)



class Document(models.Model):
    file = models.FileField(upload_to='uploads')
