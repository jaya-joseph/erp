from django.db import models
from django.contrib.auth.models import User


class Login(models.Model):
    class Meta:
        db_table = "login"

    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('faculty', 'Faculty'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    usertype = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, null=False)

    def __str__(self):
        return f'{self.user.username}'


class Department(models.Model):
    class Meta:
        db_table = 'department'

    dept_name = models.CharField(max_length=100, blank=False, null=False)
    hod = models.ForeignKey('FacultyDetails', null=True, on_delete=models.DO_NOTHING, related_name='hod_faculty')


class FacultyDetails(models.Model):
    class Meta:
        db_table = 'faculty_details'

    name = models.TextField()
    department = models.ForeignKey('Department',
                                   null=True,
                                   on_delete=models.DO_NOTHING,
                                   related_name='faculty_department')
    phone_no = models.TextField()
    email = models.TextField()
    photo = models.TextField()


class FacultyDesignation(models.Model):
    class Meta:
        db_table = 'faculty_designation'

    DESIGNATION_CHOICES = (
        ('hod', 'Head of the Department'),
        ('fclty', 'Faculty'),
        ('prncpl', 'Principal'),
        ('pgdean', 'PG Dean'),
        ('ugdean', 'UG Dean'),
        ('sadean', 'Student Affairs Dean'),
        ('stfadv', 'Staff Advisor'),
    )

    faculty = models.ForeignKey('FacultyDetails', on_delete=models.DO_NOTHING, related_name='faculty_id')
    designation = models.CharField(max_length=100,
                                   choices=DESIGNATION_CHOICES,
                                   default='faculty',
                                   blank=False,
                                   null=False)


class AcademicYear(models.Model):
    class Meta:
        db_table = 'academic_year'

    acd_year = models.TextField()
    status = models.SmallIntegerField()
