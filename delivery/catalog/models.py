from django.db import models
from django.shortcuts import reverse


class Product(models.Model):
	slug		= models.SlugField(max_length=60, db_index=True, unique=True)
	title 		= models.CharField(max_length=60)

	price		= models.DecimalField(max_digits=10, decimal_places=2)
	description	= models.TextField()
	recipe		= models.TextField()
	weight		= models.DecimalField(max_digits=10, decimal_places=2)

	created		= models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('created', 'title')

	def fix_slug(self):
		for i in [":", "/", "?", "#", "[", "]", "@", "!", "$", "&", "'", "(", ")", "*", "+", ",", ";", "=", " "]:
			self.slug.replace(i, '')

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)
		self.fix_slug()

		super().save(*args, **kwargs)

	def __str__(self):
		return f'{self.title}: {self.price}'
	

	def get_absolute_url(self):
		return reverse("catalog:product_detail", kwargs={"slug": self.slug})


class Image(models.Model):
	product = models.ForeignKey(Product, default=None, related_name='images', on_delete=models.CASCADE)
	image = models.ImageField(upload_to='products/%Y%m%d')
