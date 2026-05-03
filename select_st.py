from sqlalchemy import func, select

from models import Group, Student, Teacher, Subject, Grade


def select_1(session, limit=5):
    """Find 5 students with the highest average grade for all subjects."""
    stmt = (
        select(
            Student.id,
            Student.first_name,
            Student.last_name,
            func.avg(Grade.score).label("average_score"),
        )
        .join(Grade)
        .group_by(Student.id)
        .order_by(func.avg(Grade.score).desc())
        .limit(limit)
    )
    return session.execute(stmt).all()


def select_2(session, subject_name):
    """Find the student with the highest average grade for a specific subject."""
    stmt = (
        select(
            Student.id,
            Student.first_name,
            Student.last_name,
            func.avg(Grade.score).label("average_score"),
        )
        .join(Grade)
        .join(Subject)
        .where(Subject.name == subject_name)
        .group_by(Student.id)
        .order_by(func.avg(Grade.score).desc())
        .limit(1)
    )
    return session.execute(stmt).first()


def select_3(session, subject_name):
    """Find the average grade in groups for a specific subject."""
    stmt = (
        select(
            Group.id,
            Group.name,
            func.avg(Grade.score).label("average_score"),
        )
        .join(Group.students)
        .join(Student.grades)
        .join(Grade.subject)
        .where(Subject.name == subject_name)
        .group_by(Group.id)
        .order_by(Group.name)
    )
    return session.execute(stmt).all()


def select_4(session):
    """Find the average grade across the entire database."""
    stmt = select(func.avg(Grade.score).label("average_score"))
    return session.execute(stmt).scalar_one_or_none()


def select_5(session, teacher_id=None, teacher_name=None):
    """Find the courses taught by a specific teacher."""
    stmt = select(Subject).join(Teacher)
    if teacher_id is not None:
        stmt = stmt.where(Teacher.id == teacher_id)
    elif teacher_name is not None:
        name_filter = f"%{teacher_name}%"
        stmt = stmt.where(
            func.concat(Teacher.first_name, ' ', Teacher.last_name).ilike(name_filter)
        )
    else:
        raise ValueError("teacher_id or teacher_name must be provided")
    return session.execute(stmt).scalars().all()


def select_6(session, group_id=None, group_name=None):
    """Find the list of students in a specific group."""
    stmt = select(Student).join(Group)
    if group_id is not None:
        stmt = stmt.where(Group.id == group_id)
    elif group_name is not None:
        stmt = stmt.where(Group.name == group_name)
    else:
        raise ValueError("group_id or group_name must be provided")
    return session.execute(stmt).scalars().all()


def select_7(session, group_name, subject_name):
    """Find the grades of students in a specific group for a specific subject."""
    stmt = (
        select(
            Student.id,
            Student.first_name,
            Student.last_name,
            Grade.score,
            Grade.created_at,
        )
        .join(Student.group)
        .join(Student.grades)
        .join(Grade.subject)
        .where(Group.name == group_name, Subject.name == subject_name)
        .order_by(Student.last_name, Grade.created_at)
    )
    return session.execute(stmt).all()


def select_8(session, teacher_id=None, teacher_name=None):
    """Find the average grade given by a specific teacher for their subjects."""
    stmt = (
        select(func.avg(Grade.score).label("average_score"))
        .join(Grade.subject)
        .join(Subject.teacher)
    )
    if teacher_id is not None:
        stmt = stmt.where(Teacher.id == teacher_id)
    elif teacher_name is not None:
        name_filter = f"%{teacher_name}%"
        stmt = stmt.where(
            func.concat(Teacher.first_name, ' ', Teacher.last_name).ilike(name_filter)
        )
    else:
        raise ValueError("teacher_id or teacher_name must be provided")
    return session.execute(stmt).scalar_one_or_none()


def select_9(session, student_id=None, student_name=None):
    """Find the list of courses attended by a specific student."""
    stmt = select(Subject).join(Subject.grades).join(Grade.student)
    if student_id is not None:
        stmt = stmt.where(Student.id == student_id)
    elif student_name is not None:
        name_filter = f"%{student_name}%"
        stmt = stmt.where(
            func.concat(Student.first_name, ' ', Student.last_name).ilike(name_filter)
        )
    else:
        raise ValueError("student_id or student_name must be provided")
    return session.execute(stmt.distinct()).scalars().all()


def select_10(session, student_id=None, teacher_id=None, student_name=None, teacher_name=None):
    """Find the list of courses a specific student attends for a specific teacher."""
    stmt = (
        select(Subject)
        .join(Subject.grades)
        .join(Grade.student)
        .join(Subject.teacher)
    )
    if student_id is not None:
        stmt = stmt.where(Student.id == student_id)
    elif student_name is not None:
        student_filter = f"%{student_name}%"
        stmt = stmt.where(
            func.concat(Student.first_name, ' ', Student.last_name).ilike(student_filter)
        )
    else:
        raise ValueError("student_id or student_name must be provided")

    if teacher_id is not None:
        stmt = stmt.where(Teacher.id == teacher_id)
    elif teacher_name is not None:
        teacher_filter = f"%{teacher_name}%"
        stmt = stmt.where(
            func.concat(Teacher.first_name, ' ', Teacher.last_name).ilike(teacher_filter)
        )
    else:
        raise ValueError("teacher_id or teacher_name must be provided")

    return session.execute(stmt.distinct()).scalars().all()
