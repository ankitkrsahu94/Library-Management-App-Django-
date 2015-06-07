from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
# Create your models here.

BOOK_TYPES = (
	('A','Adventure'),
	('R','Romance'),
	('F','Fiction'),
	('E','Educational'),
)
MEMBERSHIP_TYPES = (
	('U','User'),
	('A','Admin'),
)
STATUS_OPTION = (
	('RP','Return Pending'),
	('BR','Book Returned'),
	('NA','Not Approved'),
)
class Book(models.Model):
	isbn = models.CharField(max_length=100)
	title = models.CharField(max_length=50)
	pub_date = models.DateField(default=timezone.now)
	author = models.CharField(max_length=30)
	category = models.CharField(max_length=1,choices=BOOK_TYPES)
	quantity = models.BigIntegerField(default=0)
	available = models.BigIntegerField(default=True)
	test = models.BooleanField(default=True)

	class Meta:
		ordering = ["-title"]
		
	def __unicode__(self):
		return self.title

class Member(models.Model):
	user = models.OneToOneField(User)
	dob = models.DateField(default=timezone.now)
	contactNo = models.CharField(max_length=15)
	member_since = models.DateField(default=timezone.now)
	membership_type = models.CharField(max_length=1,default='U',choices=MEMBERSHIP_TYPES)
	hasBooks = models.BigIntegerField(default=0)
	request = models.BigIntegerField(default=0)
	verified = models.BooleanField(default=False)
	
	def is_eligible_for_book(self):
		return (self.hasBooks + self.request) <= 5

	def __unicode__(self):
		return self.user.username
		#return ["No","Yes"][self.verified]


class Books_Issued(models.Model):
	user_id = models.ForeignKey(Member)
	isbn = models.ForeignKey(Book)
	issue_date = models.DateField(default = timezone.now)
	due_date = models.DateField(default = datetime.datetime.now() + datetime.timedelta(days=30))
	fine = models.BigIntegerField(default=0)
	issued = models.BooleanField(default=False)
	status = models.CharField(max_length=2,default='NA',choices=STATUS_OPTION)

	def __unicode__(self):
		return 'success'

