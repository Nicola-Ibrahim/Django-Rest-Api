from apps.accounts.models import Admin, Student, Teacher, User
from hypothesis import HealthCheck, Verbosity, given, settings
from hypothesis import strategies as st
from hypothesis.extra.django import from_model
from hypothesis.stateful import Bundle, RuleBasedStateMachine, precondition, rule


class TestUserModel:
    user_strategy: st.SearchStrategy = from_model(User)

    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        verbosity=Verbosity.verbose,
        deadline=2000,
        max_examples=40,
    )
    @given(user=user_strategy)
    def test_full_name(self, user):
        assert user.get_full_name() == f"{user.first_name} {user.last_name}".strip()

    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        verbosity=Verbosity.verbose,
        deadline=2000,
        max_examples=10,
    )
    @given(user=user_strategy)
    def test_set_password(self, user):
        user.set_password("Django pass")
        user.save()
        assert user.check_password("Django pass") is True


class TestAdminModel:
    user_admin_strategy: st.SearchStrategy = from_model(Admin)

    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        verbosity=Verbosity.verbose,
        deadline=2000,
        max_examples=10,
    )
    @given(user=user_admin_strategy)
    def test_is_admin(self, user):
        assert isinstance(user, Admin)
        assert user.type == User.Type.ADMIN
        assert user.is_staff and user.is_superuser


class TestStudentModel:
    user_student_strategy: st.SearchStrategy = from_model(Student)

    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        verbosity=Verbosity.verbose,
    )
    @given(student=user_student_strategy)
    def test_is_student(self, student):
        assert isinstance(student, Student)
        assert student.type == User.Type.STUDENT
        assert not (student.is_staff or student.is_superuser)


class TestTeacherModel:
    user_teacher_strategy: st.SearchStrategy = from_model(Teacher)

    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        verbosity=Verbosity.verbose,
        deadline=2000,
        max_examples=10,
    )
    @given(user=user_teacher_strategy)
    def test_is_teacher(self, user):
        assert isinstance(user, Teacher)
        assert user.type == User.Type.TEACHER
        assert not (user.is_staff or user.is_superuser)


# class TeacherUserStateMachine(RuleBasedStateMachine):
#     teachers = Bundle("teachers")
#     profiles = Bundle("profiles")

#     @rule(target=teachers, email=st.emails(), password=st.text(min_size=8))
#     def create_user(self, email, password):
#         # This will create a unique User object and save it in the database
#         return User.objects.create_user(email=email, password=password)

#     @rule(target=profiles, teacher=teachers)
#     def create_profile(self, teacher):
#         # This will create a Profile object for the given user and save it in the database
#         return profiles.Teacher.objects.create(teacher=teacher)

#     @precondition(lambda self: self.teachers.count > 0)
#     @rule(teacher=teachers)
#     def check_user_verified(self, teacher):
#         # This will check that the user is verified
#         self.assertTrue(teacher.is_verified)


# TestUserMachine = TeacherUserStateMachine.TestCase
