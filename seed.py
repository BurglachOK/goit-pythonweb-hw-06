import random
from datetime import datetime, timedelta

from faker import Faker
from sqlalchemy.exc import IntegrityError

from db import SessionLocal, engine
from models import Base, Group, Student, Teacher, Subject, Grade

fake = Faker()

GROUP_NAMES = ["Group A", "Group B", "Group C"]
SUBJECT_NAMES = [
    "Mathematics",
    "History",
    "Physics",
    "Chemistry",
    "Biology",
    "Literature",
    "Computer Science",
    "English",
]


def random_date(start_days_ago=180):
    return datetime.utcnow() - timedelta(days=random.randint(0, start_days_ago))


def seed_database():
    Base.metadata.create_all(engine)

    with SessionLocal() as session:
        groups = [Group(name=name) for name in GROUP_NAMES]
        session.add_all(groups)
        session.commit()

        teachers = []
        for _ in range(random.randint(3, 5)):
            teacher = Teacher(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.unique.email(),
            )
            teachers.append(teacher)
        session.add_all(teachers)
        session.commit()

        selected_subjects = random.sample(SUBJECT_NAMES, k=random.randint(5, 8))
        subjects = [Subject(name=name, teacher=random.choice(teachers)) for name in selected_subjects]
        session.add_all(subjects)
        session.commit()

        students = []
        for _ in range(random.randint(30, 50)):
            student = Student(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.unique.email(),
                group=random.choice(groups),
            )
            students.append(student)
        session.add_all(students)
        session.commit()

        grades = []
        for student in students:
            subject_sample = random.sample(subjects, k=random.randint(3, len(subjects)))
            for subject in subject_sample:
                for _ in range(random.randint(1, 5)):
                    grades.append(
                        Grade(
                            student=student,
                            subject=subject,
                            score=random.randint(60, 100),
                            created_at=random_date(),
                        )
                    )

        session.add_all(grades)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            print("Seed data contained a duplicate grade. Please rerun seed.py if necessary.")
        else:
            print("Seeded database successfully.")


if __name__ == "__main__":
    seed_database()
