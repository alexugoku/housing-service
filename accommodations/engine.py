from accommodations.models import Student, Dorm, Room, Application, Document


social_case_students = Student.objects.filter(current_room_id=None, social_case=True)
students = Student.objects.filter(current_room_id=None, social_case=False)

sorted_social_case_students = sorted(social_case_students, key=lambda student:student.grade) # sort the social case students

sorted_students = sorted(students, key=lambda student:student.grade) # sort the students

for i in room_numbers:
    
