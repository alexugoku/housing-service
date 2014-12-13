from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class Dorm(models.Model):
    name = models.CharField(max_length=40) # name of the Dorm
    room_numbers = models.IntegerField(default=0) # no of classic rooms
    social_room_numbers = model.IntegerField(default=0) # no of rooms for social cases
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
    #dorms = models.OneToOneField(Dorm) # de ce? strike 1!
    student = models.OneToOneField('Student') # one student has one application

class Student(AbstractBaseUser):
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

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)



class Document(models.Model):
    file = models.FileField(upload_to='uploads')     # the files to be uploaded

    attachment = models.ForeignKey('Application')    # an application has many documents
