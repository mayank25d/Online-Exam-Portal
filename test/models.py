from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class DifficultyLevel(models.Model):
    difficulty = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.difficulty


class Quarter(models.Model):
    quarter = models.CharField(max_length=100)
    difficulty = models.ForeignKey(DifficultyLevel, related_name="quarter_difficulty", on_delete=models.SET_NULL,
                                   null=True)

    def __str__(self):
        return self.quarter


class Package(models.Model):
    package = models.CharField(max_length=50)

    def __str__(self):
        return self.package


class Subjects(models.Model):
    standard = models.ForeignKey('super_admin.Standard', related_name='sub_standard', on_delete=models.SET_NULL,
                                 null=True)
    atl = models.BooleanField(default=False)
    package = models.ForeignKey(Package, related_name="sub_package", on_delete=models.SET_NULL, null=True)
    sub_name = models.CharField(max_length=40)

    def __str__(self):
        return self.sub_name


class TestLanguage(models.Model):
    test_lang = models.CharField(max_length=50)

    def __str__(self):
        return self.test_lang


class TestTopic(models.Model):
    standard = models.ForeignKey('super_admin.Standard', related_name="topic_standard", on_delete=models.SET_NULL,
                                 null=True)
    package = models.ForeignKey(Package, related_name="topic_package", max_length=50, on_delete=models.SET_NULL,
                                null=True)
    sub_name = models.ForeignKey(Subjects, related_name="topic_subject", max_length=90, on_delete=models.SET_NULL,
                                 null=True)
    topic_name = models.CharField(max_length=50)

    def __str__(self):
        return self.topic_name


class Test(models.Model):
    affiliation = models.ForeignKey('super_admin.AffiliationType', related_name="test_affiliation",
                                    on_delete=models.SET_NULL, null=True)
    quarter = models.ForeignKey(Quarter, related_name="test_quarter", max_length=50, on_delete=models.SET_NULL,
                                null=True, blank=True)
    package = models.ForeignKey(Package, related_name="test_package", max_length=50, on_delete=models.SET_NULL,
                                null=True, blank=True)
    sub_name = models.ForeignKey(Subjects, related_name="test_subject", max_length=90, on_delete=models.SET_NULL,
                                 null=True)
    test_duration = models.PositiveIntegerField(null=True)
    test_lang = models.ForeignKey(TestLanguage, related_name="test_language", null=True, on_delete=models.SET_NULL)
    standard = models.ForeignKey('super_admin.Standard', related_name="test_standard", on_delete=models.SET_NULL,
                                 null=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='test_created_by', on_delete=models.SET_NULL,
                                   null=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='test_updated_by',
                                   null=True)

    def __str__(self):
        return "{} {}, package {}, {} created on {}".format(self.affiliation, self.quarter, self.package,
                                                                  self.sub_name, self.created_at.date())


class Question(models.Model):
    standard = models.ForeignKey('super_admin.Standard', related_name="que_standard",
                                 on_delete=models.SET_NULL, null=True)
    package = models.ForeignKey(Package, related_name="que_package", max_length=50, on_delete=models.SET_NULL,
                                null=True)
    sub_name = models.ForeignKey(Subjects, related_name="que_subject", max_length=90, on_delete=models.SET_NULL,
                                 null=True)
    topic = models.ForeignKey(TestTopic, related_name="que_topic", on_delete=models.SET_NULL, null=True)
    # test = models.ForeignKey(Test, related_name="questions_for_test", on_delete=models.CASCADE, null=True)
    question_type = (
        ('Single Correct', 'Single'),
        ('Multiple Correct', 'Multiple'),
        ('Passage Based', 'Passage')
    )

    language = models.ForeignKey(TestLanguage, related_name="question_lang", on_delete=models.SET_NULL, null=True)
    question = models.TextField(default='')
    question_tags = models.CharField(max_length=60, choices=question_type, default="Single")
    level = models.ForeignKey(DifficultyLevel, null=True, related_name="question_difficulty", on_delete=models.SET_NULL)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name="ques_created_by", on_delete=models.SET_NULL, null=True)
    updated_by = models.ForeignKey(User, related_name="ques_updated_by", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.question


class Options(models.Model):
    question_id = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE, null=True)
    option = models.CharField(max_length=1000, null=True, blank=True)
    is_valid = models.BooleanField(default=True, null=True)


class QuestionHistory(models.Model):
    test = models.ForeignKey(Test, on_delete=models.SET_NULL, null=True, related_name="test_history")
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, related_name="que_history")
    value = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=5)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_by_history')
    created_at = models.DateTimeField(null=True, auto_now_add=True)


class MarkSheet(models.Model):
    student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='test_by')
    test = models.ForeignKey(Test, on_delete=models.SET_NULL, null=True, related_name="test_id")
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, related_name="ques_in_test")
    marks = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)


class AnswerSheet(models.Model):
    marks_sheet = models.ForeignKey(MarkSheet, on_delete=models.SET_NULL, null=True, related_name='my_answersheet')
    ques_id = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, related_name="answer_of_ques")
    my_answer = models.TextField(null=True, blank=True)
    select_opt = models.ForeignKey(Options, on_delete=models.SET_NULL, null=True, related_name='selected_opt')


class ReportCard(models.Model):
    student = models.ForeignKey('super_admin.Student', on_delete=models.SET_NULL, null=True,
                                related_name='test_given_by')
    test = models.ForeignKey(Test, on_delete=models.SET_NULL, null=True, related_name="test_my_id")
    sub = models.ForeignKey(Subjects, on_delete=models.SET_NULL, null=True, related_name="test_sub_id")
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True, related_name="test_package_id")
    quarter = models.ForeignKey(Quarter, on_delete=models.SET_NULL, null=True, related_name="test_quarter_id")
    score = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    checked_by = models.ForeignKey('super_admin.Teacher', on_delete=models.SET_NULL, null=True,
                                   related_name='checked_by')
    checked_on = models.DateTimeField(null=True, auto_now_add=True)
