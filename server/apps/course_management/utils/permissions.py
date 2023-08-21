from server.apps.course_management.models.course import Course
from server.apps.main.models import User


class CourseComponentPermission(object):
    """Permission for course component."""

    @classmethod
    def user_has_permission(cls, user: User, course: Course) -> bool:
        """
        Check if the user has permission to perform actions on the course component.

        Args:
            user (User): The user making the request.
            course (Course): The course associated with the component.

        Returns:
            bool: True if the user has permission, False otherwise.
        """
        return (
            user.is_staff or  # noqa: WPS222
            user.is_admin or
            (user.is_institutional_admin and course.institute == user.institute) or
            (user.is_faculty and course.teacher == user)
        )
