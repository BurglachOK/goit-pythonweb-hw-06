from db import SessionLocal
from select_st import (
    select_1, select_2, select_3, select_4, select_5,
    select_6, select_7, select_8, select_9, select_10
)


session = SessionLocal()

try:
    # Query 1: 5 Students with the highest average grade:
    print("." * 100)
    print("1. Top 5 students by average grade:")
    print("." * 100)
    result = select_1(session)
    for row in result:
        print(f"ID: {row[0]}, Name: {row[1]} {row[2]}, Avg: {row[3]:.2f}")
    
    # Query 2: Student with the highest average grade from a subject:
    print("\n" + "." * 100)
    print("2. Top student by subject:")
    print("." * 100)
    result = select_2(session, "Mathematics")
    if result:
        print(f"ID: {result[0]}, Name: {result[1]} {result[2]}, Avg: {result[3]:.2f}")
    
    # Query 3: Average grade in groups from a subject:
    print("\n" + "." * 100)
    print("3. Average grade by group for subject:")
    print("." * 100)
    result = select_3(session, "Physics")
    for row in result:
        print(f"Group: {row[1]}, Avg: {row[2]:.2f}")
    
    # Query 4: Average grade in the stream:
    print("\n" + "." * 100)
    print("4. Average grade:")
    print("." * 100)
    avg = select_4(session)
    print(f"Stream Average: {avg:.2f}")
    
    # Query 5: Courses taught by a teacher:
    print("\n" + "." * 100)
    print("5. Courses by teacher (teacher_id=1):")
    print("." * 100)
    result = select_5(session, teacher_id=1)
    for subject in result:
        print(f"- {subject.name}")
    
    # Query 6: Students in a group:
    print("\n" + "." * 100)
    print("6. Students in group (group_id=1):")
    print("." * 100)
    result = select_6(session, group_id=1)
    for student in result:
        print(f"- {student.first_name} {student.last_name}")
    
    # Query 7: Grades for group and subject:
    print("\n" + "." * 100)
    print("7. Grades for group and subject (group_name='Group B', subject='Computer Science'):")
    print("." * 100)
    result = select_7(session, "Group B", "Computer Science")
    for row in result:
        print(f"{row[1]} {row[2]}: {row[3]} ({row[4]})")
    
    # Query 8: Average grade given by a teacher:
    print("\n" + "." * 100)
    print("8. Average grade by teacher (teacher_id=1):")
    print("." * 100)
    avg = select_8(session, teacher_id=1)
    print(f"Teacher Average: {avg:.2f}")
    
    # Query 9: Courses attended by a student:
    print("\n" + "." * 100)
    print("9. Courses for student (student_id=1):")
    print("." * 100)
    result = select_9(session, student_id=1)
    for subject in result:
        print(f"- {subject.name}")
    
    # Query 10: Courses for student from teacher
    print("\n" + "." * 100)
    print("10. Courses for student from teacher (student_id=1, teacher_id=1):")
    print("." * 100 )
    result = select_10(session, student_id=1, teacher_id=1)
    for subject in result:
        print(f"- {subject.name}")

finally:
    session.close()
