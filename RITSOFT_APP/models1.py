from django.db import models


class Course(models.Model):
    class Meta:
        db_table = 'course'

    course_code = models.CharField(max_length=5)
    course_name = models.CharField(max_length=20)
    category = models.CharField(max_length=20)
    no_of_semesters = models.IntegerField()


class ClassDetails(models.Model):
    class Meta:
        db_table = 'class_details'

    class_id = models.CharField(max_length=50)
    course = models.ForeignKey('Course', on_delete=models.DO_NOTHING, related_name='class_course')
    sem_id = models.IntegerField()
    branch_or_specialisation = models.CharField(max_length=100)
    department = models.ForeignKey('Department',
                                   null=True,
                                   on_delete=models.DO_NOTHING,
                                   related_name='class_department')
    active = models.TextField()


class SubjectDetails(models.Model):
    class Meta:
        db_table = 'subject_details'
        unique_together = (('subject_code', 'class_id'),)

    subject_code = models.CharField(max_length=50)
    subject_title = models.TextField()
    class_id = models.OneToOneField('ClassDetails',
                                    on_delete=models.DO_NOTHING,
                                    db_column='class_id',
                                    related_name='subject_class')
    type = models.CharField(max_length=30)
    internal_passmark = models.IntegerField()
    internal_mark = models.IntegerField()
    external_pass_mark = models.IntegerField()
    external_mark = models.IntegerField()


class SubjectAllocation(models.Model):
    class Meta:
        db_table = 'subject_allocation'
        unique_together = (('subject', 'faculty', 'type'),)

    subject = models.ForeignKey('SubjectDetails', on_delete=models.DO_NOTHING)
    faculty = models.ForeignKey('FacultyDetails', on_delete=models.DO_NOTHING)
    type = models.CharField(max_length=50)


class SubjectAllocationOld(models.Model):
    class Meta:
        db_table = 'subject_allocation_old'
        unique_together = (('subject', 'faculty', 'type', 'acd_year'),)

    subject = models.ForeignKey('SubjectDetails', on_delete=models.DO_NOTHING)
    faculty = models.ForeignKey('FacultyDetails', on_delete=models.DO_NOTHING)
    type = models.CharField(max_length=50)
    acd_year = models.ForeignKey('AcademicYear', on_delete=models.DO_NOTHING)


class LabBatch(models.Model):
    class Meta:
        db_table = 'lab_batch'

    batch_name = models.CharField(max_length=50)
    subject = models.ForeignKey('SubjectDetails', on_delete=models.DO_NOTHING)


class LabBatchOld(models.Model):
    class Meta:
        db_table = 'lab_batch_old'

    batch_name = models.CharField(max_length=50)
    subject = models.ForeignKey('SubjectDetails', on_delete=models.DO_NOTHING)
    acd_year = models.ForeignKey('AcademicYear', on_delete=models.DO_NOTHING)


class SessionalStatus(models.Model):
    class Meta:
        db_table = 'sessional_status'

    subject = models.ForeignKey('SubjectDetails', on_delete=models.DO_NOTHING)
    sessional_status = models.CharField(max_length=255)
    verification_status = models.IntegerField()
    sessional_remark = models.TextField(blank=True, null=True)
    sessional_date = models.DateTimeField()


class SessionalStatusOld(models.Model):
    class Meta:
        db_table = 'sessional_status_old'

    subject = models.ForeignKey('SubjectDetails', on_delete=models.DO_NOTHING)
    sessional_status = models.CharField(max_length=255)
    verification_status = models.IntegerField()
    sessional_remark = models.TextField(blank=True, null=True)
    sessional_date = models.DateTimeField()
    acd_year = models.ForeignKey('AcademicYear', on_delete=models.DO_NOTHING)
