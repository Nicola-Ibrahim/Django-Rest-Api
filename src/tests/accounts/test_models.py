from src.apps.accounts.models import models


class TestUserModel:
    def test_full_name(self, db, one_user):
        one_user.first_name = "Django"
        one_user.last_name = "D"
        assert one_user.get_full_name() == "Django D"

    def test_set_password(self, db, one_user):
        one_user.set_password("Django pass")
        assert one_user.check_password("Django pass") is True


class TestAdminModel:
    def test_is_admin(self, one_admin_user):
        assert isinstance(one_admin_user, models.Admin)
        assert one_admin_user.type == models.User.Type.ADMIN
        assert one_admin_user.is_staff and one_admin_user.is_superuser


class TestStudentModel:
    def test_is_student(self, one_student_user):
        assert isinstance(one_student_user, models.Student)
        assert one_student_user.type == models.User.Type.STUDENT
        assert not (one_student_user.is_staff or one_student_user.is_superuser)


class TestTeacherModel:
    def test_is_teacher(self, one_teacher_user):
        assert isinstance(one_teacher_user, models.Teacher)
        assert one_teacher_user.type == models.User.Type.TEACHER
