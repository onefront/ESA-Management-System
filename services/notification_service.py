from extensions import db
from models.notification import Notification
from models.member import Member


def notify_class_members(class_group, title, message, link=None):

    print("=" * 60)
    print("Notification function started")
    print("Class Group:", class_group.id)

    members = Member.query.filter_by(
        class_group_id=class_group.id
    ).all()

    print("Members found:", len(members))

    notifications = []

    for member in members:

        print(
            f"Member ID={member.id}, "
            f"User ID={member.user_id}"
        )

        if member.user_id is None:
            print("Skipped (no user account)")
            continue

        notification = Notification(
            user_id=member.user_id,
            title=title,
            message=message,
            notification_type="Class Notice",
            link=link,
            is_read=False
        )

        notifications.append(notification)
        print("Notification prepared")

    print("Total notifications:", len(notifications))

    if notifications:
        db.session.add_all(notifications)
        db.session.commit()
        print("Notifications saved!")

    print("=" * 60)