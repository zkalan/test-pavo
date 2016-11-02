# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from django.db import models
from django.utils import timezone
import datetime

from decimal import *

class Catagory(models.Model):
	catagoryId = models.CharField(primary_key = True, max_length = 10)
	name = models.CharField(max_length = 50)

	def __unicode__(self):
		return self.name.encode('utf-8')

class BookLocation(models.Model):
	locationId = models.CharField(primary_key = True, max_length = 30)
	floor = models.CharField(max_length = 2)
	area = models.CharField(max_length = 20)

	def __unicode__(self):
		return ('floor:' + self.floor + ' area:' + self.area).encode('utf-8')


class PublishingHouse(models.Model):
	publisherId = models.CharField(primary_key = True, max_length = 30)
	name = models.CharField(max_length = 200)
	#location = models.CharField(max_length = 30)
	#tel = models.CharField(max_length = 11)

	def __unicode__(self):
		return self.name.encode('utf-8')


#base class Person
class Person(models.Model):

	GENDER = (
		('male', 'male'),
		('female', 'female'),
	)

	account = models.CharField(primary_key = True, max_length = 20)
	password = models.CharField(max_length = 30)
	name = models.CharField(max_length = 200)
	gender = models.CharField(max_length = 6, choices = GENDER)
	tel = models.CharField(max_length = 11)
	photo = models.ImageField(upload_to='photo',null=True,blank=True)
	def __unicode__(self):
		return self.account
	
	class Meta:
		abstract = True



class Admin(Person):
	admin_add_date = models.DateTimeField()
	def publish(self):
		self.admin_add_date = timezone.now()
		self.save()
		
class FrontDeskLibrarian(Person):
	front_add_date = models.DateTimeField()
	def publish(self):
		self.front_add_date = timezone.now()
		self.save()

class StackLibrarian(Person):
	stack_add_date = models.DateTimeField()
	def publish(self):
		self.stack_add_date = timezone.now()
		self.save()


class Member(Person):

	TYPE = (
		('undergraduate', 'undergraduate'),
		('postgraduate', 'postgraduate'),
		('faculty', 'faculty'),
	)

	school = models.CharField(max_length = 30)
	type = models.CharField(max_length = 20, choices = TYPE)

	#Student特有
	major = models.CharField(max_length = 300)
	classNo = models.CharField(max_length = 20)
	#student and teacher both have
	dueDate = models.DateField()
	maxBorrowedBooks = models.PositiveIntegerField(default = 10)
	availableDays = models.PositiveIntegerField(default = 30)
	debt = models.DecimalField(max_digits = 4, decimal_places = 1, default = 000.0)
	bookOwning = models.IntegerField(default = 0)
	member_add_date = models.DateTimeField()

	def publish(self):
		self.member_add_date = timezone.now()
		self.save()

	def __unicode__(self):
		return self.account
	
   	def isAlive(self):
		return (timezone.now().strftime('%Y%m%d%H%M%S') <= self.dueDate.strftime('%Y%m%d%H%M%S'))
	
	def isOverMaxLend(self):
		return (self.bookOwning >= self.maxBorrowedBooks)
	
	def isOverMaxDebt(self):
		return (self.debt >= Decimal('10.0'))


'''
class Student(Member):

	TYPE = (
		('undergraduate', 'undergraduate'),
		('postgraduate', 'postgraduate'),
	)

	studentType = models.CharField(max_length = 20, choices = TYPE)
	major = models.CharField(max_length = 300)
	classNo = models.CharField(max_length = 20)
	registeredDate = models.DateField(default = timezone.now())
	dueDate = models.DateField()
	maxBorrowedBooks = models.IntegerField(default = 10)
	availableDays = models.IntegerField(default = 30)
	student_add_date = models.DateTimeField()

	def publish(self):
		self.student_add_date = timezone.now()
		self.save()

class Faculty(Member):

	maxBorrowedBooks = models.IntegerField(default = 20)
	availableDays = models.IntegerField(default = 60)
	faculty_add_date = models.DateTimeField()

	def publish(self):
		self.faculty_add_date = timezone.now()
		self.save() 
'''
class BookInfo(models.Model):
	ISBN = models.CharField(max_length = 17, primary_key = True)
	title = models.CharField(max_length = 300)
	author = models.CharField(max_length = 200)
	publishingHouse = models.ForeignKey(PublishingHouse)
	catagory = models.ForeignKey(Catagory)
	book_image_URL = models.CharField(max_length=200,null=True,blank=True)
	introducton = models.TextField(null = True, blank = True)

	def __unicode__(self):
		return self.title.encode('utf-8')


class BookOnShelf(models.Model):
	STATE = (
		('in', 'in'),
		('out', 'out'),
	)
	
	bookId = models.CharField(primary_key = True, max_length = 50)
	bookLocation = models.ForeignKey(BookLocation)
	bookInfo = models.ForeignKey(BookInfo)
	state = models.CharField(max_length = 10, choices = STATE, default = 'in')
	book_add_date = models.DateTimeField()

	def publish(self):
		self.book_add_date = timezone.now()
		self.save()
	def __unicode__(self):
		return self.bookId


class TransactionRecord(models.Model):

	id = models.CharField(primary_key = True, max_length = 70)
	borrowOperator = models.ForeignKey(FrontDeskLibrarian,related_name='borrowOperator')
	returnOperator = models.ForeignKey(FrontDeskLibrarian,related_name='returnOperator',null = True, blank = True)
	member = models.ForeignKey(Member)
	#faculty = models.ForeignKey(Faculty,null = True, blank = True)
	bookOnShelf = models.ForeignKey(BookOnShelf)
	borrowedTime = models.DateTimeField(default = timezone.now())	
	returnedTime = models.DateTimeField(null = True, blank = True)

	def __unicode__(self):
		return self.id
	def dueTime(self):
			return self.borrowedTime+datetime.timedelta(self.member.availableDays)


class BackupRecords(models.Model):

	recordId = models.AutoField(primary_key = True)
	operator = models.ForeignKey(Admin,null = True, blank = True)
	fileName = models.CharField(max_length = 50)
	operateTime = models.DateTimeField()
	fileSize = models.IntegerField(default = 0)
	location = models.CharField(max_length = 15)

	def __unicode__(self):
		return self.fileName
