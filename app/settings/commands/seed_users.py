from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

class Command(BaseCommand):
    help = "Seeds the database with initial users: 1 superuser, 2 admins, 3 standard users."

    def handle(self, *args, **options):
        self.stdout.write("Seeding users...")

        # 1. Superuser
        self.create_user(
            username="superuser",
            email="superuser@example.com",
            password="password123",
            is_superuser=True,
            is_staff=True,
            role="Superuser"
        )

        # 2. Admins (Wagtail Editors/Moderators)
        # Try to find standard Wagtail groups, fallback to staff status only if not found
        editor_group = Group.objects.filter(name="Editors").first()
        moderator_group = Group.objects.filter(name="Moderators").first()
        
        admin_groups = []
        if editor_group: admin_groups.append(editor_group)
        if moderator_group: admin_groups.append(moderator_group)

        self.create_user(
            username="admin1",
            email="admin1@example.com",
            password="password123",
            is_staff=True,
            groups=admin_groups,
            role="Admin (Editor/Moderator)"
        )

        self.create_user(
            username="admin2",
            email="admin2@example.com",
            password="password123",
            is_staff=True,
            groups=admin_groups,
            role="Admin (Editor/Moderator)"
        )

        # 3. Standard Users
        for i in range(1, 4):
            self.create_user(
                username=f"user{i}",
                email=f"user{i}@example.com",
                password="password123",
                role="Standard User"
            )

        self.stdout.write(self.style.SUCCESS("User seeding complete."))

    def create_user(self, username, email, password, is_superuser=False, is_staff=False, groups=None, role="User"):
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f"User '{username}' already exists. Skipping."))
            return

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=is_staff,
            is_superuser=is_superuser
        )
        
        if groups:
            user.groups.set(groups)
            user.save()

        self.stdout.write(self.style.SUCCESS(f"Created {role}: {username} / {password}"))
