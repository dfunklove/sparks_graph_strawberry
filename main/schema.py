from datetime import datetime
from strawberry_django import auto
from strawberry_django_jwt.decorators import login_required
from strawberry_django_jwt.middleware import JSONWebTokenMiddleware
import strawberry_django_jwt.mutations as jwt_mutations
from strawberry_django_plus import gql
from strawberry_django_plus.directives import SchemaDirectiveExtension
from strawberry_django_plus.permissions import IsAuthenticated
from typing import Iterable, List, Optional, Type, cast
from . import models
import custom_user

@gql.django.type(models.Lesson)
class Lesson:
    id: gql.ID
    school: "School"
    student: "Student"
    time_in: auto
    time_out: auto
    user: "User"

@gql.django.type(models.School)
class School:
    id: gql.ID
    name: auto

@gql.django.type(models.Student)
class Student:
    id: gql.ID
    first_name: auto
    last_name: auto
    school: "School"

@gql.django.type(custom_user.models.User)
class User:
    id: gql.ID
    first_name: auto
    last_name: auto
    email: auto
    password: auto

@gql.django.input(models.Lesson)
class LessonInput:
    notes: auto
    school: "SchoolInputPartial"
    student: "StudentInputPartial"
    time_in: auto
    time_out: auto
    user: "UserInputPartial"

@gql.django.input(models.School)
class SchoolInput:
    name: auto

@gql.django.input(models.Student)
class StudentInput:
    first_name: auto
    last_name: auto
    school: "SchoolInputPartial"

@gql.django.input(custom_user.models.User)
class UserInput:
    first_name: auto
    last_name: auto
    email: auto
    password: auto

@gql.django.partial(models.Lesson)
class LessonInputPartial(gql.NodeInputPartial):
    id: gql.ID
    notes: Optional[str]
    school: Optional["SchoolInputPartial"]
    student: Optional["StudentInputPartial"]
    time_in: Optional[datetime]
    time_out: Optional[datetime]
    user: Optional["UserInputPartial"]
    
@gql.django.partial(models.School)
class SchoolInputPartial(gql.NodeInputPartial):
    id: gql.ID
    name: Optional[str]

@gql.django.partial(models.Student)
class StudentInputPartial(gql.NodeInputPartial):
    id: gql.ID
    first_name: Optional[str]
    last_name: Optional[str]
    school: Optional["SchoolInputPartial"]

@gql.django.partial(custom_user.models.User)
class UserInputPartial(gql.NodeInputPartial):
    id: gql.ID
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    password: Optional[str]

@gql.type
class Query:
    lesson: Lesson = login_required(gql.django.field())
    lessons: list[Lesson] = login_required(gql.django.field())
    school: School = login_required(gql.django.field())
    schools: list[School] = login_required(gql.django.field())
    student: Student = login_required(gql.django.field())
    students: list[Student] = login_required(gql.django.field())
    user: User = login_required(gql.django.field())
    users: list[User] = login_required(gql.django.field())

@gql.type
class Mutation:
    create_lesson: Lesson = login_required(gql.django.create_mutation(LessonInput))
    update_lesson: Lesson = login_required(gql.django.update_mutation(LessonInputPartial))
    delete_lesson: Lesson = login_required(gql.django.delete_mutation(gql.NodeInput))
    create_user: User = login_required(gql.django.create_mutation(UserInput))
    update_user: User = login_required(gql.django.update_mutation(UserInputPartial))
    delete_user: User = login_required(gql.django.delete_mutation(gql.NodeInput))

schema = gql.Schema(query=Query, mutation=Mutation, extensions=[JSONWebTokenMiddleware])

# This is just a placeholder
@gql.type
class LoginQuery:
    user: User = gql.django.field()

@gql.type
class LoginMutation:
    token_auth = jwt_mutations.ObtainJSONWebToken.obtain
    verify_token = jwt_mutations.Verify.verify
    refresh_token = jwt_mutations.Refresh.refresh
    delete_token_cookie = jwt_mutations.DeleteJSONWebTokenCookie.delete_cookie

login_schema = gql.Schema(query=LoginQuery, mutation=LoginMutation)
