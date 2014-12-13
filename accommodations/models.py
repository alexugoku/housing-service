from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class Dorm(models.Model):

    name = models.CharField(max_length=40) # name of the Dorm
    room_numbers = models.IntegerField(default=0) # no of classic rooms
    social_room_numbers = models.IntegerField(default=0) # no of rooms for social cases
    faculty = models.CharField('Faculty', max_length=40) # Faculty which has students here
    description = models.TextField()  # dorm description
    picture = models.FileField(upload_to='uploads') # picture of the dorm
    map_latitude = models.FloatField(('Latitude'), blank=True, null=True)     # coords for dorm map positioning
    map_longitude = models.FloatField(('Longitude'), blank=True, null=True)

    application_dorms = models.ForeignKey('Application') # an application has many dorms to chose from
    def total(self):
        return self.room_set.aggregate(total=Sum('number'))['total']

class Room(models.Model):
    number = models.CharField(max_length=10) # room number, i.e. name
    size = models.IntegerField(default=0) # room size, i.e. no of max students in the room
    floor = models.IntegerField(default=0) # room floor

    dorm = models.ForeignKey(Dorm) # a dorm has many rooms

class Application(models.Model):
    STATUS = ('New', 'Saved', 'Sent', 'Seen', 'Rejected', 'Accepted')  # possible status of an application
    STATUS_CHOICES = zip(STATUS,STATUS) # tuple of the name nad value
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='New') # the current status
    comment = models.TextField() # comments to be sent to the admin

    publication_date = models.DateTimeField()  # application pub_date
    dorm1 = model.ForeignKey(Dorm)
    dorm2 = model.ForeignKey(Dorm)
    dorm3 = model.ForeignKey(Dorm)
    #dorms = models.OneToOneField(Dorm) # de ce? strike 1!
    student = models.OneToOneField('Student') # one student has one application


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
    grade = models.IntegerField(default=0) # the grade is used for sorting
    social_case = models.BooleanField(default=False) # social cases are treated separately
    year = models.IntegerField(default=1) # student in which year?
    selfie = models.FileField(upload_to='uploads') # picture
#    previous_room = models.ForeignKey(Room, related_name='last_year_students') # related_name avoids crashing with current_room

    current_room = models.ForeignKey('Room', related_name='this_year_students', null=True) # assigned room after sort

    USERNAME_FIELD = 'email'  # email is the log-in token
    objects = UserManager()

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)



class Document(models.Model):
    file = models.FileField(upload_to='uploads')     # the files to be uploaded

    attachment = models.ForeignKey('Application')    # an application has many documents
