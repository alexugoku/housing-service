from django.contrib import admin
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


class Dorm(models.Model):
    name = models.CharField(max_length=40)
    room_numbers = models.IntegerField(default=0)  # classic rooms
    social_room_numbers = models.IntegerField(default=0)  # rooms for social cases
    faculty = models.CharField('Faculty', max_length=40)
    description = models.TextField()
    picture = models.FileField(upload_to='uploads', blank=True)
    map_latitude = models.FloatField('Latitude', blank=True, null=True)
    map_longitude = models.FloatField('Longitude', blank=True, null=True)

    application_dorms = models.ForeignKey('Application', blank=True, null=True)

    def __unicode__(self):
        return self.name


class Room(models.Model):
    number = models.CharField(max_length=10)
    size = models.IntegerField(default=0)
    floor = models.IntegerField(default=0)

    dorm = models.ForeignKey(Dorm)


class Application(models.Model):
    publication_date = models.DateTimeField(auto_now_add=True)
    # dorms = models.OneToOneField(Dorm) # de ce? strike 1!
    student = models.OneToOneField('Student')
    attachments = models.ManyToManyField('Document', blank=True)
    STATUS = ('New', 'Saved', 'Sent', 'Seen', 'Rejected', 'Accepted')
    STATUS_CHOICES = zip(STATUS, STATUS)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='New')
    comment = models.TextField()

    dorm1 = models.ForeignKey(Dorm, related_name='first_option')
    dorm2 = models.ForeignKey(Dorm, related_name='2nd_option')
    dorm3 = models.ForeignKey(Dorm, related_name='3rd_option')

    def __unicode__(self):
        return u'%s %s @ %s' % (self.status, self.student, self.publication_date)


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

    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    county = models.CharField(max_length=30, blank=True, null=True)
    address = models.CharField(max_length=60, blank=True, null=True)
    email = models.EmailField(max_length=40, unique=True, blank=True)
    grade = models.IntegerField(default=0)
    social_case = models.BooleanField(default=False)  # social cases are treated separately
    year = models.IntegerField(default=1)
    selfie = models.FileField(upload_to='uploads', blank=True, null=True)
    # previous_room = models.ForeignKey(Room, related_name='last_year_students') # crashes with current_room

    current_room = models.ForeignKey('Room', related_name='this_year_students', blank=True, null=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def has_module_perms(self, *args):
        return True

    def has_perm(self, *args):
        return True

    def get_full_name(self):
        return self.first_name

    def get_short_name(self):
        return self.last_name


    def __unicode__(self):
        return u'%s' % self.email


class Document(models.Model):
    file = models.FileField(upload_to='uploads')


admin.site.register(Student)
admin.site.register(Dorm)
admin.site.register(Application)
