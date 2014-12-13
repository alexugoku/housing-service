from accommodations.models import Student, Dorm, Room, Application, Document


social_case_students = Student.objects.filter(current_room_id=None, social_case=True)
students = Student.objects.filter(current_room_id=None, social_case=False)

sorted_social_case_students = sorted(social_case_students, key=lambda student:student.grade) # sort the social case students

sorted_students = sorted(students, key=lambda student:student.grade) # sort the students


dorms = Dorm.objects.all()

for d in dorms:
    for r in d.room_set.all(): # r.number returneaza din Room
        normal_dorms[d.name[r.number]] = r.size

#for ss in sorted_students:
#    normal_dorms[]
