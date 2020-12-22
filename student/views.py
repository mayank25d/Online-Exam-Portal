from django.shortcuts import render, redirect
from super_admin.models import AssignTest, Student
from django.contrib.auth.decorators import login_required
from tests.models import Test, QuestionHistory, Question, Options, MarkSheet, AnswerSheet
import datetime
from datetime import timedelta, date
from .forms import *
from django.http import HttpResponse


# Create your views here.
@login_required
def student_home_view(request):
    return redirect("test_history")

def student_dashboard_view(request):
    return render(request, 'student/dashboard.html')


def test_history_view(request):
    current_date_time = datetime.datetime.now().replace(microsecond=0)
    test_paper = []

    # fetch all cancelled tests
    assigned_test = AssignTest.objects.filter(student__user=request.user)
    print(assigned_test)

    for at in assigned_test:
        if at.test_status == 'cancel':
            test_cancel = Test.objects.get(id=at.test_paper.id)
            test_paper.append(test_cancel)
        else:
            test_alive = Test.objects.get(id=at.test_paper.id)
            print(test_alive)

            # for test in test_alive:
            # get test_date
            test_date = at.test_date
            print(test_date)

            # get date-time type
            print(test_date, type(test_date))
            print(current_date_time, type(current_date_time))

            test_duration = test_alive.test_duration
            test_end_time = test_date + timedelta(days=0, minutes=int(test_duration))

            print(test_date < current_date_time)
            print(current_date_time < test_end_time)

            # if test has begun
            if test_date <= current_date_time < test_end_time:
                remaining_minutes = (test_end_time - current_date_time).seconds / 60
                print(test_duration - remaining_minutes)

                #if 15 mins have passed
                if test_duration - remaining_minutes >= 15 and \
                        remaining_minutes <= test_duration:
                    assigned = AssignTest.objects.get(id=at.id)
                    assigned.test_status = 'cancel'
                    assigned.save()
                    print('You were late')

                    test_paper.append(test_alive)
            if current_date_time > test_end_time:
                assigned = AssignTest.objects.get(id=at.id)
                assigned.test_status = 'cancel'
                assigned.save()

    return render(request, 'student/test_history.html', {'test_paper': test_paper})


@login_required
def start_test_view(request, id):
    data = {}
    test = Test.objects.filter(id=id).get()
    # list of all questions in the test, filtered by test id
    questions = QuestionHistory.objects.filter(test_id=id)

    if request.method == 'POST':
        for q in questions:
            # radio option id, marked by the user
            if q.question.question_tags == "Single Correct":
                marksheet = MarkSheet.objects.create(student=request.user, test=test,
                                                     question=Question.objects.get(id=q.question_id))
                radio_but = request.POST.get(str(q.question_id))
                if radio_but != None:
                    print(Options.objects.get(id=radio_but).option)
                    my_answer_radio = AnswerSheet(my_answer=Options.objects.get(id=radio_but).option,
                                                  marks_sheet=marksheet,
                                                  ques_id=Question.objects.get(id=q.question_id))
                    my_answer_radio.save()
            elif q.question.question_tags == "Multiple Correct":
                marksheet = MarkSheet.objects.create(student=request.user, test=test,
                                                     question=Question.objects.get(id=q.question_id))

                # list of all options in radio button
                options = Options.objects.filter(question_id=q.question_id)

                for opt in options:
                    # option's values which are marked by the students
                    option_val = request.POST.get(str(opt.id))
                    if option_val != None:
                        print(Options.objects.get(id=option_val).option)
                        my_answer_checkbox = AnswerSheet(my_answer=Options.objects.get(id=option_val).option,
                                                         marks_sheet=marksheet,
                                                         ques_id=Question.objects.get(id=q.question_id))
                        my_answer_checkbox.save()
            else:
                marksheet = MarkSheet.objects.create(student=request.user, test=test,
                                                     question=Question.objects.get(id=q.question_id))

                options = Options.objects.filter(question_id=q.question_id)
                for opt in options:
                    passage_val = request.POST.get(str(opt.id))
                    if passage_val != None:
                        my_answer_passage = AnswerSheet.objects.create(my_answer=passage_val,
                                                                       marks_sheet=marksheet,
                                                                       ques_id=Question.objects.get(id=q.question_id))
                        my_answer_passage.save()
        return redirect('test_history')
    else:
        for q in questions:
            options = Options.objects.filter(question_id=q.question_id)
            data[q] = options

        return render(request, 'student/start_test.html', {'id': id, 'test': test, 'data': data, 'question': questions})


@login_required
def upcoming_test_view(request):
    test_paper = []
    print(request.user)
    student = Student.objects.get(user=request.user)
    print(student)
    upcoming_test = AssignTest.objects.filter(student=student, test_status='pending')

    for ut in upcoming_test:
        test_paper.append(Test.objects.get(id=ut.test_paper_id))

    print(upcoming_test, upcoming_test.count(), test_paper)

    return render(request, 'student/upcoming_test.html', {'upcoming': upcoming_test, 'count': upcoming_test.count(),
                                                          'test_paper': test_paper})


@login_required
def cancel_test_view(request, id):
    test = AssignTest.objects.get(id=id)
    test.test_status = 'cancel'
    test.save()
    return redirect('upcoming_test')
