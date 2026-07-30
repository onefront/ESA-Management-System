import os
from flask import request, redirect, url_for

from flask import (
    Flask,
    render_template,
    redirect,
    url_for
)
from flask_migrate import Migrate

from models.slider import Slider
from flask_login import current_user

from models.executive import Executive
from config import Config
from routes.events import events_bp
from routes.member_import import member_import_bp
from models.event import Event
from extensions import db, login_manager
from routes.programmes import programmes_bp
from routes.attendance import attendance_bp
from routes.candidates import candidates_bp
from routes.reports import reports_bp
from routes.lecturers import lecturers_bp
from routes.auth import auth_bp
from routes.class_groups import class_groups_bp
from routes.payment_settings import payment_settings_bp
from routes.chat_admin import chat_admin_bp
from routes.notifications import notifications_bp





# Import models
from models.class_notice import ClassNotice
from models.payment_settings import PaymentSettings
from models.class_group import ClassGroup
from models.course_rep import CourseRep
from models.attendance import Attendance
from models.department import Department
from models.faculty import Faculty
from models.member_application import MemberApplication
from models.member import Member
from models.programme import Programme
from models.payment import Payment
from models.election import Election
from models.election_settings import ElectionSettings
from models.portfolio import Portfolio
from models.system_settings import SystemSettings
from models.lecturer import Lecturer
from models.vote import Vote
from models.audit_log import AuditLog
from models.class_announcement import ClassAnnouncement
from models.announcement import Announcement
from models.conversation import Conversation
from models.conversation_member import ConversationMember
from models.message import Message
from models.message_read import MessageRead
from models.attachment import Attachment
from models.chat_setting import ChatSetting
from models.chat_block import ChatBlock
from models.notice import Notice
from models.message import Message
from models.user import User
from models.notification import Notification


# Create Flask App
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)

migrate = Migrate(app, db)



@app.context_processor
def inject_notifications():

    unread_count = 0

    if current_user.is_authenticated:

        unread_count = (
            Notification.query
            .filter_by(
                user_id=current_user.id,
                is_read=False
            )
            .count()
        )

    return dict(
        unread_notifications=unread_count
    )
# print("=" * 60)
# print("Template Folder:", app.template_folder)
# print("Root Path:", app.root_path)
# print("=" * 60)

#
# print("=" * 80)
# print("Template Folder:", app.template_folder)
# print("Root Path:", app.root_path)
# print("=" * 80)

# Upload folder configuration
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load configuration
app.config.from_object(Config)





from routes.class_notices import class_notices_bp
from routes.backup import backup_bp
from routes.messages import messages_bp
from routes.sliders import sliders_bp
from routes.member_indexes import member_indexes_bp
from routes.course_reps import course_reps_bp
from routes.notices import notices_bp
from routes.member_portal import member_portal_bp
from routes.applications import applications_bp
from routes.registration import registration_bp
from routes.history import history_bp
from routes.dashboard import dashboard_bp
from routes.audit import audit_bp
from routes.analytics import analytics_bp
from routes.members import members_bp
from routes.payments import payments_bp
from routes.executives import executives_bp
from routes.departments import departments_bp
from routes.reports import reports_bp
from routes.voting import voting_bp
from routes.results import results_bp
from routes.election_control import control_bp
from routes.election_settings import settings_bp
from routes.users import users_bp
from routes.elections import elections_bp
from routes.portfolios import portfolios_bp
from routes.candidates import candidates_bp
from routes.settings import settings_bp
from routes.election_settings import settings_bp as election_settings_bp
from routes.academic_class import academic_class_bp
from routes.member_payments import member_payments_bp
from routes.class_announcements import class_announcements_bp
from routes.payment_approval import payment_approval_bp
from routes.slides import slides_bp
from routes.chat_block import chat_block_bp





# Register blueprints
app.register_blueprint(notifications_bp)
app.register_blueprint(class_notices_bp)
app.register_blueprint(backup_bp)
app.register_blueprint(chat_block_bp)
app.register_blueprint(chat_admin_bp)
app.register_blueprint(messages_bp)
app.register_blueprint(slides_bp)
app.register_blueprint(sliders_bp)
app.register_blueprint(member_payments_bp)
app.register_blueprint(payment_settings_bp)
app.register_blueprint(payment_approval_bp)
app.register_blueprint(class_announcements_bp)
app.register_blueprint(academic_class_bp)
app.register_blueprint(member_indexes_bp)
app.register_blueprint(course_reps_bp)
app.register_blueprint(lecturers_bp)
app.register_blueprint(notices_bp)
app.register_blueprint(member_portal_bp)
app.register_blueprint(applications_bp)
app.register_blueprint(history_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(audit_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(results_bp)
app.register_blueprint(control_bp)
app.register_blueprint(members_bp)
app.register_blueprint(candidates_bp)
app.register_blueprint(payments_bp)
app.register_blueprint(executives_bp)
app.register_blueprint(events_bp)
app.register_blueprint(elections_bp)
app.register_blueprint(departments_bp)
app.register_blueprint(attendance_bp)
app.register_blueprint(member_import_bp)
app.register_blueprint(reports_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(voting_bp)
app.register_blueprint(programmes_bp)
app.register_blueprint(users_bp)
app.register_blueprint(portfolios_bp)
app.register_blueprint(registration_bp)
app.register_blueprint(settings_bp)
app.register_blueprint(election_settings_bp)
app.register_blueprint(class_groups_bp)



# python app.py
# print(app.url_map)



@app.context_processor
def inject_permissions():

    def get_member():
        if not current_user.is_authenticated:
            return None
        return getattr(current_user, "member_profile", None)

    def get_course_rep():
        member = get_member()
        if member is None:
            return None
        return member.course_rep

    def is_admin():
        return (
            current_user.is_authenticated
            and current_user.role == "Administrator"
        )

    def is_general_secretary():
        return (
            current_user.is_authenticated
            and current_user.role == "General Secretary"
        )

    def is_course_rep():
        rep = get_course_rep()

        print("========== COURSE REP DEBUG ==========")
        print("User:", current_user.username)
        print("Role:", current_user.role)
        print("Member:", get_member())
        print("Course Rep Record:", rep)

        if rep:
            print("Position:", rep.position)
            print("Status:", rep.status)

        result = (
                rep is not None
                and rep.status == "Active"
                and rep.position == "Course Rep"
        )

        print("Is Course Rep:", result)
        print("======================================")

        return result
        rep = get_course_rep()
        return (
            rep is not None
            and rep.status == "Active"
            and rep.position == "Course Rep"
        )

    def is_assistant_course_rep():
        rep = get_course_rep()
        return (
            rep is not None
            and rep.status == "Active"
            and rep.position == "Assistant Course Rep"
        )

    def can_view_lecturer_directory():



        if current_user.is_authenticated:
            pass
             # print("User:", current_user.username)
            # print("Role:", current_user.role)

        member = get_member()
        # print("Member:", member)

        rep = get_course_rep()
        # print("Course Rep:", rep)

        if rep:
            pass
            # print("Position:", rep.position)
            # print("Status:", rep.status)

        result = (
            is_admin()
            or is_general_secretary()
            or is_course_rep()
            or is_assistant_course_rep()
        )
        #
        # print("Permission:", result)
        # print("=" * 60)

        return result

    return {
        "is_admin": is_admin,
        "is_general_secretary": is_general_secretary,
        "is_course_rep": is_course_rep,
        "is_assistant_course_rep": is_assistant_course_rep,
        "can_view_lecturer_directory": can_view_lecturer_directory,
    }
# Initialize database



@app.before_request
def force_password_change():

    if not current_user.is_authenticated:
        return

    if not current_user.must_change_password:
        return

    allowed_endpoints = {
        "auth.change_password",
        "auth.logout",
        "auth.login",
        "static"
    }

    if request.endpoint in allowed_endpoints:
        return

    return redirect(url_for("auth.change_password"))



@login_manager.user_loader
def load_user(user_id):
        return User.query.get(int(user_id))
with app.app_context():
    db.create_all()

@app.route("/")
def home():

    if current_user.is_authenticated:

        if current_user.role == "Member":

            return redirect(
                url_for("member_portal.dashboard")
            )

        return redirect(
            url_for("dashboard.dashboard")
        )

    return render_template(
        "public/index.html"
    )


if __name__ == "__main__":
    app.run(debug=True)
