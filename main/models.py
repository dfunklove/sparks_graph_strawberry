# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.db.models import Q
import custom_user

BCRYPT_HASH_LEN = 64
CHAR_FIELD_LEN = 64

class Course(models.Model):
    end_date = models.DateField(blank=True, null=True)
    name = models.CharField(max_length=CHAR_FIELD_LEN)
    notes = models.TextField(blank=True, null=True)
    school = models.ForeignKey('School', models.CASCADE)
    start_date = models.DateField()
    user = models.ForeignKey(custom_user.models.User, models.CASCADE)

    class Meta:
        db_table = 'courses'
        constraints = [models.UniqueConstraint(name='unique_courses_name_school_user', fields = ['name','school','user'])]


class Goal(models.Model):
    name = models.CharField(unique=True, max_length=CHAR_FIELD_LEN)

    class Meta:
        db_table = 'goals'
        constraints = [models.UniqueConstraint(name='unique_goals_name', fields = ['name'])]


class GroupLesson(models.Model):
    course = models.ForeignKey(Course, models.SET_NULL, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    time_in = models.DateTimeField()
    time_out = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(custom_user.models.User, models.CASCADE)

    class Meta:
        db_table = 'group_lessons'
        constraints = [models.UniqueConstraint(name='unique_group_lessons_user_and_time_in', fields = ['user', 'time_in'])]


class Lesson(models.Model):
    group_lesson = models.ForeignKey(GroupLesson, models.CASCADE, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    school = models.ForeignKey('School', models.CASCADE)
    student = models.ForeignKey('Student', models.CASCADE)
    time_in = models.DateTimeField()
    time_out = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(custom_user.models.User, models.CASCADE)

    class Meta:
        db_table = 'lessons'
        constraints = [models.UniqueConstraint(name='unique_lessons_user_and_time_in', fields = ['user', 'time_in'], condition=Q(group_lesson=None))]


class Login(models.Model):
    time_in = models.DateTimeField()
    time_out = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(custom_user.models.User, models.CASCADE)

    class Meta:
        db_table = 'logins'


class Rating(models.Model):
    goal = models.ForeignKey(Goal, models.CASCADE)
    lesson = models.ForeignKey(Lesson, models.CASCADE)
    score = models.IntegerField()

    class Meta:
        db_table = 'ratings'
        constraints = [models.UniqueConstraint(name='unique_ratings_lesson_and_goal', fields = ['lesson', 'goal'])]

class School(models.Model):
    activated = models.BooleanField(blank=True, null=True)
    name = models.CharField(unique=True, max_length=CHAR_FIELD_LEN)

    class Meta:
        db_table = 'schools'
        constraints = [models.UniqueConstraint(name='unique_schools_name', fields = ['name'])]


class Student(models.Model):
    activated = models.BooleanField(blank=True, null=True)
    courses = models.ManyToManyField(Course)
    first_name = models.CharField(max_length=CHAR_FIELD_LEN)
    goals = models.ManyToManyField(Goal)
    last_name = models.CharField(max_length=CHAR_FIELD_LEN)
    permissions = models.TextField(blank=True, null=True)
    school = models.ForeignKey(School, models.CASCADE)

    class Meta:
        db_table = 'students'
        constraints = [models.UniqueConstraint(name='unique_students_name_school', fields = ['first_name','last_name','school'])]

""" This is left as a reference since we have different user model that is compatible with Django auth.
That model is defined in its own app.

class User(models.Model):
    ADMIN = "Admin"
    PARTNER = "Partner"
    TEACHER = "Teacher"
    TYPE_CHOICES = [
        (ADMIN, ADMIN),
        (PARTNER, PARTNER),
        (TEACHER, TEACHER)
    ]
    activated = models.BooleanField(blank=True, null=True)
    email = models.CharField(unique=True, max_length=CHAR_FIELD_LEN)
    first_name = models.CharField(max_length=CHAR_FIELD_LEN)
    last_name = models.CharField(max_length=CHAR_FIELD_LEN)
    password_digest = models.CharField(max_length=BCRYPT_HASH_LEN)
    reset_digest = models.CharField(max_length=CHAR_FIELD_LEN, blank=True, null=True)
    reset_sent_at = models.DateTimeField(blank=True, null=True)
    school_id = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=8,
        choices = TYPE_CHOICES)

    class Meta:
        db_table = 'users'
        constraints = [models.UniqueConstraint(name='unique_users_email', fields = ['email'])]

class Admin(User):
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.type = User.ADMIN

    class Meta:
        proxy = True

class Partner(User):
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.type = User.PARTNER

    class Meta:
        proxy = True

class Teacher(User):
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.type = User.TEACHER

    class Meta:
        proxy = True
"""