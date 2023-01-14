from strawberry_django_plus import gql
#from strawberry_django import auto
from typing import Iterable, List, Optional, Type, cast
from . import models

@gql.django.type(models.Lesson)
class Lesson:
    id: gql.ID
    notes: gql.auto

@gql.django.type(models.School)
class School:
    id: gql.ID
    name: gql.auto

@gql.django.type(models.Student)
class Student:
    id: gql.ID
    first_name: gql.auto
    last_name: gql.auto

@gql.django.type(models.User)
class User:
    id: gql.ID
    first_name: gql.auto
    last_name: gql.auto
    email: gql.auto
    password_digest: gql.auto

@gql.django.input(models.Lesson)
class LessonInput:
    notes: gql.auto
    school: "SchoolInputPartial"
    student: "StudentInputPartial"
    time_in: gql.auto
    time_out: gql.auto
    user: "UserInputPartial"

@gql.django.input(models.User)
class UserInput:
    first_name: gql.auto
    last_name: gql.auto
    email: gql.auto
    password_digest: gql.auto

@gql.django.partial(models.Lesson)
class LessonInputPartial(gql.NodeInputPartial):
    id: gql.ID
    notes: gql.auto

@gql.django.partial(models.School)
class SchoolInputPartial(gql.NodeInputPartial):
    id: gql.ID
    name: gql.auto

@gql.django.partial(models.Student)
class StudentInputPartial(gql.NodeInputPartial):
    id: gql.ID
    first_name: gql.auto
    last_name: gql.auto

@gql.django.partial(models.User)
class UserInputPartial(gql.NodeInputPartial):
    id: gql.ID
    first_name: gql.auto
    last_name: gql.auto
    email: gql.auto
    password_digest: gql.auto

@gql.type
class Query:
    lesson: Lesson = gql.django.field()
    lessons: list[Lesson] = gql.django.field()
    user: User = gql.django.field()
    users: list[User] = gql.django.field()

@gql.type
class Mutation:
    create_lesson: Lesson = gql.django.create_mutation(LessonInput)
    update_lesson: Lesson = gql.django.update_mutation(LessonInputPartial)
    delete_lesson: Lesson = gql.django.delete_mutation(gql.NodeInput)
    create_user: User = gql.django.create_mutation(UserInput)
    update_user: User = gql.django.update_mutation(UserInputPartial)
    delete_user: User = gql.django.delete_mutation(gql.NodeInput)

schema = gql.Schema(query=Query, mutation=Mutation)