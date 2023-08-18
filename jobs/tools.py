def unpack_comments_answers(comment):
	answers = comment.answers.all()
	res = [comment, ]

	if len(answers) == 0:
		return res
	else:
		for i in answers:
			res += unpack_comments_answers(i)
		return res


def get_comment_to_answer_order(comments):
	res = []

	for com in comments:
		if not com in res:
			res += unpack_comments_answers(com)

	return res


def is_ajax(request):
	return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def conbine_search_res(res1, res2):
	res = res1.filter(status='Publish').union(res2.filter(status='Publish'))
	if res.count() == 0:
		return []
	return res[0].__class__.objects.all().filter(pk__in=[i.pk for i in res])

