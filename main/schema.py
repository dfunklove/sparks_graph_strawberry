from strawberry_django_plus import gql
from strawberry_django import auto
from typing import Iterable, List, Optional, Type, cast
from . import models

@gql.django.type(models.Lesson)
class Lesson:
    id: gql.ID
    school: "School"
    student: "Student"
    time_in: auto
    time_out: auto
    user: "User"

@gql.django.input(models.Lesson)
class LessonInput:
    notes: auto
    school: "SchoolInputPartial"
    student: "StudentInputPartial"
    time_in: auto
    time_out: auto
    user: "UserInputPartial"

@gql.django.partial(models.Lesson)
class LessonInputPartial(gql.NodeInputPartial):
    id: gql.ID
    notes: auto
    school: "SchoolInputPartial"
    student: "StudentInputPartial"
    time_in: auto
    time_out: auto
    user: "UserInputPartial"

@gql.django.type(models.School)
class School:
    id: gql.ID
    name: auto

@gql.django.input(models.School)
class SchoolInput:
    name: auto

@gql.django.partial(models.School)
class SchoolInputPartial(gql.NodeInputPartial):
    id: gql.ID
    name: auto

@gql.django.type(models.Student)
class Student:
    id: gql.ID
    first_name: auto
    last_name: auto
    school: "School"

@gql.django.input(models.Student)
class StudentInput:
    first_name: auto
    last_name: auto
    school: "SchoolInputPartial"

@gql.django.partial(models.Student)
class StudentInputPartial(gql.NodeInputPartial):
    id: gql.ID
    first_name: auto
    last_name: auto
    school: "SchoolInputPartial"

@gql.django.type(models.User)
class User:
    id: gql.ID
    first_name: auto
    last_name: auto
    email: auto
    password_digest: auto

@gql.django.input(models.User)
class UserInput:
    first_name: auto
    last_name: auto
    email: auto
    password_digest: auto

@gql.django.partial(models.User)
class UserInputPartial(gql.NodeInputPartial):
    id: gql.ID
    first_name: auto
    last_name: auto
    email: auto
    password_digest: auto

@gql.type
class Query:
    lesson: Lesson = gql.django.field()
    lessons: list[Lesson] = gql.django.field()
    school: School = gql.django.field()
    schools: list[School] = gql.django.field()
    student: Student = gql.django.field()
    students: list[Student] = gql.django.field()
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