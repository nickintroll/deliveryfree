from django.contrib.postgres.search import SearchVector
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

from jobs.tools import is_ajax

from .forms import LoginForm, RegisterForm, UpdateProfileForm, EmployeeSearchForm
from .models import Profile, Chat, Message


def register_page(request):
	form = RegisterForm()
	notification = None

	if request.method == 'POST':
		form = RegisterForm(request.POST)

		if form.is_valid():
			new_user = form.save(commit=False)

			try:
				_password = form.clean_password()
			except ValidationError:
				return render(request, 'users/register.html', 
					{
						'form': form, 
						'note': "Password don't matching"
					})

			new_user.set_password(_password)

			new_user.save()
			Profile(user=new_user).save()

			login(request, new_user)
			return redirect('users:profile')

	if form.errors:
		errors = form.errors.as_data()
		notification = errors[list(errors.keys())[0]][0].message # just gets first error
		
		form.errors.clear()

	return render(request, 'users/register.html', {'form': form, 'note': notification})


def login_page(request):
	form = LoginForm()
	notification = None

	if request.method == "POST":
		form = LoginForm(request.POST)

		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(
				request, 
				username=cd['username'], 
				password=cd['password'])

			if user:
				if user.is_active:
					login(request, user)
					return redirect('users:profile')
				else:
					notification = 'Disabled account. Register new or use feed back page to contact the managers.'

			else:
				notification = 'Invalid login, try again.'
		else:
			notification = 'Wrong request, check data and try again.'

	return render(request, 'users/login.html', {'form': form, 'note': notification})


def profile_page(request, slug=None):
	controll = False
	
	if request.user.is_authenticated:
		user = request.user.profile
	else:
		user = None

	if slug:
		user = get_object_or_404(Profile, slug=slug)
	
	if request.user.is_authenticated:	
		if user == request.user.profile:
			controll = True

	return render(request, 'profile/profile.html', {'controll': controll, 'user': user})


@login_required
def update_profile(request):
	form = UpdateProfileForm(instance = request.user.profile)

	if request.method == 'POST':
		print(request.FILES)
		print(request.POST)
		form = UpdateProfileForm(data=request.POST, files=request.FILES, instance=request.user.profile)
		if form.is_valid():
			form.save()
			return redirect('users:profile')

	return render(request, 'profile/update_profile.html', {'form': form})


def users_list(request):
	form = EmployeeSearchForm()

	is_search = False
	search_request = ''

	# seach logic
	if 'search' in request.GET.keys():
		form = EmployeeSearchForm(request.GET)
		if form.is_valid():
			is_search = True
			query = form.cleaned_data
			users = Profile.objects.annotate(
				search=SearchVector('description', 'user__username', 'imlookingfor', 'education'),
			).filter(search__contains=query['search'])
			search_request += query['search'] + ', '

	else:
		users = Profile.objects.all()

	if 'age_from' in request.GET.keys():
		if request.GET['age_from'] != '':
			is_search = True
			users.filter(age__gte=request.GET['age_from'])
			search_request += 'age > ' + request.GET['age_from'] + ', '
	
	if 'age_to' in request.GET.keys():
		if request.GET['age_to'] != '':
			is_search = True
			users.filter(age__lte=request.GET['age_to'])
			search_request += 'age < ' + request.GET['age_to']

	# paginator logic
	# users = Profile.objects.all()
	total_users = users.count()
	paginator = Paginator(users, 10)
	page = request.GET.get('page')

	try:
		users = paginator.page(page)
	except EmptyPage:
		if is_ajax(request):
			return HttpResponse('')
		users = paginator.page(paginator.num_pages)

	except PageNotAnInteger:
		users = paginator.page(1)

	if is_ajax(request):
		return render(request, 'users/users_ajax_list.html', {'users': users, 'form_': form, 'total_users': total_users})

	return render(request, 'users/list_view.html', {'users': users, 'form_': form, 'total_users': total_users, 'is_search': is_search, 'search_request': search_request})


@login_required()
def chat_room_enter(request, usr1):
	other = Profile.objects.get(slug=usr1)	# add 404 here
	chat = Chat.get_chat(user_one=other, user_two=request.user.profile)
	return redirect('users:chat_room', chat=chat.slug)


@login_required()
def chat_room(request, chat):
	chat = get_object_or_404(Chat, slug=chat)
	other = chat.get_oposite_user(request)

	for i in chat.messages.all().filter(creator=other, is_read=False):
		print(i)
		i.is_read=True
		i.save()

	return render(request, 'chat/room.html', {'chat': chat, 'other': other})
