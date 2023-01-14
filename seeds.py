# TODO: There's got to be a better way to do this...

import django
django.setup()
from main.models import Admin, Teacher, School, Goal

admin1 = Admin(first_name="Cynthia",
  last_name="Smith",
  email="cynthia@sparksforsuccess.org",
  activated=True )
admin1.password = "sparksISgr8*"
admin1.password_confirmation = "sparksISgr8*"
admin1.save()

teacher1 = Teacher(first_name="Ima",
  last_name="Test",
  email="test@example.com",
  activated=True )
teacher1.password = "sparksISgr8*"
teacher1.password_confirmation = "sparksISgr8*"
teacher1.save()

school1 = School.objects.create( name="Blackshear", activated=True)
school2 = School.objects.create( name="Kealing", activated=True)
school3 = School.objects.create( name="Oak Springs", activated=True)
school4 = School.objects.create( name="Zavala", activated=True)

Goal.objects.create(name="Active listening")
Goal.objects.create(name="Appropriate behavior")
Goal.objects.create(name="Communication")
Goal.objects.create(name="Emotional expression")
Goal.objects.create(name="Emotional regulation")
Goal.objects.create(name="Following directions")
Goal.objects.create(name="Leadership skills")
Goal.objects.create(name="Making choices")
Goal.objects.create(name="Social skills")
Goal.objects.create(name="Turn taking")
