from functools import wraps
from flask import abort
from flask_login import current_user
from models.course_rep import CourseRep

def roles_required(*roles):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            #
            # print("=" * 60)
            # print("Current User Type:", type(current_user))
            # print("Current User Class:", current_user.__class__)
            # print("Current User Dict:", getattr(current_user, "__dict__", {}))
            # print("Has role:", hasattr(current_user, "role"))

            if not current_user.is_authenticated:
                abort(401)

            if not hasattr(current_user, "role"):
                abort(500, description="User object has no role attribute.")

            if current_user.role not in roles:
                abort(403)

            return func(*args, **kwargs)

        return wrapper

    return decorator


def lecturer_directory_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        # print("=" * 60)
        # print("USER:", current_user.username)
        # print("ROLE:", current_user.role)

        if not current_user.is_authenticated:
            # print("NOT AUTHENTICATED")
            abort(401)

        if current_user.role in [
            "Administrator",
            "General Secretary"
        ]:
            # print("ADMIN ACCESS")
            return func(*args, **kwargs)

        if current_user.role == "Member":

            member = getattr(current_user, "member_profile", None)

            # print("MEMBER:", member)

            if member is None:
                # print("NO MEMBER PROFILE")
                abort(403)

            # print("MEMBER ID:", member.id)

            rep = CourseRep.query.filter_by(
                member_id=member.id
            ).first()

            # print("COURSE REP:", rep)

            if rep:
                print("POSITION:", rep.position)

            if rep and rep.position in [
                "Course Rep",
                "Assistant Course Rep"
            ]:
                print("ACCESS GRANTED")
                return func(*args, **kwargs)

        # print("ACCESS DENIED")
        abort(403)

    return wrapper
def admin_required(func):
    return roles_required("Administrator")(func)