from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Exam, Exam_Details, Mcqs, Questions
from classroom.models import Classroom
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
import csv
# Create your views here.

def view_exams(request):
    if request.method == 'GET':
        exams = Exam.objects.all()
        return render(request, 'teacher_exam.html', {'exams':exams})
    else:
        pass

def delete_exam(request, exam_id = 0):
    Exam.objects.filter(id = exam_id).delete()
    messages.info(request, 'Exam record deleted!')
    return redirect('exams')

def view_exam(request, exam_id = 0):
    exam = Exam.objects.filter(id = exam_id)
    context=[]
    with open('auto-grade.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            context.append(row) 
    del context[0]
    return render(request, 'teacher_exam_view.html', {'exam':exam,'results':context})

def create_exam(request):
    if request.method == 'POST':
        exam_name = request.POST['examName']
        class_id = request.POST['classId']
        start_time = request.POST['startTime']
        end_time = request.POST['endTime']
        class_name = Classroom.objects.filter(id = class_id).values_list('cls_name', flat=True)[0]
        print(class_name)
        exam = Exam_Details( exam_name = exam_name,
                            class_id = class_id,
                            start_time = start_time,
                            end_time = end_time)
        exam.save()
        current_exam_id = exam.id

        questions = request.POST.getlist('questions[]')
        correct_answers = request.POST.getlist('correctAnswers[]')
        questions_marks = request.POST.getlist('questionsMarks[]')
        questions_type = request.POST.getlist('questionsType[]')
        

        q_option = "optionsQ"
        q_type = "mcqs"
        for index, question in enumerate(questions):
            q_type = q_type + str(index+1)
            q_option = q_option + str(index+1) + '[]'
            
            print('\nQuestion No:',index+1,'\t Question:', question, '\t Marks:', questions_marks[index], '\n')
            print("Custom type created: ",q_type)
            print("Actual Question type:", questions_type[index])

            quest = Questions( exam_id = current_exam_id,
                            question = question,
                            correct_ans =  correct_answers[index],
                            question_marks = questions_marks[index],
                            std_id = None, 
                            std_answer = None)
            quest.save()
            if questions_type[index] == q_type:
                print("CURRENT QUESTION ID:",quest.id)
                quest.question_type = 'mcq'
                question_options = request.POST.getlist(q_option)
                for index2, option_value in enumerate(question_options):
                    print(index2+1, ': ', option_value)
                    mcqs_options = Mcqs(question_id = quest.id,
                                        option = option_value)
                    mcqs_options.save()
            else:
                quest.question_type = 'descriptive'
                print('Its a descriptive question')
            
            quest.save()
            q_type = 'mcqs'
            q_option = 'optionsQ'
            print('\n')

        exam_created = Exam( cls_name = class_name,
                            total_std = 3,
                            total_attempts = 0,
                            exam_created = start_time)
        exam_created.save()

        # Returning results
        messages.info(request, 'Exam has been created!.')
        return redirect('exams')
    
    else:
        classes = Classroom.objects.filter(teacher_id = request.user.id)
        return render(request, 'teacher_schedule_exam.html', {'cls': classes})