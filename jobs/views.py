from django.contrib.postgres.search import SearchVector
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

from users.models import Profile

from .models import Job, Requirements
from .forms import JobForm, CommentForm, JobsSearchForm, JobAnswerForm
from .tools import get_comment_to_answer_order, is_ajax, conbine_search_res


def jobs_search_main_page(request):
	employees = Profile.objects.all()[:8]

	is_search = False

	form = JobsSearchForm()

	if ''.join(request.GET.keys()).replace('page', '') != '':
		form = JobsSearchForm(request.GET)

		if form.is_valid():
			is_search = True
			query = form.cleaned_data

			jobs = conbine_search_res(
				Job.objects.annotate(
					search=SearchVector('job_title', 'description', 'location', 'requirements')
				).filter(search=query['search']),
				Job.objects.annotate(
					search=SearchVector('job_title', 'description', 'location', 'requirements')
				).filter(search__contains=query['search'])
			)

			if query['salary_from']:
				jobs = jobs.filter(salary__mt=query['salary_from'])
			if query['salary_to']:
				jobs = jobs.filter(salary__lt=query['salary_to'])



	if not is_search:
		jobs = Job.objects.all().filter(status='Publish')

	jobs_total = Job.objects.all().count()
	paginator = Paginator(jobs, 5)
	page = request.GET.get('page')	

	try: 
		jobs = paginator.page(page)

	except EmptyPage:
		if is_ajax(request):
			return HttpResponse('')
		jobs = paginator.page(paginator.num_pages)

	except PageNotAnInteger:
		jobs = paginator.page(1)

	if is_ajax(request):
		print(request.GET)
		return render(request, 'jobs_list_ajax.html', {'jobs': jobs})

	# return render(request, 'main_page.html', {"jobs": jobs, 'employees': employees, 'form': form})
	return render(request, 'main_page.html', {"jobs": jobs, 'employees': employees, 'jobs_total': jobs_total, 'form': form, 'is_search': is_search})


@login_required
def creating_job(request):
	reqs = Requirements.objects.all()

	form = JobForm()
	
	notification = ''

	if request.method == 'POST':
		form = JobForm(request.POST)
		if form.is_valid():
			job = form.save(commit=False)
			job.owner = request.user.profile
			job.save()
			
			if 'reqs' in ''.join(request.POST.keys()):
				for key in request.POST.keys():
					if 'reqs' in key:
						req = request.POST[key]
						if Requirements.objects.filter(id=req).exists():
							job.requirements.add(
								Requirements.objects.get(id=req)
							)

			job.save()
			return redirect('users:profile')
	
	if form.errors:
		errors = form.errors.as_data()
		
		errors[list(errors.keys())[0]][0].message

		notification = list(errors.keys())[0] + ': '+ errors[list(errors.keys())[0]][0].message
		
		form.errors.clear()

	return render(request, 'jobs/new_job_form.html', {'form': form, 'reqs': reqs, 'notification': notification})


def detail(request, slug):
	job = get_object_or_404(Job, slug=slug)
	controll = False

	more_from_this_dev = job.owner.jobs.all()[:6]

	users_answer = None

	if request.user.is_authenticated:
		if request.user.profile == job.owner:
			controll = True

		users_answer = job.answers.filter(creator=request.user.profile)
		if len(users_answer) != 0:
			users_answer = users_answer[0]

	commentForm = CommentForm()
	print(users_answer)
	if users_answer:
		answerform = JobAnswerForm(instance=users_answer)
	else:
		answerform = JobAnswerForm()
	

	if request.method == 'POST':
		if request.user.is_authenticated:
			commentf = CommentForm(request.POST)
			if users_answer:
				answerf = JobAnswerForm(request.POST, instance=users_answer)
			else:
				answerf = JobAnswerForm(request.POST)
			if 'description' in request.POST:
				# working with jobanswer
				if answerf.is_valid():
					job_answer = answerf.save(commit=False)
					job_answer.job = job
					job_answer.creator = request.user.profile

					job_answer.save()

				return redirect('jobs:detail', job.slug)

			else:
				# comment logic
				if commentf.is_valid():
					comment = commentf.save(commit=False)

					comment.creator = request.user.profile
					comment.job = job

					if comment.answer_to:
						comment.is_answer = True

					comment.save()

					return redirect('jobs:detail', job.slug)
		else:
			return redirect('users:login')


	comments = get_comment_to_answer_order(job.comments.all())
	
	return render(
		request, 
		'jobs/detail.html', 
		{
			'job': job, 
			'controll': controll, 
			'commentForm': commentForm, 
			'comments': comments, 
			'more_from_this_dev': more_from_this_dev,
			'answerform': answerform,
			'users_answer': users_answer
		}
	)


@login_required
def edit(request, slug):
	reqs = Requirements.objects.all()

	job = Job.objects.get(slug=slug)
	if request.user.profile != job.owner:
		return redirect('jobs:main')

	form = JobForm(instance=job)
	if request.method == 'POST':
		form = JobForm(instance=job, data=request.POST)
		job = form.save(commit=False)

		if 'reqs' in ''.join(request.POST.keys()):
			for key in request.POST.keys():
				if 'reqs' in key:
					req = request.POST[key]
					if Requirements.objects.filter(id=req).exists():
						job.requirements.add(
							Requirements.objects.get(id=req)
						)

		job.save()

	return render(request, 'jobs/edit.html', {'job': job, 'form': form, 'reqs': reqs})
