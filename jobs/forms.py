from django import forms

from .models import Job, Comment, JobAnswer


class JobForm(forms.ModelForm):
	salary = forms.IntegerField(label='Salary', widget=forms.NumberInput(attrs={'placeholder': 'Payment'}))

	class Meta:
		model = Job
		fields = ['job_title','location','description','salary','type', 'status']
		widgets = {
			'job_title': forms.TextInput(attrs={'placeholder': 'Job title'}),
		}


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['comment', 'answer_to']
		widgets = {
			'comment': forms.Textarea(attrs={'placeholder': 'Your comment'}),
		}


class JobsSearchForm(forms.Form):
	search = forms.CharField(required=False, label='', max_length=300, widget=forms.TextInput(attrs={'placeholder': 'search'}))
	salary_from = forms.IntegerField(required=False, label='', widget=forms.NumberInput(attrs={'placeholder': 'payment from'}))
	salary_to = forms.IntegerField(required=False, label='', widget=forms.NumberInput(attrs={'placeholder': 'payment from'}))


class JobAnswerForm(forms.ModelForm):
	class Meta:
		model = JobAnswer
		fields = ['description', ]
		widgets = {
			'description': forms.Textarea(attrs={'placeholder': 'Your message to creator of this job. Make sure to provide reason why employer should pick you.'})
		}
