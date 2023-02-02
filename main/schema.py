from datetime import datetime
from django.contrib.auth.middleware import get_user
from strawberry import UNSET
from strawberry.types.info import Info
from strawberry_django import auto
from strawberry_django.fields.types import ManyToOneInput, OneToManyInput
from strawberry_django_jwt.decorators import login_required
from strawberry_django_jwt.middleware import JSONWebTokenMiddleware
from strawberry_django_jwt.utils import get_context
import strawberry_django_jwt.mutations as jwt_mutations
from strawberry_django_plus import gql
from strawberry_django_plus.directives import SchemaDirectiveExtension
from strawberry_django_plus.permissions import IsAuthenticated
from typing import Dict, Iterable, List, Optional, Type, cast
from . import models
import custom_user

@gql.django.type(models.Goal)
class Goal:
    id: gql.ID
    name: auto

@gql.django.input(models.Goal)
class GoalInput:
    id: gql.ID
    name: auto

@gql.django.partial(models.Goal)
class GoalInputPartial(gql.NodeInputPartial):
    id: gql.ID

@gql.django.type(models.GroupLesson)
class GroupLesson:
    id: gql.ID
    lesson_set: List["Lesson"]
    notes: auto
    time_in: auto
    time_out: auto
    user: "User"

@gql.django.input(models.GroupLesson)
class GroupLessonInput:
    lesson_set: List["LessonInputNested"]
    notes: auto
    time_in: auto
    time_out: auto
    user: "UserInputPartial"

@gql.django.partial(models.GroupLesson)
class GroupLessonInputPartial(gql.NodeInputPartial):
    id: gql.ID
    lesson_set: Optional[List["LessonInputPartial"]]
    notes: Optional[str]
    time_in: Optional[datetime]
    time_out: Optional[datetime]
    user: Optional["UserInputPartial"]

@gql.django.type(models.Lesson)
class Lesson:
    id: gql.ID
    notes: auto
    rating_set: List["Rating"]
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

@gql.django.input(models.Lesson)
class LessonInputNested:
    notes: auto
    rating_set: Optional[List["RatingInputPartial"]]
    school_id: gql.ID
    student_id: gql.ID
    time_in: auto
    time_out: auto
    user_id: gql.ID

@gql.django.partial(models.Lesson)
class LessonInputPartial(gql.NodeInputPartial):
    id: gql.ID
    notes: Optional[str]
    rating_set: Optional[List["RatingInputPartial"]]
    school: Optional["SchoolInputPartial"]
    student: Optional["StudentInputPartial"]
    time_in: Optional[datetime]
    time_out: Optional[datetime]
    user: Optional["UserInputPartial"]

@gql.django.type(models.Rating)
class Rating:
    id: gql.ID
    goal: Goal
    lesson: Lesson
    score: auto

@gql.django.input(models.Rating)
class RatingInput:
    goal: GoalInputPartial
    lesson: LessonInputPartial
    score: auto

@gql.django.partial(models.Rating)
class RatingInputPartial(gql.NodeInputPartial):
    goal_id: gql.ID
    score: auto

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
    name: Optional[str]

@gql.django.type(models.Student)
class Student:
    id: gql.ID
    first_name: auto
    last_name: auto
    school: "School"
    goals: List["Goal"]

@gql.django.input(models.Student)
class StudentInput:
    first_name: auto
    last_name: auto
    school: "SchoolInputPartial"

@gql.django.partial(models.Student)
class StudentInputPartial(gql.NodeInputPartial):
    id: gql.ID
    first_name: Optional[str]
    last_name: Optional[str]
    school: Optional["SchoolInputPartial"]

@gql.django.type(custom_user.models.User)
class User:
    id: gql.ID
    first_name: auto
    last_name: auto
    email: auto

@gql.django.input(custom_user.models.User)
class UserInput:
    first_name: auto
    last_name: auto
    email: auto
    password: auto

@gql.django.partial(custom_user.models.User)
class UserInputPartial(gql.NodeInputPartial):
    id: gql.ID
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    password: Optional[str]

@gql.type
class Query:
    @login_required
    @gql.django.field
    def user(self, email: Optional[str] = None, id: Optional[gql.ID] = None) -> Optional[User]:
        params = {}
        if (email):
            params["email"] = email
        if (id):
            params["id"] = id
        return custom_user.models.User.objects.filter(**params).first()
    
    goals: list[Goal] = login_required(gql.django.field())
    group_lesson: GroupLesson = login_required(gql.django.field())
    lesson: Lesson = login_required(gql.django.field())
    lessons: list[Lesson] = login_required(gql.django.field())
    school: School = login_required(gql.django.field())
    schools: list[School] = login_required(gql.django.field())
    student: Student = login_required(gql.django.field())
    students: list[Student] = login_required(gql.django.field())
    users: list[User] = login_required(gql.django.field())

@gql.type
class Mutation:
    @login_required
    @gql.django.input_mutation
    def create_group_lesson(
        self,
        info: Info,
        student_ids: List[gql.ID],
        user_id: gql.ID
    ) -> GroupLesson:
        now = datetime.utcnow()
        g = models.GroupLesson.objects.create(time_in = now, user_id = user_id)
        if student_ids.count:
            school_id = models.Student.objects.get(id=student_ids[0]).school.id
            for id in student_ids:
                models.Lesson.objects.create(group_lesson_id=g.id, school_id=school_id, student_id=id, time_in=now, user_id=user_id)
        return cast(GroupLesson, g)

    @login_required
    @gql.django.input_mutation
    def update_group_lesson(
        self,
        info: Info,
        input: GroupLessonInputPartial,
    ) -> GroupLesson:
        group_lesson = models.GroupLesson.objects.get(id=input.id)
        group_lesson.notes=input.notes
        group_lesson.time_out=input.time_out
        for s in input.lesson_set:
            lesson = models.Lesson.objects.get(id=s.id)
            lesson.notes=s.notes
            lesson.time_out=group_lesson.time_out # from the group lesson
            if (s.rating_set != gql.UNSET) and s.rating_set.count:
                lesson.rating_set.all().delete()
                for g in lesson.student.goals.all():
                    lesson.student.goals.remove(g)
                for r in s.rating_set:
                    lesson.rating_set.create(goal_id=r.goal_id, score=r.score)
                    lesson.student.goals.add(r.goal_id)
            lesson.save()
        group_lesson.save()
        return cast(GroupLesson, group_lesson)

    @login_required
    @gql.django.input_mutation()
    def update_lesson(
        self,
        info: Info,
        input: LessonInputPartial,
    ) -> Lesson:
        lesson = models.Lesson.objects.get(id=input.id)
        lesson.notes=input.notes
        lesson.time_out=input.time_out
        if input.rating_set and input.rating_set.count:
            lesson.rating_set.all().delete()
            for g in lesson.student.goals.all():
                lesson.student.goals.remove(g)
            for r in input.rating_set:
                lesson.rating_set.create(goal_id=r.goal_id, score=r.score)
                lesson.student.goals.add(r.goal_id)
        lesson.save()
        return cast(Lesson, lesson)

    #create_group_lesson: GroupLesson = login_required(gql.django.create_mutation(GroupLessonInput))
    #update_group_lesson: GroupLesson = login_required(gql.django.update_mutation(GroupLessonInputPartial))
    #delete_group_lesson: GroupLesson = login_required(gql.django.delete_mutation(gql.NodeInput))
    create_lesson: Lesson = login_required(gql.django.create_mutation(LessonInput))
    #update_lesson: Lesson = login_required(gql.django.update_mutation(LessonInputPartial))
    delete_lesson: Lesson = login_required(gql.django.delete_mutation(gql.NodeInput))
    create_user: User = login_required(gql.django.create_mutation(UserInput))
    update_user: User = login_required(gql.django.update_mutation(UserInputPartial))
    delete_user: User = login_required(gql.django.delete_mutation(gql.NodeInput))
    # JWT Mutations
    token_auth = jwt_mutations.ObtainJSONWebToken.obtain
    verify_token = jwt_mutations.Verify.verify
    refresh_token = jwt_mutations.Refresh.refresh
    delete_token_cookie = jwt_mutations.DeleteJSONWebTokenCookie.delete_cookie

schema = gql.Schema(query=Query, mutation=Mutation, extensions=[JSONWebTokenMiddleware])
