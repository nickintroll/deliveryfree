from django.db import models

class Product(models.Model):
	slug		= models.SlugField(max_length=60, db_index=True, unique=True)
	title 		= models.CharField(max_length=60)

	price		= models.DecimalField(max_digits=10, decimal_places=2)
	description	= models.TextField
	recipe		= models.TextField
	weight		= models.TextField

	created		= models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('created', 'title')

	def check_slug(self):
		for i in [":", "/", "?", "#", "[", "]", "@", "!", "$", "&", "'", "(", ")", "*", "+", ",", ";", "=", " "]:
			self.slug.replace(i, '')

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		self.check_slug()

		super().save(*args, **kwargs)

	def __str__(self):
		return f'{self.title}: {self.price}'
	

# 	def get_absolute_url(self):
# 		retur  reverse("shop:product_detail", kwargs={"slug": self.slug})
