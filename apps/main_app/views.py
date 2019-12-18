from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt


def index(request):
    return render(request, 'main_app/index.html')


def register(request):
    if request.method == 'POST':
        errors = User.objects.user_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            hashed_password = bcrypt.hashpw(
                request.POST['password'].encode(), bcrypt.gensalt())
            new_user = User.objects.create(
                first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hashed_password)
            request.session['user_id'] = new_user.id
            return redirect('/users/success')
    return redirect('/')


def login(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(email=request.POST['email'])
        except:
            messages.error(request, 'Invalid username or password')
            return redirect('/')
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['first_name'] = user.first_name
            request.session['user_id'] = user.id
            return redirect('/users/success')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('/')
    return redirect('/')


def success(request):
    if not check_login(request):
        return redirect('/')
    all_jobs = Job.objects.all()
    context = {
    "all_jobs_tb": all_jobs
    }
    return render(request, 'main_app/success.html', context)


def logout(request):
    del request.session['user_id']
    del request.session['first_name']
    return redirect('/')


def check_login(request):
    if not 'first_name' in request.session:
        messages.error(request, 'Log in to view this page')
        return False
    return True


# Belt Exam


def new_job(request):
    return render(request, 'main_app/newjob.html')


def create_job(request):
    if request.method == 'POST':
        errors = Job.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/users/jobs/new')
        else:
          new_job = Job.objects.create(
          title = request.POST['title'],
          desc = request.POST['desc'],
          location = request.POST['location'], user = User.objects.get(first_name = request.session['first_name']))
          new_job_id = new_job.id
          return redirect ("/users/success")

def display_job(request, job_id):
  new_job = Job.objects.get(id = job_id)
  created = new_job.created_at.strftime('%d %B, %Y')
  context = {
    "created_date_view": created,
    "job_view": new_job,
  }
  return render(request, "main_app/viewjob.html", context)

def delete(request, job_id):
  job = Job.objects.get(id = job_id)
  job.delete()
  return redirect ("/users/success")

def edit(request, job_id):
  job = Job.objects.get(id = job_id)
  context = {
    "job_view": job
  }
  return render(request, "main_app/editjob.html", context)

def update(request, job_id):
  if request.method == 'POST':
    errors = Job.objects.basic_validator(request.POST)
    if len(errors) > 0:
      for key, value in errors.items():
        messages.error(request, value)
      return redirect(f"/users/jobs/edit/{job_id}")
    else:
      job = Job.objects.get(id = job_id)
      job.title = request.POST['title']
      job.desc = request.POST['desc']
      job.location = request.POST['location']
      job.save()
    return redirect ("/users/success")