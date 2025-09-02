from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
import random

from core.apps.resumes.models.permission import Permission
from core.apps.resumes.models.role import Role
from core.apps.resumes.models.role_permission import RolePermission
from core.apps.resumes.models.staff import Staff
from core.apps.resumes.models.department import Department
from core.apps.resumes.models.team import Team
from core.apps.resumes.models.department_group import DepartmentGroup
from core.apps.resumes.models.user_group import UserGroup
from core.apps.resumes.models.user_role import UserRole



fake = Faker("ru_RU")


class Command(BaseCommand):
    help = "Генерация тестовых данных для всех моделей"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("=== Очищаем старые данные ==="))

        UserRole.objects.all().delete()
        UserGroup.objects.all().delete()
        RolePermission.objects.all().delete()
        Staff.objects.all().delete()
        DepartmentGroup.objects.all().delete()
        Permission.objects.all().delete()
        Role.objects.all().delete()
        Team.objects.all().delete()
        Department.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

        self.stdout.write(self.style.SUCCESS("Данные очищены!"))

        # Departments
        departments = [
            Department.objects.create(
                title=fake.unique.company(),
                description=fake.text(max_nb_chars=120),
            )
            for _ in range(3)
        ]
        self.stdout.write(self.style.SUCCESS(f"Создано департаментов: {len(departments)}"))

        # Teams
        teams = [
            Team.objects.create(
                title=fake.unique.bs().title(),
                description=fake.text(max_nb_chars=120),
            )
            for _ in range(5)
        ]
        self.stdout.write(self.style.SUCCESS(f"Создано групп: {len(teams)}"))

        # Department <-> Team links
        for t in teams:
            DepartmentGroup.objects.create(
                department=random.choice(departments), group=t
            )
        self.stdout.write(self.style.SUCCESS("Связаны департаменты и группы"))

        # Roles
        roles = [
            Role.objects.create(
                title=fake.unique.job(),
                description=fake.text(max_nb_chars=80),
            )
            for _ in range(4)
        ]
        self.stdout.write(self.style.SUCCESS(f"Создано ролей: {len(roles)}"))

        # Permissions
        permissions = [
            Permission.objects.create(
                title=fake.word().capitalize(),
                code=fake.unique.lexify(text="perm_????"),
                description=fake.text(max_nb_chars=60),
            )
            for _ in range(6)
        ]
        self.stdout.write(self.style.SUCCESS(f"Создано разрешений: {len(permissions)}"))

        # Role <-> Permission links
        for r in roles:
            for p in random.sample(permissions, k=random.randint(1, 3)):
                RolePermission.objects.create(role=r, permission=p)
        self.stdout.write(self.style.SUCCESS("Связаны роли и разрешения"))

        # Users & Staff
        users = []
        for _ in range(10):
            user = User.objects.create_user(
                username=fake.unique.user_name(),
                email=fake.unique.email(),
                password="test1234",
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            )
            Staff.objects.create(
                user=user,
                department=random.choice(departments),
            )
            users.append(user)
        self.stdout.write(self.style.SUCCESS(f"Создано пользователей: {len(users)}"))

        # User <-> Group links
        for u in users:
            for t in random.sample(teams, k=random.randint(1, 2)):
                UserGroup.objects.create(user=u, group=t)
        self.stdout.write(self.style.SUCCESS("Связаны пользователи и группы"))

        # User <-> Role links
        for u in users:
            for r in random.sample(roles, k=random.randint(1, 2)):
                dept = random.choice(departments) if random.choice([True, False]) else None
                UserRole.objects.create(user=u, role=r, department=dept)
        self.stdout.write(self.style.SUCCESS("Связаны пользователи и роли"))

        self.stdout.write(self.style.SUCCESS("=== Генерация тестовых данных завершена! ==="))
