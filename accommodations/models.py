from django.db import models


class Dorm(models.Model):
    name = models.CharField(max_length=40)
    room_numbers = models.IntegerField(default=0)
    faculty = models.CharField(max_length=40)


class Room(models.Model):
    number = models.IntegerField(default=0)
    size = models.IntegerField(default=0)

    accomodation = models.ForeignKey(Dorm)


class Application(models.Model):
    publication_date = models.DateTimeField()
    dorms = models.OneToOneField(Dorm)


class Student(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    county = models.CharField(max_length=30)
    address = models.CharField(max_length=60)
    email = models.EmailField()
    grade = models.IntegerField(default=0)
    social_case = models.BooleanField(default=False)  # social cases are treated separately
    year = models.IntegerField(default=1)

    # previous_room = models.ForeignKey(Room) # crashes with current_room
    current_room = models.ForeignKey(Room)


    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)


class Documents(models.Model):
    student = models.ForeignKey(Student)
