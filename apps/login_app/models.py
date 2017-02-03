from __future__ import unicode_literals
from django.core.validators import validate_email
from django.contrib import messages
from django.db import models
import bcrypt

# # Create your models here.

class UserManager(models.Manager):
	def register(self, first_name, last_name, email, password, password2, dob):
		try:
			validate_email(email)
		except Exception as e:
			print e
			return False
		if len(password)<8:
			raise NameError('Password no fewer than 8 characters in length')
			return False
		if password != password2:
			raise NameError('Password must match')
		if len(first_name)<2:
			raise NameError('First name has to be at least 2 characters')
			return False
		if not first_name.isalpha():
			raise NameError('First name has to be letters only')
			return False
		if len(last_name)<2:
			raise NameError('Last name has to be at least 2 characters')
			return False
		if not last_name.isalpha():
			raise NameError('Last name has to be letters only')
			return False
		try:
			hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
			newUser= self.create(first_name=first_name, last_name=last_name, email=email, password=hashed, date_of_birth=dob)
			newUser.save()
			return True
		except Exception as e:
			print e
			return False

		
	def login(self, email, password):
		# first check if user exits
		user = User.objects.filter(email=email)
		print user[0].id

		# also match the password
		userPassword = user[0].password.encode()
		if bcrypt.hashpw(password.encode(), userPassword) == userPassword:
			userInfo = {
			'first_name': user[0].first_name,
			'user_id': user[0].id,
			'login': True
			}
			return userInfo
		else:
			return False



class User(models.Model):
	first_name =models.CharField(max_length=45)
	last_name=models.CharField(max_length=45)
	email=models.CharField(max_length=100)
	password=models.CharField(max_length=100)
	date_of_birth=models.DateField(null=True, blank=True)
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now=True)
	objects=UserManager()


class Quote(models.Model):
	quoted_by = models.CharField(max_length=255)
	message = models.TextField(max_length=10000)
	submit_by = models.ForeignKey(User)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Favorite(models.Model):
	quote_id = models.ForeignKey(Quote)
	user_id = models.ForeignKey(User)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)






























