# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render_to_response
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import BookInfo,Catagory,BookLocation,PublishingHouse,BookOnShelf,TransactionRecord,Admin,FrontDeskLibrarian,StackLibrarian,Member,BackupRecords
from .forms import AdminForm, BookForm, StudentForm, FacultyForm, FrontForm, StacktForm,StudentForm_add, FacultyForm_add, FrontForm_add, StacktForm_add, LendBookForm, ReturnBookForm, BookFormZHY, MemberForm
from django.shortcuts import redirect
import json, urllib
from urllib import urlencode
import urllib2
from django.http import HttpResponse
from django.template import RequestContext
import datetime
import ssl
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import os
import os.path
import shutil
import time

from decimal import *

#import MySQLdb

'''
wei shu guang
'''

def searchIndex(request):

	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)

	return render(request, 'search/search.html', {'accounttype': accounttype, 'account': account})


def dosearch(request):
	if request.method == 'GET':
		if  ('select' in request.GET) and ('keyword' in request.GET):
			select = request.GET['select'] # returns a string
			keyword = request.GET['keyword']
			keyword = keyword.lstrip()
			keyword = keyword.rstrip()

			results = []
			select = int(select)
			if select == 1:
				booklist = BookInfo.objects.filter(title__contains = keyword)
			elif select == 2:
				booklist = BookInfo.objects.filter(author__contains = keyword)
			elif select == 3:
				booklist = BookInfo.objects.filter(ISBN = keyword) #booklist is an object !!!
			else:
				publishers = PublishingHouse.objects.filter(name__contains = keyword) # publisher is a 
                # set an empty list
				booklist = []
				for publisher in publishers:
					queryset = publisher.bookinfo_set.all()
					booklist = booklist + list(queryset) #list queryset

			#return booklist(in table BookInfo)
			for book in booklist:

				#how many books in Table BookOnShelf named book
				queryset = book.bookonshelf_set.all()
		
				#library collections
				collections = len(queryset)
				#available copies
				available = 0
				for copy in queryset:
					if(copy.state == 'in'):
						available = available + 1
					else:
						available = available
				result = {'ISBN': book.ISBN, 'title':book.title, 'author': book.author, 'publishingHouse': book.publishingHouse, 'collections': collections, 'available': available}
				results.append(result)

			if len(results) == 0:
				empty_message = u'No book found'
				return render(request, 'search/searchLists.html', {'empty_message': empty_message})
			else:
				pageContent = paginate(request, results, 'results', 8, ['select', 'keyword'])
				return render(request, 'search/searchLists.html', pageContent)
		else:
			return render(request, 'search/search.html', {})
	else:
		return render(request, 'search/search.html', {})

             #if booklist == null
             
             #booklist is an QuerySet which contains BoonInfo objects, 
             #but searchReults should contain four Attributes:bookId,title,location,state; searchResults should be a 
             # list whose every item is a dictionary
			 
def book_detail_w(request, ISBN) :

	results = []
	#get BookInfo object of title: title
	bookInfo = BookInfo.objects.get(ISBN = ISBN)

	#get infos of bookInfo in table BookOnShelf
	bookonshelfs = bookInfo.bookonshelf_set.all()

	for bookOnShelf in bookonshelfs:

		result = {'bookId': bookOnShelf.bookId}
		location = bookOnShelf.bookLocation
		result['location'] = location.__unicode__()
		result['state'] = bookOnShelf.state
		results.append(result)

	return render(request, 'search/book_detail.html', {'results': results, 'bookInfo': bookInfo})



def login(request):

    if request.method == 'POST':
        if  ('select' in request.POST) and ('account' in request.POST) and ('password' in request.POST):
			
			select = request.POST['select']
			account = request.POST['account'] # returns a string
			password = request.POST['password']
			
			# make sure if someone is online
			currentaccount = request.session.get('account', default = None)
			currenttype = request.session.get('accounttype', default = None)
			if currentaccount != None and currenttype != None:
				if select != currenttype and account == currentaccount:
					# current user is the same as the one who wants to login
					if currenttype == 'Admin':
						return HttpResponseRedirect('/adminIndex/')
					elif currenttype == 'FrontDeskLibrarian':
						return HttpResponseRedirect('/frontIndex/')
				else:
					message = u'Another user is online, please logout first and then log in'
					return render_to_response('search/login.html', {'message': message})


			select = int(select)
			#Admin login
			if select == 1:
				queryset = Admin.objects.filter(account = account)
				if len(queryset) == 1:

					for admin in queryset:
						#validate password
						if admin.password == password:
							#注册session
							request.session['accounttype'] = 'Admin'
							request.session['account'] = account

							return HttpResponseRedirect('/adminIndex/')
						else:
							error_message2 = u'Password is wrong！'
							return render(request, 'search/login.html', {'error_message2': error_message2})
				else:
					error_message1 = u'Account does not exist！'
					return render(request, 'search/login.html', {'error_message1': error_message1})
			#front login
			elif select == 2:
				queryset = FrontDeskLibrarian.objects.filter(account = account)
				if len(queryset) == 1:

					for front in queryset:
						#validate password
						if front.password == password:
							#register session
							request.session['accounttype'] = 'FrontDeskLibrarian'
							request.session['account'] = account

							return HttpResponseRedirect('/frontIndex/')
						else:
							error_message2 = u'Password is wrong!'
							return render(request, 'search/login.html', {'error_message2': error_message2})

				else:
					error_message1 = u'Account does not exist!'
					return render(request, 'search/login.html', {'error_message1': error_message1})

			#stack login	
			elif select == 3:
				queryset = StackLibrarian.objects.filter(account = account)
				##validate account
				if len(queryset) == 1:
					for stack in queryset:
						#validate password
						if stack.password == password:
							#register session
							request.session['accounttype'] = 'StackLibrarian'
							request.session['account'] = account

							return HttpResponseRedirect('/stackIndex/')
						else:
							error_message2 = u'Password is wrong!'
							return render(request, 'search/login.html', {'error_message2': error_message2})
				else:
					error_message1 = u'Account does not exist!'
					return render(request, 'search/login.html', {'error_message1': error_message1})


			#member login
			elif select == 4:
				queryset = Member.objects.filter(account = account)
				if len(queryset) == 1:
					for member in queryset:
						#validate password
						if member.password == password:
							
							if member.type == 'faculty':
								request.session['accounttype'] = 'faculty'
							else:
								request.session['accounttype'] = 'student'
				
							request.session['account'] = account
							
							return HttpResponseRedirect('/member_my_activity/')
						else:
							error_message2 = u'Password is wrong!'
							return render(request, 'search/login.html', {'error_message2': error_message2})
				else:
					error_message1 = u'Account does not exist!'
					return render(request, 'search/login.html', {'error_message1': error_message1})
			
        else:
            return render(request, 'search/login.html', {})

    else:
		accounttype = request.session.get('accounttype', default = None)
		account = request.session.get('account', default = None)
		
		if accounttype == None and account == None:
			return render(request, 'search/login.html', {})
		else:
			#make sure what kind of user is online
			if accounttype == 'Admin':
				return HttpResponseRedirect('/adminIndex/')
			elif accounttype == 'FrontDeskLibrarian':
				return HttpResponseRedirect('/frontIndex/')
			elif accounttype == 'StackLibrarian':
				return HttpResponseRedirect('/stackIndex/')
			else:
				return HttpResponseRedirect('/member_my_activity/')


def logout(request):

	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)

	if accounttype == None:
		return HttpResponseRedirect('/login/')
	#del request.session['usertype']
	else:
		del request.session['accounttype']
		del request.session['account']

		return HttpResponseRedirect('/login/')
		

'''
唐波
'''
'''
Admin端
'''
def adminIndex(request):

	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)

	if accounttype != "Admin" :
		return HttpResponseRedirect('/login/')
	else:
		posts = BookOnShelf.objects.filter(book_add_date__lte=timezone.now()).order_by('-book_add_date')
		return render(request, 'admin/book/book_list.html', {'posts': posts,'account': account})
	
def adminInfo(request):
	
	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)

	if accounttype != "Admin":
		return HttpResponseRedirect('/login/')
	else:
		results = []
		adminlist = Admin.objects.filter(account = account)
		for admin in adminlist:
			if not admin.photo:
				admin.photo = '/static/photo/nophoto.png' 
			result = {'account':admin.account, 'name':admin.name,'password':admin.password,'gender':admin.gender,'tel':admin.tel,'photo':admin.photo,'admin_add_date':admin.admin_add_date}
			results.append(result)

		return render(request, 'admin/admin_detail.html', {'results':results,'account':account})
	
def adminInfoChangePassword(request):

	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)

	if accounttype != "Admin":
		return HttpResponseRedirect('/login/')
	else:
		return render(request, 'admin/admin_detail_changepassword.html', {'account': account})

def do_changepassword(request):

	oldpassword = request.POST['oldpassword']
	newpassword = request.POST['newpassword1']

	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)

	if accounttype != "Admin":
		return HttpResponseRedirect('/login/')
	else:
		admin = Admin.objects.get(account = account)
		#判断老密码是否合法
		if oldpassword == admin.password:
			admin.password = newpassword
			admin.save()
			return HttpResponseRedirect('/adminInfo/')
		else:
			error_message = u'old password is wrong'
			return render_to_response('admin/admin_detail_changepassword.html', {'error_message': error_message,'account': account})
	
	
#显示图书列表
def book_list(request):
	
	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)
	if request.method =='POST':
		return print_barcode_admin(request)
	else:
		if accounttype != "Admin":
			return HttpResponseRedirect('/login/')
		else:
			posts = BookOnShelf.objects.filter(book_add_date__lte=timezone.now()).order_by('-book_add_date')
			pageContent = paginate(request, posts, 'posts', 8)
			pageContent.update({'account':account})
			return render(request, 'admin/book/book_list.html', pageContent)
	
def dosearch_booklist(request):
	
	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)

	if accounttype != 'Admin':
		return HttpResponseRedirect('/login/')
	else:
		if request.method == 'GET':
			if  ('select' in request.GET) and ('keyword' in request.GET):
				select = request.GET['select'] # returns a string
				keyword = request.GET['keyword']   
				#*********define a list containing dicts*********
				results = []
				#search in table BooKInfo, Publishing House,according to 'select'
				###seachResults ---booklist from table BookInfo 
				
				# integer or string
				#******************************************
				select = int(select)
				if select == 1:
					booklist = BookInfo.objects.filter(title__contains = keyword)
				elif select == 2:
					booklist = BookInfo.objects.filter(author__contains = keyword)
				elif select == 3:
					booklist = BookInfo.objects.filter(ISBN = keyword) #booklist is an object !!!
				else:
					publishers = PublishingHouse.objects.filter(name__contains = keyword) # publisher is a 
					# set an empty list
					booklist = []
					for publisher in publishers:
						queryset = publisher.bookinfo_set.all()
						booklist = chain(booklist, list(queryset)) #list queryset

				#if booklist == null
             
				#booklist is an QuerySet which contains BoonInfo objects, 
				#but searchReults should contain four Attributes:bookId,title,location,state; searchResults should be a 
				#list whose every item is a dictionary
				for book in booklist:
					#results = []
					booksOnShelf = book.bookonshelf_set.all()
					#the same book has many copies
					for bookOnShelf in booksOnShelf:
						result = {'bookId':bookOnShelf.bookId, 'title':book.title,'author':book.author,'ISBN':book.ISBN,'publishingHouseName':book.publishingHouse.name}
						#get bookLocation
						bookLocation = bookOnShelf.bookLocation
						result['bookLocation'] = bookLocation.__unicode__()
						#get state
						result['state'] = bookOnShelf.state
						#get book_add_date
						result['book_add_date'] = bookOnShelf.book_add_date
						#add result to results
						results.append(result)
				if len(results) == 0:
					empty_message = u'No book found'
					return render(request, 'admin/book/booklist_search.html', {'empty_message': empty_message,'account':account})
				pageContent = paginate(request, results, 'results', 8, ['select', 'keyword'])
				pageContent.update({'account':account})
				return render(request, 'admin/book/booklist_search.html', pageContent)
			else:
				return render(request, 'admin/book/book_list.html', {'account': account})
		else:
			return render(request, 'admin/book/book_list.html', {'account': account})
		
def booklist_detail(request, bookId):

	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)

	if accounttype != "Admin":
		return HttpResponseRedirect('/login/')
	else:
		bookOnShelf = get_object_or_404(BookOnShelf, bookId = bookId)
		return render(request, 'admin/book/booklist_detail.html', {'bookOnShelf': bookOnShelf, 'account': account})
	
def delete_booklist(request,bookId):  
	
	results = get_object_or_404(BookOnShelf, bookId=bookId)
	results.delete()
	return HttpResponseRedirect(reverse('book_list'))
		
#显示图书详情	
def book_detail(request,pk):
	
	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)

	if accounttype != 'Admin':
		return HttpResponseRedirect('/login/')
	else:
		posts = get_object_or_404(BookOnShelf, pk=pk)
		return render(request,'admin/book/book_detail.html',{'posts':posts, 'account': account})
	
#删除图书
def delete_book(request,pk):  
	posts = get_object_or_404(BookOnShelf, pk=pk)
	posts.delete()
	return HttpResponseRedirect(reverse('book_list'))
	
#修改图书详情
def edit_book(request,pk):
	account = request.session.get('account', default = None)
	if account == None:
		return HttpResponseRedirect('/login/')
	else:
		post = get_object_or_404(BookOnShelf,pk=pk)
		return render(request, 'admin/book/edit_book.html', { 'post': post, 'account': account})	
		'''
			return redirect('LMS.views.book_detail', pk=post.pk)
		else:
			form = BookForm(instance=post)
		return render(request, 'admin/book/edit_book.html', {'form': form, 'post': post, 'account': account})	
		'''
def edit_book_admin(request):
			post = get_object_or_404(BookOnShelf,bookId=request.POST['bookId'])
			#存Catagory
			is_exist = Catagory.objects.filter(name = request.POST['catagoryName']).exists()
			if is_exist:
				queryset = Catagory.objects.filter(name = request.POST['catagoryName'])
				catagory = queryset[0]
			else:
			
				newId = Catagory.objects.count() + 1
				catagory = Catagory(catagoryId=newId,name=request.POST['catagoryName'])
				catagory.save()

			#存PublishingHouse
			is_exist = PublishingHouse.objects.filter(name = request.POST['publisher']).exists()
			if is_exist:
				queryset = PublishingHouse.objects.filter(name = request.POST['publisher'])
				publishingHouse = queryset[0]
			else:
			
				newId = PublishingHouse.objects.count() + 1
				publishingHouse = PublishingHouse(publisherId=newId,name=request.POST['publisher'])
				publishingHouse.save()
			
			#存BookInfo
			bookInfo = BookInfo(ISBN=request.POST['isbn13'],title=request.POST['title'],author=request.POST['author'],publishingHouse=publishingHouse,catagory=catagory,book_image_URL=request.POST['images_large_url'],introducton=request.POST['summary'])
			bookInfo.save()

			#存BookLocation
			is_exist = BookLocation.objects.filter(floor = request.POST['floor'],area = request.POST['area']).exists() 
			if is_exist :
					queryset = BookLocation.objects.filter(floor = request.POST['floor'],area = request.POST['area'] )
					bookLocation = queryset[0]
			else:
			
				newId = BookLocation.objects.count() + 1
				bookLocation = BookLocation(locationId=newId,floor = request.POST['floor'],area = request.POST['area'])
				bookLocation.save()
			
			state = request.POST['state']
			demo = BookOnShelf(bookId=request.POST['bookId'],bookLocation=bookLocation,bookInfo=bookInfo,state=request.POST['state'])
			demo.book_add_date = post.book_add_date
			demo.save()

			return redirect('LMS.views.book_detail', pk=demo.pk)
#通过ISBN添加图书	
def add_ISBN(request):
	
	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)

	if accounttype != 'Admin':
		return HttpResponseRedirect('/login/')
	else:
		return render(request,'admin/add_ISBN.html', {'account': account})
def	search(request):
	account = request.session.get('account', default = None)
	if account == None:
		return HttpResponseRedirect('/login/')
	else:
		return render_to_response('admin/add_ISBN.html')
		
#通过豆瓣api解析Json字符串在页面上显示
def getInfoFromDouban(request):
	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)
	if accounttype != 'Admin':
		return HttpResponseRedirect('/login/')
	else:
		isbn = request.GET['q']
		ssl._create_default_https_context = ssl._create_unverified_context
		#判断ISBN是否输入为空
		if not isbn :
			message = u'Please enter ISBN'
			return render_to_response('admin/add_ISBN.html',{'message':message,'account':account})
		url = 'https://api.douban.com/v2/book/isbn/'+isbn
		#判断ISBN是否存在
		status = urllib.urlopen(url).code
		if status == 404:
			message = u'Please check the ISBN'
			return render_to_response('admin/add_ISBN.html',{'message':message,'account':account})
		else:
			html = urllib.urlopen(url)
			hjson = json.loads(html.read()) 
			isbn13 = hjson['isbn13']
			title = hjson['title']
			author = hjson['author']
			if not author:
				author = u'NO AUTHOR TO SHOW'
			else:
				author = hjson['author'][0]
			translator = hjson['translator']
			if not translator:
				translator = u'NO TRANSLATOR TO SHOW'
			else:
				translator = hjson['translator'][0]
			pubdate = hjson['pubdate']
			publisher = hjson['publisher']
			if not publisher:
				publisher = u'NO PUBLISHER TO SHOW'
			else:	
				publisher = hjson['publisher']
			price = hjson['price']
			pages = hjson['pages']
			images_large = hjson['images']['large']
			summary = hjson['summary']
			if not summary:
				summary = u'NO SUMMARY TO SHOW'
			else:	
				summary = hjson['summary']
			return render_to_response('admin/add_ISBN.html',{'id':id,'isbn13':isbn13,'title':title,'author':author,'translator':translator,'pubdate':pubdate,'publisher':publisher,
								  'price':price,'pages':pages,'images_large':images_large,'summary':summary,'account':account})


#获得页面解析结果存入数据库	
def getInfo(request):
	
		BookNumber = request.POST['bookNumber']
		bookNumber = int(BookNumber)
		
		if bookNumber == 0:
			return HttpResponseRedirect('/add_ISBN_stack/')
		
		else:
			#存Catagory
			is_exist = Catagory.objects.filter(name = request.POST['catagoryName']).exists()
			if is_exist:
				queryset = Catagory.objects.filter(name = request.POST['catagoryName'])
				catagory = queryset[0]
			else:
			
				newId = Catagory.objects.count() + 1
				catagory = Catagory(catagoryId=newId,name=request.POST['catagoryName'])
				catagory.save()

			#存PublishingHouse
			is_exist = PublishingHouse.objects.filter(name = request.POST['publisher']).exists()
			if is_exist:
				queryset = PublishingHouse.objects.filter(name = request.POST['publisher'])
				publishingHouse = queryset[0]
			else:
			
				newId = PublishingHouse.objects.count() + 1
				publishingHouse = PublishingHouse(publisherId=newId,name=request.POST['publisher'])
				publishingHouse.save()
			
			#存BookInfo
			bookInfo = BookInfo(ISBN=request.POST['isbn13'],title=request.POST['title'],author=request.POST['author'],publishingHouse=publishingHouse,catagory=catagory,book_image_URL=request.POST['images_large_url'],introducton=request.POST['summary'])
			bookInfo.save()

			#存BookLocation
			is_exist = BookLocation.objects.filter(floor = request.POST['floor'],area = request.POST['area']).exists() 
			#is_exist = BookLocation.objects.filter(floor = request.POST['floor']).exists() 
			#is_exist1 = BookLocation.objects.filter(area = request.POST['area']).exists() 
			if is_exist:
			
				queryset = BookLocation.objects.filter(floor = request.POST['floor'],area = request.POST['area'] )
				bookLocation = queryset[0]
			else:
			
				newId = BookLocation.objects.count() + 1
				bookLocation = BookLocation(locationId=newId,floor = request.POST['floor'],area = request.POST['area'])
				bookLocation.save()
			
			

			for i in range(0 , bookNumber):

				if BookOnShelf.objects.count() == 0:
					
					newId = 1
					newId_str = '%07d'% newId
					demo = BookOnShelf(bookId=newId_str,bookLocation=bookLocation,bookInfo=bookInfo,state='in')
					demo.book_add_date = timezone.now()
					demo.save()

				else:
					newId = BookOnShelf.objects.order_by('-bookId')[0]
					newId = newId.bookId
					newId = int(newId) + 1
					newId_str = '%07d'% newId
					demo = BookOnShelf(bookId=newId_str,bookLocation=bookLocation,bookInfo=bookInfo,state='in')
					demo.book_add_date = timezone.now()
					demo.save()

			return redirect('LMS.views.book_detail_t', pk=demo.pk, bookNumber = bookNumber)

def book_detail_t(request, pk, bookNumber) :

	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)

	if request.method =='POST':
		return print_barcode_t(request)
	else:
		if accounttype !=  'Admin':
			return HttpResponseRedirect('/login/')
		else:
			results = []
			posts = get_object_or_404(BookOnShelf, pk=pk)
			ISBN = posts.bookInfo.ISBN
			bookInfo = BookInfo.objects.get(ISBN = ISBN)
			bookNumber=bookNumber
			bookonshelfs = bookInfo.bookonshelf_set.all().order_by('-book_add_date')[0:bookNumber]
			for bookOnShelf in bookonshelfs:
				result = {'bookId': bookOnShelf.bookId}
				location = bookOnShelf.bookLocation
				result['location'] = location.__unicode__()
				result['state'] = bookOnShelf.state
				results.append(result)
			return render(request, 'admin/book/book_detail_t.html', {'results': results, 'bookInfo': bookInfo ,'account':account})	

#显示Student列表
def student_list(request):
	
	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)


	if accounttype != 'Admin':
		return HttpResponseRedirect('/login/')
	else:
		posts = []
		#posts = Member.objects.filter(member_add_date__lte=timezone.now()).order_by('-member_add_date')
		posts1 = Member.objects.filter(type = 'undergraduate').order_by('-member_add_date')
		posts2 = Member.objects.filter(type = 'postgraduate').order_by('-member_add_date')
		posts.extend(posts1)
		posts.extend(posts2)
		pageContent = paginate(request, posts, 'posts', 8)
		pageContent.update({'account':account})
		return render(request, 'admin/student/student_list.html', pageContent)
		
def dosearch_studentlist(request):
	
	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)

	if accounttype != 'Admin':
		return HttpResponseRedirect('/login/')
	else:
		if request.method == 'GET':
			if  ('select' in request.GET) and ('keyword' in request.GET):

				select = request.GET['select'] # returns a string
				keyword = request.GET['keyword']   
				#*********define a list containing dicts*********
				results = []
				#search in table BooKInfo, Publishing House,according to 'select'
				###seachResults ---booklist from table BookInfo 
				# integer or string
				select = int(select)
				if select == 1:
					studentlist = Member.objects.filter(account = keyword)
				else:
					studentlist = Member.objects.filter(name__contains = keyword)
				for student in studentlist:
					if student.type == 'undergraduate' or student.type == 'postgraduate':
							result = {'account':student.account, 'name':student.name,
							'type':student.type,'school':student.school,'classNo':student.classNo,'major':student.major,
							'bookOwning':student.bookOwning,'debt':student.debt,'member_add_date':student.member_add_date}
							#add result to results
							results.append(result)
				if len(results) == 0:
					empty_message = u'No student found'
					return render(request, 'admin/student/studentlist_search.html', {'empty_message': empty_message,'account':account})
				pageContent = paginate(request, results, 'results', 8, ['select', 'keyword'])
				pageContent.update({'account':account})
				return render(request, 'admin/student/studentlist_search.html', pageContent)
			else:
				return render(request, 'admin/student/student_list.html', {})
		else:
			return render(request, 'admin/student/student_list.html', {})
			
def studentlist_detail(request,account):

	account1 = request.session.get('account', default = None)
	if account1 == None:
		return HttpResponseRedirect('/login/')
	else:
		student = get_object_or_404(Member, account=account)
		if not student.photo:
			student.photo = '/static/photo/nophoto.png'
		return render(request,'admin/student/studentlist_detail.html',{'student':student, 'account1':account1})
	
def delete_studentlist(request,account):  

	results = get_object_or_404(Member, account=account)
	results.delete()
	return HttpResponseRedirect(reverse('student_list'))
	
#删除Student
def delete_student(request,pk):  

	posts = get_object_or_404(Member, pk=pk)
	posts.delete()
	return HttpResponseRedirect(reverse('student_list'))
	
#显示Student信息
def student_detail(request,pk):

	account = request.session.get('account', default = None)
	if account == None:
		return HttpResponseRedirect('/login/')
	else:
		posts = get_object_or_404(Member, pk=pk)
		if not posts.photo:
			posts.photo = '/static/photo/nophoto.png'
		return render(request,'admin/student/student_detail.html',{'posts':posts, 'account': account})
	
#修改Student信息
def edit_student(request,pk):

	account = request.session.get('account', default = None)
	if account == None:
		return HttpResponseRedirect('/login/')
	else:
		post = get_object_or_404(Member,pk=pk)
		if request.method == "POST":
			form = StudentForm(request.POST, request.FILES, instance=post)
			if form.is_valid():
				post = form.save(commit=False) 
				if not post.photo:
					post.photo = '/static/photo/nophoto.png'
				if post.debt < 0:
					message = u'The debt must be greater than 0!'
					return render(request, 'admin/student/edit_student.html', {'form': form, 'account': account,'message':message}) 
				post.save()
				return redirect('LMS.views.student_detail', pk=post.pk)
		else:
			form = StudentForm(instance=post)
		return render(request, 'admin/student/edit_student.html', {'form': form, 'post':post,'account':account})

#新增Student
def add_student(request):

	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)

	if accounttype != 'Admin':
		return HttpResponseRedirect('/login/')
	else:
		if request.method == "POST":
			form = StudentForm_add(request.POST,request.FILES)
			if form.is_valid():
				post = form.save(commit=False)
				if not post.photo:
					post.photo = '/static/photo/nophoto.png'
				if post.debt < 0:
					message = u'The debt must be greater than 0!'
					return render(request, 'admin/student/add_student.html', {'form': form, 'account': account,'message':message}) 
				post.author = request.user
				post.member_add_date = timezone.now()
				post.save()
				return redirect('LMS.views.student_detail', pk=post.pk)
		else:
			form = StudentForm_add()
		return render(request, 'admin/student/add_student.html', {'form': form, 'account': account})

#Faculty列表
def faculty_list(request):

	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)

	if accounttype != 'Admin':
		return HttpResponseRedirect('/login/')
	else:
		#posts = Member.objects.filter(member_add_date__lte=timezone.now()).order_by('-member_add_date')
		posts = Member.objects.filter(type = 'faculty').order_by('-member_add_date')
		pageContent = paginate(request, posts, 'posts', 8)
		pageContent.update({'account':account})
		return render(request, 'admin/faculty/faculty_list.html', pageContent)

def dosearch_facultylist(request):

	account = request.session.get('account', default = None)
	if account == None:
		return HttpResponseRedirect('/login/')
	else:
		if request.method == 'GET':
			if('select' in request.GET) and ('keyword' in request.GET):
				select = request.GET['select'] # returns a string
				keyword = request.GET['keyword']
				#*********define a list containing dicts*********
				results = []
				#search in table BooKInfo, Publishing House,according to 'select'
				###seachResults ---booklist from table BookInfo
				select = int(select)
				if select == 1:
					facultylist = Member.objects.filter(account = keyword)
				else:
					facultylist = Member.objects.filter(name__contains = keyword)
				for faculty in facultylist:
					if(faculty.type == 'faculty'):
						result = {'account':faculty.account, 'name':faculty.name,'bookOwning':faculty.bookOwning,'member_add_date':faculty.member_add_date,'type':faculty.type,'debt':faculty.debt}
						#add result to results
						results.append(result)
				if len(results) == 0:
					empty_message = u'No faculty found'
					return render(request, 'admin/faculty/facultylist_search.html', {'empty_message': empty_message,'account':account})	
				pageContent = paginate(request, results, 'results', 8, ['select', 'keyword'])
				pageContent.update({'account':account})
				return render(request, 'admin/faculty/facultylist_search.html', pageContent)
			else:
				return render(request, 'admin/faculty/faculty_list.html', {})
		else:
			return render(request, 'admin/faculty/faculty_list.html', {})

def facultylist_detail(request,account):

	account1 = request.session.get('account', default = None)
	if account1 == None:
		return HttpResponseRedirect('/login/')
	else:
		faculty = get_object_or_404(Member, account=account)
		if not faculty.photo:
			faculty.photo = '/static/photo/nophoto.png'
        return render(request,'admin/faculty/facultylist_detail.html',{'faculty':faculty, 'account1':account1})

def delete_facultylist(request,account):

	results = get_object_or_404(Member, account=account)
	results.delete()
	return HttpResponseRedirect(reverse('faculty_list'))

#删除Faculty
def delete_faculty(request,pk):

	posts = get_object_or_404(Member, pk=pk)
	posts.delete()
	return HttpResponseRedirect(reverse('faculty_list'))

#Faculty详情
def faculty_detail(request,pk):

	account = request.session.get('account', default = None)
	if account == None:
		return HttpResponseRedirect('/login/')
	else:
		posts = get_object_or_404(Member, pk=pk)
        if not posts.photo:
            posts.photo = '/static/photo/nophoto.png'
        return render(request,'admin/faculty/faculty_detail.html',{'posts':posts, 'account':account})


#修改Faculty
def edit_faculty(request,pk):

	account = request.session.get('account', default = None)
	if account == None:
		return HttpResponseRedirect('/login/')
	else:
		post = get_object_or_404(Member,pk=pk)
		if request.method == "POST":
			form = FacultyForm(request.POST, request.FILES, instance=post)
			if form.is_valid():
				post = form.save(commit=False)
				if not post.photo:
					post.photo = '/static/photo/nophoto.png'
				if post.debt < 0:
					message = u'The debt must be greater than 0!'
					return render(request, 'admin/faculty/edit_faculty.html', {'form': form, 'account':account,'message':message})
				post.published_date = timezone.now()
				post.save()
				return redirect('LMS.views.faculty_detail', pk=post.pk)
		else:
			form = FacultyForm(instance=post)
		return render(request, 'admin/faculty/edit_faculty.html', {'form': form, 'post':post,'account':account})

			
#添加Faculty
def add_faculty(request):

	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)

	if accounttype != 'Admin':
		return HttpResponseRedirect('/login/')
	else:
		if request.method == "POST":
			form = FacultyForm_add(request.POST,request.FILES)
			if form.is_valid():
				post = form.save(commit=False)
				post.member_add_date = timezone.now()
				if not post.photo:
					post.photo = '/static/photo/nophoto.png'
				if post.debt < 0:
					message = u'The debt must be greater than 0!'
					return render(request, 'admin/faculty/add_faculty.html', {'form': form, 'account':account,'message':message})
				post.major = 'null'
				post.classNo = 'null'
				post.type = 'faculty'
				post.save()
				return redirect('LMS.views.faculty_detail', pk=post.pk)
		else:
			form = FacultyForm_add()
		return render(request, 'admin/faculty/add_faculty.html', {'form': form, 'account':account})

		
#FrontDeskLibrarian列表
def front_list(request):

	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)

	if accounttype != 'Admin':
		return HttpResponseRedirect('/login/')
	else:
		posts = FrontDeskLibrarian.objects.filter(front_add_date__lte=timezone.now()).order_by('-front_add_date')
		pageContent = paginate(request, posts, 'posts', 8)
		pageContent.update({'account':account})
		return render(request, 'admin/frontDeskLibrarian/front_list.html', pageContent)
		
def dosearch_frontlist(request):

	account = request.session.get('account', default = None)
	if account == None:
		return HttpResponseRedirect('/login/')
	else:
		if request.method == 'GET':
			if('select' in request.GET) and ('keyword' in request.GET):
				select = request.GET['select'] # returns a string
				keyword = request.GET['keyword']   
				#*********define a list containing dicts*********
				results = []
				#search in table BooKInfo, Publishing House,according to 'select'
				###seachResults ---booklist from table BookInfo 
				select = int(select)
				if select == 1:
					frontlist = FrontDeskLibrarian.objects.filter(account = keyword)
				else:
					frontlist = FrontDeskLibrarian.objects.filter(name__contains = keyword)
				for front in frontlist:
					result = {'account':front.account, 'name':front.name,'front_add_date':front.front_add_date}
					#add result to results
					results.append(result)
				if len(results) == 0:
					empty_message = u'No frontDeskLibrarian found'
					return render(request, 'admin/frontDeskLibrarian/frontlist_search.html', {'empty_message': empty_message,'account':account})
				pageContent = paginate(request, results, 'results', 8, ['select', 'keyword'])
				pageContent.update({'account':account})
				return render(request, 'admin/frontDeskLibrarian/frontlist_search.html', pageContent)
			else:
				return render(request, 'admin/frontDeskLibrarian/front_list.html', {})
		else:
			return render(request, 'admin/frontDeskLibrarian/front_list.html', {})
			
def frontlist_detail(request,account):

	account1 = request.session.get('account', default = None)
	if account1 == None:
		return HttpResponseRedirect('/login/')
	else:
		front = get_object_or_404(FrontDeskLibrarian, account=account)
		if not front.photo:
			front.photo = '/static/photo/nophoto.png'
		return render(request,'admin/frontDeskLibrarian/frontlist_detail.html',{'front':front, 'account1':account1})
		

def delete_frontlist(request,account):  

	results = get_object_or_404(FrontDeskLibrarian, account=account)
	results.delete()
	return HttpResponseRedirect(reverse('front_list'))
	
#删除FrontDeskLibrarian
def delete_front(request,pk):  

	posts = get_object_or_404(FrontDeskLibrarian, pk=pk)
	posts.delete()
	return HttpResponseRedirect(reverse('front_list'))
	
#FrontDeskLibrarian详情
def front_detail(request,pk):

	account = request.session.get('account', default = None)
	if account == None:
		return HttpResponseRedirect('/login/')
	else:
		posts = get_object_or_404(FrontDeskLibrarian, pk=pk)
		if not posts.photo:
			posts.photo = '/static/photo/nophoto.png'
		return render(request,'admin/frontDeskLibrarian/front_detail.html',{'posts':posts, 'account':account})
		
#修改FrontDeskLibrarian详情
def edit_front(request,pk):

	account = request.session.get('account', default = None)
	if account == None:
		return HttpResponseRedirect('/login/')
	else:
		post = get_object_or_404(FrontDeskLibrarian,pk=pk)
		if request.method == "POST":
			form = FrontForm(request.POST, request.FILES, instance=post)
			if form.is_valid():
				post = form.save(commit=False) 
				if not post.photo:
					post.photo = '/static/photo/nophoto.png'
				post.published_date = timezone.now()
				post.save()
				return redirect('LMS.views.front_detail', pk=post.pk)
		else:
			form = FrontForm(instance=post)
		return render(request, 'admin/frontDeskLibrarian/edit_front.html', {'form': form, 'post':post,'account':account})
		
#添加FrontDeskLibrarian
def add_front(request):

	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)

	if accounttype != 'Admin':
		return HttpResponseRedirect('/login/')
	else:
		if request.method == "POST":
			form = FrontForm_add(request.POST,request.FILES)
			if form.is_valid():
				post = form.save(commit=False)
				if not post.photo:
					post.photo = '/static/photo/nophoto.png'
				post.front_add_date = timezone.now()
				post.save()
				return redirect('LMS.views.front_detail', pk=post.pk)
		else:
			form = FrontForm_add()
		return render(request, 'admin/frontDeskLibrarian/add_front.html', {'form': form, 'account':account})

	
#StackLibrarian列表
def stack_list(request):

	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)

	if accounttype != 'Admin':
		return HttpResponseRedirect('/login/')
	else:
		posts = StackLibrarian.objects.filter(stack_add_date__lte=timezone.now()).order_by('-stack_add_date')
		pageContent = paginate(request, posts, 'posts', 8)
		pageContent.update({'account':account})
		return render(request, 'admin/stackLibrarian/stack_list.html', pageContent)
		
def dosearch_stacklist(request):

	account = request.session.get('account', default = None)
	if account == None:
		return HttpResponseRedirect('/login/')
	else:
		if request.method == 'GET':
			if  ('select' in request.GET) and ('keyword' in request.GET):
				select = request.GET['select'] # returns a string
				keyword = request.GET['keyword']   
				#*********define a list containing dicts*********
				results = []
				#search in table BooKInfo, Publishing House,according to 'select'
				###seachResults ---booklist from table BookInfo 
				select = int(select)
				if select == 1:
					stacklist = StackLibrarian.objects.filter(account = keyword)
				else:
					stacklist = StackLibrarian.objects.filter(name__contains = keyword)
				for stack in stacklist:
					result = {'account':stack.account, 'name':stack.name,'stack_add_date':stack.stack_add_date}
					#add result to results
					results.append(result)
				if len(results) == 0:
					empty_message = u'No stackLibrarian found'
					return render(request, 'admin/stackLibrarian/stacklist_search.html', {'empty_message': empty_message,'account':account})
				pageContent = paginate(request, results, 'results', 8, ['select', 'keyword'])
				pageContent.update({'account':account})
				return render(request, 'admin/stackLibrarian/stacklist_search.html', pageContent)
			else:
				return render(request, 'admin/stackLibrarian/stack_list.html', {})
		else:
			return render(request, 'admin/stackLibrarian/stack_list.html', {})
			
def stacklist_detail(request,account):

	account1 = request.session.get('account', default = None)
	if account1 == None:
		return HttpResponseRedirect('/login/')
	else:
		stack = get_object_or_404(StackLibrarian, account=account)
		if not stack.photo:
			stack.photo = '/static/photo/nophoto.png'
		return render(request,'admin/stackLibrarian/stacklist_detail.html',{'stack':stack,'account1':account1})


def delete_stacklist(request,account): 
	
	results = get_object_or_404(StackLibrarian, account=account)
	results.delete()
	return HttpResponseRedirect(reverse('stack_list'))
	
#删除StackLibrarian
def delete_stack(request,pk):  

	posts = get_object_or_404(StackLibrarian, pk=pk)
	posts.delete()
	return HttpResponseRedirect(reverse('stack_list'))
	
#StackLibrarian详情
def stack_detail(request,pk):
	
	account = request.session.get('account', default = None)
	if account == None:
		return HttpResponseRedirect('/login/')
	else:
		posts = get_object_or_404(StackLibrarian, pk=pk)
		if not posts.photo:
			posts.photo = '/static/photo/nophoto.png'
		return render(request,'admin/stackLibrarian/stack_detail.html',{'posts':posts,'account':account})
	
#修改StackLibrarian详情
def edit_stack(request,pk):

	account = request.session.get('account', default = None)
	if account == None:
		return HttpResponseRedirect('/login/')
	else:
		post = get_object_or_404(StackLibrarian,pk=pk)
		if request.method == "POST":
			form = StacktForm(request.POST, request.FILES, instance=post)
			if form.is_valid():
				post = form.save(commit=False) 
				if not post.photo:
					post.photo = '/static/photo/nophoto.png'
				post.published_date = timezone.now()
				post.save()
				return redirect('LMS.views.stack_detail', pk=post.pk)
		else:
			form = StacktForm(instance=post)
		return render(request, 'admin/stackLibrarian/edit_stack.html', {'form': form,'post': post,'account':account})
		
#添加StackLibrarian
def add_stack(request):

	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)

	if accounttype != 'Admin':
		return HttpResponseRedirect('/login/')
	else:
		if request.method == "POST":
			form = StacktForm_add(request.POST,request.FILES)
			if form.is_valid():
				post = form.save(commit=False)
				if not post.photo:
					post.photo = '/static/photo/nophoto.png'
				post.stack_add_date = timezone.now()
				post.save()
				return redirect('LMS.views.stack_detail', pk=post.pk)
		else:
			form = StacktForm_add()
		return render(request, 'admin/stackLibrarian/add_stack.html', {'form': form,'account':account})


		




'''
唐波
'''	
'''
StackLibrarian端
'''
def stackIndex(request):

	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)
	
	if accounttype != 'StackLibrarian':
		return HttpResponseRedirect('/login/')
	else:
		posts = BookOnShelf.objects.filter(book_add_date__lte=timezone.now()).order_by('-book_add_date')
		return render(request, 'stack/book/book_list_stack.html',{'posts':posts,'accounttype': accounttype, 'account': account})
	
def stackInfo(request):
	
	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)

	if accounttype != 'StackLibrarian':
		return HttpResponseRedirect('/login/')
	else:
	
		results = []
		stacklist = StackLibrarian.objects.filter(account = account)
		for stack in stacklist:
			if not stack.photo:
				stack.photo = '/static/photo/nophoto.png' 
			result = {'account':stack.account, 'name':stack.name,'password':stack.password,'gender':stack.gender,'tel':stack.tel,'photo':stack.photo,'stack_add_date':stack.stack_add_date}
			results.append(result)
			
	return render(request, 'stack/stack_detail.html', {'results':results,'account': account})
	
def stackInfoChangePassword(request):
	
	account = request.session.get('account', default = None)
	if account == None:
		return HttpResponseRedirect('/login/')
	else:
	
		return render(request, 'stack/stack_detail_changepassword.html', {'account': account})

def do_changepassword_stack(request):

	oldpassword = request.POST['oldpassword']
	newpassword = request.POST['newpassword1']
	
	account = request.session.get('account', default = None)
	if account == None:
		return HttpResponseRedirect('/login/')
	else:
	
		stack = StackLibrarian.objects.get(account = account)
		#判断老密码是否合法
		if oldpassword == stack.password:
			stack.password = newpassword
			stack.save()
			return HttpResponseRedirect('/stackInfo/')
		else:
			error_message = u'old password is wrong'
			return render_to_response('stack/stack_detail_changepassword.html', {'error_message': error_message,'account': account})
	
	
#显示图书列表
def book_list_stack(request):
	
	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)

	if request.method =='POST':
		return print_barcode_stack(request)
	else:
		if accounttype != 'StackLibrarian':
			return HttpResponseRedirect('/login/')
		else:
			posts = BookOnShelf.objects.filter(book_add_date__lte=timezone.now()).order_by('-book_add_date')
			pageContent = paginate(request, posts, 'posts', 8)
			pageContent.update({'account':account})
			return render(request, 'stack/book/book_list_stack.html', pageContent)
	
def dosearch_booklist_stack(request):
	
	account = request.session.get('account', default = None)
	if account == None:
		return HttpResponseRedirect('/login/')
	else:
	
		if request.method == 'GET':
			if  ('select' in request.GET) and ('keyword' in request.GET):
				select = request.GET['select'] # returns a string
				keyword = request.GET['keyword']   
				#*********define a list containing dicts*********
				results = []
				#search in table BooKInfo, Publishing House,according to 'select'
				###seachResults ---booklist from table BookInfo 
				
				# integer or string
				#******************************************
				select = int(select)
				if select == 1:
					booklist = BookInfo.objects.filter(title__contains = keyword)
				elif select == 2:
					booklist = BookInfo.objects.filter(author__contains = keyword)
				elif select == 3:
					booklist = BookInfo.objects.filter(ISBN = keyword) #booklist is an object !!!
				else:
					publishers = PublishingHouse.objects.filter(name__contains = keyword) # publisher is a 
					# set an empty list
					booklist = []
					for publisher in publishers:
						queryset = publisher.bookinfo_set.all()
						booklist = chain(booklist, list(queryset)) #list queryset

				#if booklist == null
             
				#booklist is an QuerySet which contains BoonInfo objects, 
				#but searchReults should contain four Attributes:bookId,title,location,state; searchResults should be a 
				#list whose every item is a dictionary
				for book in booklist:
					#results = []
					booksOnShelf = book.bookonshelf_set.all()
					#the same book has many copies
					for bookOnShelf in booksOnShelf:
						result = {'bookId':bookOnShelf.bookId, 'title':book.title,'author':book.author,'ISBN':book.ISBN,'publishingHouseName':book.publishingHouse.name}
						#get bookLocation
						bookLocation = bookOnShelf.bookLocation
						result['bookLocation'] = bookLocation.__unicode__()
						#get state
						result['state'] = bookOnShelf.state
						#get book_add_date
						result['book_add_date'] = bookOnShelf.book_add_date
						#add result to results
						results.append(result)
				pageContent = paginate(request, results, 'results', 8, ['select', 'keyword'])
				pageContent.update({'account':account})
				return render(request, 'stack/book/booklist_search.html', pageContent)
			else:
				return render(request, 'stack/book/book_list_stack.html', {'account': account})
		else:
			return render(request, 'stack/book/book_list_stack.html', {'account': account})
		
def booklist_detail_stack(request, bookId):
	
	account = request.session.get('account', default = None)
	if account == None:
		return HttpResponseRedirect('/login/')
	else:
	
		bookOnShelf = get_object_or_404(BookOnShelf, bookId = bookId)
		return render(request, 'stack/book/booklist_detail.html', {'bookOnShelf': bookOnShelf, 'account': account})
	
def delete_booklist_stack(request,bookId):  
	
	results = get_object_or_404(BookOnShelf, bookId=bookId)
	results.delete()
	return HttpResponseRedirect(reverse('book_list_stack'))
		
#显示图书详情	
def book_detail_stack(request,pk):
	
	account = request.session.get('account', default = None)
	if account == None:
		return HttpResponseRedirect('/login/')
	else:
	
		posts = get_object_or_404(BookOnShelf, pk=pk)
		return render(request,'stack/book/book_detail.html',{'posts':posts, 'account': account})
	
#删除图书
def delete_book_stack(request,pk):  
	posts = get_object_or_404(BookOnShelf, pk=pk)
	posts.delete()
	return HttpResponseRedirect(reverse('book_list_stack'))
	
#修改图书详情
def edit_book_stack(request,pk):
	
	account = request.session.get('account', default = None)
	if account == None:
		return HttpResponseRedirect('/login/')
	else:
	
		post = get_object_or_404(BookOnShelf,pk=pk)
		return render(request, 'stack/book/edit_book.html', { 'account': account,'post': post})	
def edit_book_stack_stack(request):
			post = get_object_or_404(BookOnShelf,bookId=request.POST['bookId'])
			#存Catagory
			is_exist = Catagory.objects.filter(name = request.POST['catagoryName']).exists()
			if is_exist:
				queryset = Catagory.objects.filter(name = request.POST['catagoryName'])
				catagory = queryset[0]
			else:
			
				newId = Catagory.objects.count() + 1
				catagory = Catagory(catagoryId=newId,name=request.POST['catagoryName'])
				catagory.save()

			#存PublishingHouse
			is_exist = PublishingHouse.objects.filter(name = request.POST['publisher']).exists()
			if is_exist:
				queryset = PublishingHouse.objects.filter(name = request.POST['publisher'])
				publishingHouse = queryset[0]
			else:
			
				newId = PublishingHouse.objects.count() + 1
				publishingHouse = PublishingHouse(publisherId=newId,name=request.POST['publisher'])
				publishingHouse.save()
			
			#存BookInfo
			bookInfo = BookInfo(ISBN=request.POST['isbn13'],title=request.POST['title'],author=request.POST['author'],publishingHouse=publishingHouse,catagory=catagory,book_image_URL=request.POST['images_large_url'],introducton=request.POST['summary'])
			bookInfo.save()

			#存BookLocation
			is_exist = BookLocation.objects.filter(floor = request.POST['floor'],area = request.POST['area']).exists() 
			if is_exist :
					queryset = BookLocation.objects.filter(floor = request.POST['floor'],area = request.POST['area'] )
					bookLocation = queryset[0]
			else:
			
				newId = BookLocation.objects.count() + 1
				bookLocation = BookLocation(locationId=newId,floor = request.POST['floor'],area = request.POST['area'])
				bookLocation.save()
			
			demo = BookOnShelf(bookId=request.POST['bookId'],bookLocation=bookLocation,bookInfo=bookInfo,state=post.state)
			demo.book_add_date = post.book_add_date
			demo.save()

			return redirect('LMS.views.book_detail_stack', pk=demo.pk)
#通过ISBN添加图书	
def add_ISBN_stack(request):
	
	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)

	if accounttype != 'StackLibrarian':
		return HttpResponseRedirect('/login/')
	else:
	
		return render(request,'stack/add_ISBN.html', {'account': account})
def	search_stack(request):
	
	account = request.session.get('account', default = None)
	if account == None:
		return HttpResponseRedirect('/login/')
	else:
	
		return render_to_response('stack/add_ISBN.html')
		
#通过豆瓣api解析Json字符串在页面上显示
def getInfoFromDouban_stack(request):
	account = request.session.get('account', default = None)
	if account == None:
		return HttpResponseRedirect('/login/')
	else:
		isbn = request.GET['q']
		ssl._create_default_https_context = ssl._create_unverified_context
		#判断ISBN是否输入为空
		if not isbn :
			message = u'Please enter ISBN'
			return render_to_response('stack/add_ISBN.html',{'message':message,'account':account})
		url = 'https://api.douban.com/v2/book/isbn/'+isbn
		#判断ISBN是否存在
		status = urllib.urlopen(url).code
		if status == 404:
			message = u'Please check the ISBN'
			return render_to_response('stack/add_ISBN.html',{'message':message,'account':account})
		else:
			html = urllib.urlopen(url)
			hjson = json.loads(html.read()) 
			isbn13 = hjson['isbn13']
			title = hjson['title']
			author = hjson['author']
			if not author:
				author = u'NO AUTHOR TO SHOW'
			else:
				author = hjson['author'][0]
			translator = hjson['translator']
			if not translator:
				translator = u'NO TRANSLATOR TO SHOW'
			else:
				translator = hjson['translator'][0]
			pubdate = hjson['pubdate']
			publisher = hjson['publisher']
			if not publisher:
				publisher = u'NO PUBLISHER TO SHOW'
			else:	
				publisher = hjson['publisher']
			price = hjson['price']
			pages = hjson['pages']
			images_large = hjson['images']['large']
			summary = hjson['summary']
			if not summary:
				summary = u'NO SUMMARY TO SHOW'
			else:	
				summary = hjson['summary']
			return render_to_response('stack/add_ISBN.html',{'id':id,'isbn13':isbn13,'title':title,'author':author,'translator':translator,'pubdate':pubdate,'publisher':publisher,
								  'price':price,'pages':pages,'images_large':images_large,'summary':summary,'account':account})

#获得页面解析结果存入数据库

def getInfo_stack(request):
		BookNumber = request.POST['bookNumber']
		bookNumber = int(BookNumber)
		
		if bookNumber == 0:
			return HttpResponseRedirect('/add_ISBN_stack/')
		else:

			#存Catagory
			is_exist = Catagory.objects.filter(name = request.POST['catagoryName']).exists()
			if is_exist:
				queryset = Catagory.objects.filter(name = request.POST['catagoryName'])
				catagory = queryset[0]
			else:
			
				newId = Catagory.objects.count() + 1
				catagory = Catagory(catagoryId=newId,name=request.POST['catagoryName'])
				catagory.save()

			#存PublishingHouse
			is_exist = PublishingHouse.objects.filter(name = request.POST['publisher']).exists()
			if is_exist:
				queryset = PublishingHouse.objects.filter(name = request.POST['publisher'])
				publishingHouse = queryset[0]
			else:
			
				newId = PublishingHouse.objects.count() + 1
				publishingHouse = PublishingHouse(publisherId=newId,name=request.POST['publisher'])
				publishingHouse.save()
			
			#存BookInfo
			bookInfo = BookInfo(ISBN=request.POST['isbn13'],title=request.POST['title'],author=request.POST['author'],publishingHouse=publishingHouse,catagory=catagory,book_image_URL=request.POST['images_large_url'],introducton=request.POST['summary'])
			bookInfo.save()

			#存BookLocation
			is_exist = BookLocation.objects.filter(floor = request.POST['floor']).exists() 
			is_exist1 = BookLocation.objects.filter(area = request.POST['area']).exists() 
			if is_exist:
				if is_exist1:
					queryset = BookLocation.objects.filter(floor = request.POST['floor'],area = request.POST['area'] )
					bookLocation = queryset[0]
			else:
			
				newId = BookLocation.objects.count() + 1
				bookLocation = BookLocation(locationId=newId,floor = request.POST['floor'],area = request.POST['area'])
				bookLocation.save()
			

			for i in range(1 , bookNumber + 1):

				if BookOnShelf.objects.count() == 0:
					
					newId = 1
					newId_str = '%07d'% newId
					demo = BookOnShelf(bookId=newId_str,bookLocation=bookLocation,bookInfo=bookInfo,state='in')
					demo.book_add_date = timezone.now()
					demo.save()

				else:
					newId = BookOnShelf.objects.order_by('-bookId')[0]
					newId = newId.bookId
					newId = int(newId) + 1
					newId_str = '%07d'% newId
					demo = BookOnShelf(bookId=newId_str,bookLocation=bookLocation,bookInfo=bookInfo,state='in')
					demo.book_add_date = timezone.now()
					demo.save()
			
			return redirect('LMS.views.book_detail_t_stack', pk=demo.pk, bookNumber=bookNumber)
def book_detail_t_stack(request, pk,bookNumber) :
	account = request.session.get('account', default = None)
	if request.method =='POST':
		return print_barcode_stack_t(request)
	else:
		if account == None:
			return HttpResponseRedirect('/login/')
		else:
			results = []
			posts = get_object_or_404(BookOnShelf, pk=pk)
			ISBN = posts.bookInfo.ISBN
			bookInfo = BookInfo.objects.get(ISBN = ISBN)
			bookNumber=bookNumber
			bookonshelfs = bookInfo.bookonshelf_set.all().order_by('-book_add_date')[0:bookNumber]
			for bookOnShelf in bookonshelfs:
				result = {'bookId': bookOnShelf.bookId}
				location = bookOnShelf.bookLocation
				result['location'] = location.__unicode__()
				result['state'] = bookOnShelf.state
				results.append(result)
			return render(request, 'stack/book/book_detail_t_stack.html', {'results': results, 'bookInfo': bookInfo ,'account':account})	


	
'''
张凯
'''

#get the root dir

import logging
from subprocess import Popen,PIPE

host = "127.0.0.1"
usr = "root"
passwd = "ilovepavo2016!"
dbname = "pavo"
currnetdir = os.getcwd()
parent = os.path.dirname(currnetdir)
bakroot = os.path.join(parent,"backup")

#展示页面结果
def backup_restore(request):

	if request.session.get('accounttype', default =None) == 'Admin':

		currentuser = request.session.get('account',default=None)
		recordobjectlist = BackupRecords.objects.all()
		max = 0
		for object in recordobjectlist:
			if object.recordId > max:
				max = object.recordId
		records = BackupRecords.objects.filter(recordId = max)
		pageContent = paginate(request, records, 'records', 8)
		pageContent.update({'account':currentuser})
		return render(request,'admin/backup_list.html',pageContent)
	else:
		return HttpResponseRedirect('/login/')

#list the backup files-list
#|operator|filename|operatetime|filesize|
#

def subcmd(cmd,timeStr,bakfile,operatetype):
	try:
		process = Popen('%s'  %(cmd), stdout=PIPE, stdin=PIPE, shell=True)
		output = process.communicate()
		flag = 1;
		loginfo(timeStr,flag,bakfile,operatetype)
	except MySQLdb.Error,e:
		flag = 0;
		loginfo(timeStr,flag,bakfile,operatetype)


def loginfo(timestr,flag,bakfile,operatetype):
	path = bakroot
	logfile = os.path.join(path,"loginfo.log")
	logging.basicConfig(filename = logfile,level = logging.INFO)
	if flag:
		logging.info('[' + timestr + ']' + ' ' + operatetype +' was Successful!' + bakfile)
	else:
		logging.error('[' + timestr + ']' + ' ' + operatetype +' was Wrong!' + bakfile)

def backup():
	nowTime = time.localtime()
	timeStr = str(nowTime.tm_year)+"-"+str(nowTime.tm_mon)+"-"+str(nowTime.tm_mday)+"-"+str(nowTime.tm_hour)+"-"+str(nowTime.tm_min)+"-"+str(nowTime.tm_sec)
	bakname = "dbbackup"+"-"+ timeStr + str(time.time()) + ".sql"
	bakfile = os.path.join(bakroot,bakname)
	cmd = "mysqldump -u" + usr + " -p" + passwd + " " + dbname + " > " + bakfile 
	subcmd(cmd,timeStr,bakfile,"Backup")
	bakfilesize = os.path.getsize(bakfile)/1024
	fileinfo = {'bakname':bakname,'bakfilesize':bakfilesize,'location':bakroot}
	return fileinfo

def backup_record(request):#备份和记录信息

	fileinfo = backup()#备份
	bakname = fileinfo['bakname']
	bakfilesize = fileinfo['bakfilesize']
	backupDir = fileinfo['location']
	currentuser = request.session.get('account',default=None)
	if currentuser == None:
		return HttpResponseRedirect('/login/')
	else:
		#currentoperator = get_object_or_404(Admin,currentuser)
		currentoperator = Admin.objects.filter(account = currentuser)
		for currentoperator in currentoperator:
			backupRecord = BackupRecords(operator=currentoperator,operateTime=timezone.now(),fileName=bakname,fileSize=bakfilesize,location=backupDir)
			backupRecord.save()
		return redirect('LMS.views.backup_restore')

def restoredb(fileinfo):
	fileName = fileinfo['fileName']
	bakdir = bakroot
	bakfile = os.path.join(bakdir,fileName)
	nowTime = time.localtime()
	timeStr = str(nowTime.tm_year)+"-"+str(nowTime.tm_mon)+"-"+str(nowTime.tm_mday)+"-"+str(nowTime.tm_hour)+"-"+str(nowTime.tm_min)+"-"+str(nowTime.tm_sec)
	#submit command
	cmd = "mysql -u" + usr + " -p" + passwd + " " + dbname + " < " + bakfile
	subcmd(cmd,timeStr,bakfile,"Restore")
	return True

def restore(request,pk):#恢复
	record = get_object_or_404(BackupRecords,pk=pk)
	if record:
		bakfile = record.fileName
		fileinfo = {'fileName':bakfile}
		flag = restoredb(fileinfo)
	else:
		flag = False
	return redirect('LMS.views.backup_restore')

def delete_dbfile(fileinfo):#删除备份文件
	bakdir = bakroot
	bakfile = os.path.join(bakdir,fileinfo['fileName'])
	os.remove(bakfile)
	return True

def delete_backup(request,pk):#删除
	record = get_object_or_404(BackupRecords,pk=pk)
	bakfile = record.fileName
	fileinfo = {'fileName':bakfile}
	if record:
		flag = delete_dbfile(fileinfo)
		record.delete()
	else:
		flag = False
	return redirect('LMS.views.backup_restore')

def print_barcode_admin(request):
	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)
	values = request.POST.getlist('bccb')
	if values:
		return render(request,'admin/book/book_barcode_list.html',{"values":values, 'account':account})
	else:
		return redirect('LMS.views.book_list')

def print_barcode_stack(request):
	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)
	values = request.POST.getlist('bccb')
	if values:
		return render(request,'stack/book_barcode_list.html',{"values":values, 'account':account})
	else:
		return redirect('LMS.views.book_list_stack')

def print_barcode_stack_t(request):
	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)
	values = request.POST.getlist('bccb')
	if values:
		return render(request,'stack/book/book_barcode_list_t.html',{"values":values, 'account':account})
	else:
		return redirect('LMS.views.book_detail_t')

def print_barcode_t(request):
	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)
	values = request.POST.getlist('bccb')
	if values:
		return render(request,'admin/book/book_barcode_list.html',{"values":values, 'account':account})
	else:
		return redirect('LMS.views.book_detail_t')

def dosearch_booklist_print(request):
	
	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)
	if accounttype != 'Admin':
		return HttpResponseRedirect('/login/')
	else:
		if request.method == 'POST':
			values = request.POST.getlist('bccb')
			if values:
				return render(request,'admin/book/book_barcode_list.html',{"values":values, 'account':account})
			else:
				return HttpResponseRedirect('/book_list/')
		else:
			return HttpResponseRedirect('/book_list/')

def dosearch_booklist_print_stack(request):
	
	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)
	if accounttype != 'StackLibrarian':
		return HttpResponseRedirect('/login/')
	else:
		if request.method == 'POST':
			values = request.POST.getlist('bccb')
			if values:
				return render(request,'admin/book/book_barcode_list.html',{"values":values, 'account':account})
			else:
				return HttpResponseRedirect('/book_list_stack/')
		else:
			return HttpResponseRedirect('/book_list_stack/')

'''
FrontDeskLibrarian端
'''

def frontIndex(request):

	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)
	if accounttype != 'FrontDeskLibrarian':
		return HttpResponseRedirect('/login/')
	else:
		transactionRecords = TransactionRecord.objects.all().order_by('-borrowedTime')
		limitPerPage=6
		paginator = Paginator(transactionRecords, limitPerPage)
		curPageNum = correctNum(request.GET.get('page', default=1), paginator.num_pages)
		try:
			curPageRecords = paginator.page(curPageNum)
		except PageNotAnInteger:
			curPageRecords = paginator.page(1)
		except EmptyPage:
			curPageRecords = paginator.page(paginator.num_pages)
		pageList = page_num_list(curPageNum, paginator.num_pages)
		
		if request.method == "POST":
			lendBookForm = LendBookForm(request.POST)
			if lendBookForm.is_valid():
				lendBook = BookOnShelf.objects.get(bookId=lendBookForm.cleaned_data['bookId'])
				if lendBook.get_state_display() == 'in':
					lendMember = Member.objects.get(account=lendBookForm.cleaned_data['memberId'])
					if request.POST.get('OK') == 'False':
						return transaction_book_detail("Lend", request, lendBook, lendMember, lendBookForm)
					operator = FrontDeskLibrarian.objects.get(account = request.session.get('account', default = None))
					saveLend(lendMember, lendBook, operator)
					return redirect('LMS.views.lend_book')
		else:
			lendBookForm = LendBookForm()
			#get account
			account = request.session.get('account', default = None)
		return render(request, 'front/lend_and_return.html', {'pageCount':paginator.num_pages,'pageList':pageList, 'isReturnBook':False, 'curPageRecords':curPageRecords, 'bookForm':lendBookForm, 'account':account,'accounttype':accounttype})

		#return render(request, 'front/lend_and_return.html', {'account': account})
		

#显示front_student列表
def front_student_list(request):

	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)
	
	if accounttype != 'FrontDeskLibrarian':
		return HttpResponseRedirect('/login/')
	else:
		posts = []
		#posts = Member.objects.filter(member_add_date__lte=timezone.now()).order_by('-member_add_date')
		posts1 = Member.objects.filter(type = 'undergraduate').order_by('-member_add_date')
		posts2 = Member.objects.filter(type = 'postgraduate').order_by('-member_add_date')
		posts.extend(posts1)
		posts.extend(posts2)
		pageContent = paginate(request, posts, 'posts', 8)
		pageContent.update({'account':account})
		return render(request, 'front/student/front_student_list.html', pageContent)

#搜索front_student
def dosearch_front_studentlist(request):

	account = request.session.get('account', default = None)

	if account == None:
		return HttpResponseRedirect('/login/')
	else:
		if request.method == 'GET':
			if  ('select' in request.GET) and ('keyword' in request.GET):

				select = request.GET['select'] # returns a string
				keyword = request.GET['keyword']
				#*********define a list containing dicts*********
				results = []
				#search in table BooKInfo, Publishing House,according to 'select'
				###seachResults ---booklist from table BookInfo
				# integer or string
				select = int(select)
				if select == 1:
					studentlist = Member.objects.filter(account = keyword)
				else:
					studentlist = Member.objects.filter(name__contains = keyword)
				for student in studentlist:
					if student.type == 'undergraduate' or student.type == 'postgraduate':
						result = {'account':student.account, 'name':student.name,
						'type':student.type,'school':student.school,'classNo':student.classNo,'major':student.major,
						'bookOwning':student.bookOwning,'debt':student.debt,'member_add_date':student.member_add_date}
						#add result to results
						results.append(result)
				if len(results) == 0:
					empty_message = u'No student found'
					return render(request, 'front/student/front_studentlist_search.html', {'empty_message': empty_message,'account':account})
				pageContent = paginate(request, results, 'results', 8, ['select', 'keyword'])
				pageContent.update({'account':account})
				return render(request, 'front/student/front_studentlist_search.html', pageContent)
			else:
				return render(request, 'front/student/front_student_list.html', {})
		else:
			return render(request, 'front/student/front_student_list.html', {})

#详情front_student
def front_studentlist_detail(request,account):

	account1 = request.session.get('account', default = None)
	if account1 == None:
		return HttpResponseRedirect('/login/')
	else:
		student = get_object_or_404(Member, account=account)
		if not student.photo:
			student.photo = '/static/photo/nophoto.png'
		return render(request,'front/student/front_studentlist_detail.html',{'student':student, 'account1':account1})

def front_student_detail(request,pk):

	account = request.session.get('account', default = None)
	if account == None:
		return HttpResponseRedirect('/login/')
	else:
		posts = get_object_or_404(Member, pk=pk)
		if not posts.photo:
			posts.photo = '/static/photo/nophoto.png'
		return render(request,'front/student/front_student_detail.html',{'posts':posts, 'account': account})

#显示front_faculty
def front_faculty_list(request):

	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)

	if accounttype != 'FrontDeskLibrarian':
		return HttpResponseRedirect('/login/')
	else:
		posts = Member.objects.filter(type = 'faculty').order_by('-member_add_date')
		pageContent = paginate(request, posts, 'posts', 8)
		pageContent.update({'account':account})
		return render(request, 'front/faculty/front_faculty_list.html', pageContent)

def dosearch_front_facultylist(request):

	account = request.session.get('account', default = None)
	if account == None:
		return HttpResponseRedirect('/login/')
	else:
		if request.method == 'GET':
			if('select' in request.GET) and ('keyword' in request.GET):
				select = request.GET['select'] # returns a string
				keyword = request.GET['keyword']
				#*********define a list containing dicts*********
				results = []
				#search in table BooKInfo, Publishing House,according to 'select'
				###seachResults ---booklist from table BookInfo
				select = int(select)
				if select == 1:
					facultylist = Member.objects.filter(account = keyword)
				else:
					facultylist = Member.objects.filter(name__contains = keyword)
				for faculty in facultylist:
					if faculty.type == 'faculty':
						result = {'account':faculty.account, 'name':faculty.name,'bookOwning':faculty.bookOwning,
						'member_add_date':faculty.member_add_date,'type':faculty.type}
						#add result to results
						results.append(result)
				if len(results) == 0:
					empty_message = u'No faculty found'
					return render(request, 'front/faculty/front_facultylist_search.html', {'empty_message': empty_message,'account':account})
				pageContent = paginate(request, results, 'results', 8, ['select', 'keyword'])
				pageContent.update({'account':account})

				return render(request, 'front/faculty/front_facultylist_search.html', pageContent)
			else:
				return render(request, 'front/faculty/front_faculty_list.html', {})
		else:
			return render(request, 'front/faculty/front_faculty_list.html', {})

#详情front_faculty
def front_facultylist_detail(request,account):

	account1 = request.session.get('account', default = None)
	if account1 == None:
		return HttpResponseRedirect('/login/')
	else:
		faculty = get_object_or_404(Member, account=account)
		if not faculty.photo:
			faculty.photo = '/static/photo/nophoto.png'
        return render(request,'front/faculty/front_facultylist_detail.html',{'faculty':faculty, 'account1':account1})

def front_faculty_detail(request,pk):

	account = request.session.get('account', default = None)
	if account == None:
		return HttpResponseRedirect('/login/')
	else:
		posts = get_object_or_404(Member, pk=pk)
        if not posts.photo:
            posts.photo = '/static/photo/nophoto.png'
        return render(request,'front/faculty/front_faculty_detail.html',{'posts':posts, 'account':account})

#FrontInfo
def frontInfo(request):

	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)

	if accounttype != 'FrontDeskLibrarian':
		return HttpResponseRedirect('/login/')
	else:
		results = []
		frontlist = FrontDeskLibrarian.objects.filter(account = account)
		for front in frontlist:
			if not front.photo:
				front.photo = '/static/photo/nophoto.png' 
			result = {'account':front.account, 'name':front.name,'password':front.password,'gender':front.gender,'tel':front.tel,'photo':front.photo,'front_add_date':front.front_add_date}
			results.append(result)


		return render(request, 'front/front_detail.html', {'results':results,'account':account})

def frontInfoChangePassword(request):

	account = request.session.get('account', default = None)
	if account == None:
		return HttpResponseRedirect('/login/')
	else:
		return render(request, 'front/front_detail_changepassword.html', {'account': account})

def do_changepassword_front(request):

	oldpassword = request.POST['oldpassword']
	newpassword = request.POST['newpassword1']

	account = request.session.get('account', default = None)
	if account == None:
		return HttpResponseRedirect('/login/')
	else:
		front = FrontDeskLibrarian.objects.get(account = account)
		#判断老密码是否合法
		if oldpassword == front.password:
			front.password = newpassword
			front.save()
			return HttpResponseRedirect('/frontInfo/')
		else:
			error_message = u'old password is wrong'
			return render_to_response('front/front_detail_changepassword.html', {'error_message': error_message,'account': account})
			

'''
浩洋
'''

def transaction_book_detail(operatorType, request, book, member, bookForm):
	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default= None)
	if accounttype != 'FrontDeskLibrarian':
		return HttpResponseRedirect('/login/')
	
	if not member.photo:
		member.photo = '/static/photo/nophoto.png' 
	if operatorType == "Return":
		isReturn = "True"
	else:
		isReturn = "False"
	return render(request,'front/transaction_confirm.html',{'isReturn':isReturn, 'book':book, 'member':member, 'account':account, 'bookForm':bookForm})
	
	
def page_num_list(curPageNum, pageCount):
	curPageNum = int(curPageNum)
	pageCount = int(pageCount)
	if (curPageNum > 6):
		left = curPageNum-5
	else:
		left = 1
	if (pageCount-curPageNum) > 6:
		right = curPageNum+6
	else:
		right = pageCount
	list = range(left, right+1)
	return list
	
	
def correctNum(curPage, pageCount):
	curPage = int(curPage)
	if curPage > pageCount:
		curPage = pageCount
	elif curPage < 1:
		curPage = 1
	return curPage
	
	
def saveLend(lendMember, lendBook, operator):
	transactionRecord = TransactionRecord(member=lendMember, bookOnShelf=lendBook)
	transactionRecord.borrowOperator = operator
	transactionRecord.borrowedTime = timezone.now()
	transactionRecord.id = str(transactionRecord.bookOnShelf) + str(transactionRecord.borrowedTime.strftime('%Y%m%d%H%M%S'))
	lendBook.state = 'out'
	transactionRecord.member.bookOwning += 1
	transactionRecord.member.save()
	lendBook.save()
	transactionRecord.save()
	return None
	
	
def saveReturn(returnBookRecord, lendMember, returnBook, operator):
	returnBookRecord.returnOperator = operator
	returnBookRecord.returnedTime = timezone.now()
	returnBook.state = 'in'
	overDays = (returnBookRecord.returnedTime-returnBookRecord.dueTime()).days
	if overDays > 0:
		returnBookRecord.member.debt += Decimal(overDays*0.1)
	returnBookRecord.member.bookOwning -= 1
	returnBookRecord.member.save()
	returnBook.save()
	returnBookRecord.save()
	return None
	
def paginate(request, source, sourceName, limitPrePage, searchValues = None):
	paginator = Paginator(source, limitPrePage)
	curPageNum = correctNum(request.GET.get('page', default=1), paginator.num_pages)	
	try:
		curPageRecords = paginator.page(curPageNum)
	except PageNotAnInteger:
		curPageRecords = paginator.page(1)
	except EmptyPage:
		curPageRecords = paginator.page(paginator.num_pages)
	pageList = page_num_list(curPageNum, paginator.num_pages)
	page = {'pageCount':paginator.num_pages, 'pageList':pageList, str(sourceName):curPageRecords, 'curPage':curPageRecords}
	if not searchValues is None and isinstance(searchValues, list):
		searchDict = {}
		for value in searchValues:
			searchDict[str(value)] = request.REQUEST.get(str(value),None)
		page['searchDict'] = searchDict
	return page
	
def lend_book(request):
	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default= None)
	if accounttype != 'FrontDeskLibrarian':
		return HttpResponseRedirect('/login/')
	
	if request.method == "POST":
		lendBookForm = LendBookForm(request.POST)
		if lendBookForm.is_valid():
			lendBook = BookOnShelf.objects.get(bookId=lendBookForm.cleaned_data['bookId'])
			if lendBook.get_state_display() == 'in':
				lendMember = Member.objects.get(account=lendBookForm.cleaned_data['memberId'])
				if request.POST.get('OK') == 'False':
					return transaction_book_detail("Lend", request, lendBook, lendMember, lendBookForm)
				operator = FrontDeskLibrarian.objects.get(account = request.session.get('account', default = None))
				saveLend(lendMember, lendBook, operator)
				return redirect('LMS.views.lend_book')
	else:
		lendBookForm = LendBookForm()
		#get account
	account = request.session.get('account', default = None)
	transactionRecords = TransactionRecord.objects.all().order_by('-borrowedTime')
	pageContent = paginate(request, transactionRecords, 'curPageRecords', 6)
	pageContent.update({'isReturnBook':False, 'bookForm':lendBookForm, 'account':account})
	return render(request, 'front/lend_and_return.html', pageContent)



	
def return_book(request):
	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)
	if accounttype != 'FrontDeskLibrarian':
		return HttpResponseRedirect('/login/')
	
	if request.method == "POST":
		returnBookForm = ReturnBookForm(request.POST)
		if returnBookForm.is_valid():
			returnBook = BookOnShelf.objects.get(bookId = returnBookForm.cleaned_data['bookId'])
			if returnBook.get_state_display() == 'out':
				returnBookRecord = TransactionRecord.objects.filter(returnedTime = None).get(bookOnShelf = returnBook)
				lendMember = Member.objects.get(account=returnBookRecord.member)
				if request.POST.get('OK') == 'False':
					return transaction_book_detail("Return", request, returnBook, lendMember, returnBookForm)
				operator = FrontDeskLibrarian.objects.get(account = request.session.get('account', default = None))
				saveReturn(returnBookRecord, lendMember, returnBook, operator)
			return redirect('LMS.views.return_book')
	else:
		returnBookForm = ReturnBookForm()
		#get account
	account = request.session.get('account', default = None)
	transactionRecords = TransactionRecord.objects.exclude(returnedTime = None).order_by('-returnedTime')
	pageContent = paginate(request, transactionRecords,'curPageRecords', 6)
	pageContent.update({'isReturnBook':True, 'bookForm':returnBookForm, 'account':account})
	return render(request, 'front/lend_and_return.html', pageContent)
	
	
	
def book_activity(request):
	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)
	if accounttype != 'FrontDeskLibrarian':
		return HttpResponseRedirect('/login/')
	
	if request.REQUEST.get('bookId',None)==None:
		bookForm = BookFormZHY()
		return render(request, 'front/book_activity.html', {'bookForm':bookForm, 'account': account})
	else:
		bookForm = BookFormZHY(request.GET)
		if bookForm.is_valid():
			queriedBook = BookOnShelf.objects.get(bookId = bookForm.cleaned_data['bookId'])
			queriedBookRecords=TransactionRecord.objects.filter(bookOnShelf = queriedBook).exclude(returnedTime = None).order_by('-returnedTime')
			pageContent = paginate(request, queriedBookRecords, 'queriedBookRecords', 4, ['bookId'])
			isOut = queriedBook.get_state_display() == 'out'
			if isOut:
				queriedBookOutRecord=TransactionRecord.objects.filter(bookOnShelf = queriedBook).get(returnedTime = None)
			else: 
				queriedBookOutRecord=None
			pageContent.update({'book':queriedBook, 'isOut':isOut, 'queriedBookOutRecord':queriedBookOutRecord, 'bookForm':bookForm, 'account': account})
			return render(request,'front/book_activity.html',pageContent)
	return render(request, 'front/book_activity.html', {'bookForm':bookForm, 'account': account})


def member_activity(request):
	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)
	if accounttype != 'FrontDeskLibrarian':
		return HttpResponseRedirect('/login/')
	
	if request.REQUEST.get('memberId',None)==None:
		memberForm = MemberForm()
		return render(request, 'front/member_activity.html', {'memberForm':memberForm, 'account': account})
	else:
		memberForm = MemberForm(request.GET)
		if memberForm.is_valid():
			queriedMember = Member.objects.get(account = memberForm.cleaned_data['memberId'])
			historyBorrows=TransactionRecord.objects.filter(member = queriedMember).exclude(returnedTime = None).order_by('-returnedTime')
			currentBorrows=TransactionRecord.objects.filter(member = queriedMember).filter(returnedTime = None).order_by('-borrowedTime')
			pageContent = paginate(request, historyBorrows, 'historyBorrows', 4, ['memberId'])

			if not queriedMember.photo:
				queriedMember.photo = '/static/photo/nophoto.png'
			pageContent.update({'member':queriedMember, 'currentBorrows':currentBorrows, 'memberForm':memberForm, 'account': account})
			return render(request,'front/member_activity.html',pageContent)
	return render(request, 'front/member_activity.html', {'memberForm':memberForm, 'account': account})






# Member 端

def member_my_activity(request):
		
		accounttype = request.session.get('accounttype', default = None)
		account = request.session.get('account', default = None)
		if accounttype != 'student' and accounttype != 'faculty':
			return HttpResponseRedirect('/login/')
		
		queriedMember = Member.objects.get(account = account)
		historyBorrows=TransactionRecord.objects.filter(member = queriedMember).exclude(returnedTime = None).order_by('-returnedTime')
		currentBorrows=TransactionRecord.objects.filter(member = queriedMember).filter(returnedTime = None).order_by('-borrowedTime')
		pageContent = paginate(request, historyBorrows, 'historyBorrows', 4)
		if not queriedMember.photo:
			queriedMember.photo = '/static/photo/nophoto.png'
		pageContent.update({'member':queriedMember, 'currentBorrows':currentBorrows,'accounttype': accounttype, 'account': account})
		return render(request,'member/member_my_activity.html',pageContent)


def memberInfo(request):
	
	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)

	if accounttype != 'student' and accounttype != 'faculty':
		return HttpResponseRedirect('/login/')
	else:
		results = []
		
		#retrieve member(stu / faculty) on table Member 
		#Student or Faculty

		if accounttype == 'student':
			students = Member.objects.filter(account = account)
			for student in students:
				if not student.photo:
					student.photo = '/static/photo/nophoto.png' 
				result = {'account':student.account, 'name':student.name, 'school': student.school, 'major': student.major,'studenttype': student.type,'password':student.password,'gender':student.gender,'tel':student.tel,'photo':student.photo,'member_add_date':student.member_add_date}
				results.append(result)
			return render(request, 'member/member_detail.html', {'results':results, 'accounttype': accounttype, 'account':account})
		
		else:
			faculties = Member.objects.filter(account = account)
			for faculty in faculties:
				if not faculty.photo:
					faculty.photo = '/static/photo/nophoto.png' 
				result = {'account':faculty.account, 'name':faculty.name,'password':faculty.password,'school':faculty.school,'gender':faculty.gender,'tel':faculty.tel,'photo':faculty.photo,'member_add_date':faculty.member_add_date}
				results.append(result)
			return render(request, 'member/member_detail.html', {'results':results, 'accounttype': accounttype, 'account':account})


def MemberInfoChangePassword(request):

	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)

	if accounttype == None or account == None:
		return HttpResponseRedirect('/login/')
	else:
		return render(request, 'member/member_detail_changepassword.html', {'accounttype': accounttype, 'account': account})

def do_changepassword_member(request):

	oldpassword = request.POST['oldpassword']
	newpassword = request.POST['newpassword1']

	accounttype = request.session.get('accounttype', default = None)
	account = request.session.get('account', default = None)

	if accounttype == None or account == None:
		return HttpResponseRedirect('/login/')
	else:
		# Student or Faculty changes password
		if accounttype == 'Student':

			student = Member.objects.get(account = account)
			#判断老密码是否合法
			if oldpassword == student.password:
				student.password = newpassword
				student.save()
				return HttpResponseRedirect('/memberInfo/')
			else:
				error_message = u'old password is wrong'
				return render_to_response('member/member_detail_changepassword.html', {'error_message': error_message,'account': account,'accounttype':accounttype})
		else:
			faculty = Member.objects.get(account = account)
			#判断老密码是否合法
			if oldpassword == faculty.password:
				faculty.password = newpassword
				faculty.save()
				return HttpResponseRedirect('/memberInfo/')
			else:
				error_message = u'old password is wrong'
				return render_to_response('member/member_detail_changepassword.html', {'error_message': error_message,'account': account,'accounttype':accounttype})
