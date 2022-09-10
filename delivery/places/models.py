from django.db import models
from django.shortcuts import reverse
from catalog.models import Product


class Organization(models.Model):
	slug		= models.SlugField(max_length=60, db_index=True, unique=True)
	name 		= models.CharField(max_length=60)

	location	= models.TextField()
	products	= models.ManyToManyField(Product)

	class Meta:
		ordering = ('name', )

	def fix_slug(self):
		for i in [":", "/", "?", "#", "[", "]", "@", "!", "$", "&", "'", "(", ")", "*", "+", ",", ";", "=", " "]:
			self.slug.replace(i, '')

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		self.fix_slug()

		super().save(*args, **kwargs)

	def __str__(self):
		return f'{self.name}: {self.location}'
	
	def get_absolute_url(self):
		return reverse("places:place_detail", kwargs={"slug": self.slug})
