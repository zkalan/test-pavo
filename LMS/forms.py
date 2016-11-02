#coding:utf-8
from django import forms
from .models import BookInfo,Catagory,BookLocation,PublishingHouse,BookOnShelf,TransactionRecord,Admin,FrontDeskLibrarian,StackLibrarian,Member

class AdminForm(forms.ModelForm):
	class Meta:
		model = Admin
		fields = ('password',)
class BookForm(forms.ModelForm):
	'''
	FLOOR = (
		('1L', '1L'),
		('2L', '2L'),
		('3L', '3L'),
		('4L', '4L'),
		('5L', '5L'),
	)
	floor = forms.CharField(max_length = 10, choices = FLOOR, default = '1L')
	'''
	class Meta:
		model = BookOnShelf
		fields = ()
class StudentForm(forms.ModelForm):
	dueDate = forms.DateField(label=(u'DueDate:(Date format likes "2016-10-01")'))
	class Meta:
		model = Member
		fields =('name','gender','tel','photo','school','type','major','classNo','dueDate','maxBorrowedBooks','availableDays','debt',)
class StudentForm_add(forms.ModelForm):

	password = forms.CharField(widget=forms.PasswordInput, max_length = 30)
	dueDate = forms.DateField(label=(u'DueDate:(Date format likes "2016-10-01")'))
	class Meta:
		model = Member
		fields =('account','password','name','gender','tel','photo','school','type','major','classNo','dueDate','maxBorrowedBooks','availableDays','debt',)
class FacultyForm(forms.ModelForm):
	dueDate = forms.DateField(label=(u'DueDate:(Date format likes "2016-10-01")'))
	class Meta:
		model = Member
		fields =('gender', 'name', 'tel','photo','school','dueDate','maxBorrowedBooks','availableDays','debt',)
class FacultyForm_add(forms.ModelForm):

	dueDate = forms.DateField(label=(u'DueDate:(Date format likes "2016-10-01")'))
	password = forms.CharField(widget=forms.PasswordInput, max_length = 30)

	class Meta:
		model = Member
		fields =('account','password','name','gender','tel','photo','school','dueDate','maxBorrowedBooks','availableDays','debt',)
class FrontForm(forms.ModelForm):
	class Meta:
		model = FrontDeskLibrarian
		fields =('name','gender','tel','photo',)
class FrontForm_add(forms.ModelForm):

	password = forms.CharField(widget=forms.PasswordInput, max_length = 30)
	class Meta:
		model = FrontDeskLibrarian
		fields =('account','password','name','gender','tel','photo',)
class StacktForm(forms.ModelForm):
	class Meta:
		model = StackLibrarian
		fields =('name','gender','tel','photo',)
class StacktForm_add(forms.ModelForm):

	password = forms.CharField(widget=forms.PasswordInput, max_length = 30)
	class Meta:
		model = StackLibrarian
		fields =('account','password','name','gender','tel','photo',)


class CommentForm(forms.Form):
	name = forms.CharField(widget=forms.TextInput(attrs={'class':'special'}))
	url = forms.URLField()
	comment = forms.CharField(widget=forms.TextInput(attrs={'size':'40'}))


'''zhanghaoyang'''
class BookFormZHY(forms.Form):
	bookId = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'id':'bookId', 'placeholder':'BookID'}))
	
	def clean_bookId(self):
		cleanBookId=self.cleaned_data['bookId']
		if not cleanBookId.isdigit():
			raise forms.ValidationError(u"please input num.")
			return cleanBookId
		if len(cleanBookId) < 7:
			raise forms.ValidationError(u"too short.")
			return cleanBookId
		is_exist=BookOnShelf.objects.filter(bookId=cleanBookId).exists()
		if not is_exist:
			raise forms.ValidationError(u"no this book.")
			
		return cleanBookId

class MemberForm(forms.Form):
	
	# MEMBERTYPE = (
		# ('male', 'male'),
		# ('female', 'female'),
	# )
	
	memberId = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class':'form-control', 'id':'memberId', 'placeholder':'MemberID'}))
	def clean_memberId(self):
		cleanMemberId=self.cleaned_data['memberId']
		for char in cleanMemberId:
			if char.isspace():
				raise forms.ValidationError(u"don't space.")
				return cleanMemberId
		is_exist=Member.objects.filter(account=cleanMemberId).exists()
		if not is_exist:
			raise forms.ValidationError(u"no this member.")
			return cleanMemberId
		lendMember = Member.objects.get(account=cleanMemberId)
		if not lendMember.isAlive():
			raise forms.ValidationError(u"overdue this member.")
		
		return cleanMemberId


class LendBookForm(BookFormZHY, MemberForm):
	def clean_bookId(self):
		cleanBookId=self.cleaned_data['bookId']
		if not cleanBookId.isdigit():
			raise forms.ValidationError(u"please input num.")
			return cleanBookId
		if len(cleanBookId) < 7:
			raise forms.ValidationError(u"too short.")
			return cleanBookId
		is_exist=BookOnShelf.objects.filter(bookId=cleanBookId).exists()
		if not is_exist:
			raise forms.ValidationError(u"no this book.")		
		is_out=(BookOnShelf.objects.get(bookId=cleanBookId).get_state_display() == 'out')
		if is_out:
			raise forms.ValidationError(u"had lend out.")
		return cleanBookId
		
	def clean_memberId(self):
		cleanMemberId=self.cleaned_data['memberId']
		for char in cleanMemberId:
			if char.isspace():
				raise forms.ValidationError(u"don't space.")
				return cleanMemberId
		is_exist=Member.objects.filter(account=cleanMemberId).exists()
		if not is_exist:
			raise forms.ValidationError(u"no this member.")
			return cleanMemberId
		lendMember = Member.objects.get(account=cleanMemberId)
		if not lendMember.isAlive():
			raise forms.ValidationError(u"overdue this member.")
		elif lendMember.isOverMaxLend():
			raise forms.ValidationError(u"too many lend.")
		elif lendMember.isOverMaxDebt():
			raise forms.ValidationError(u"debt too much.")
		return cleanMemberId

class ReturnBookForm(BookFormZHY):

	def clean_bookId(self):
		cleanBookId=self.cleaned_data['bookId']
		if not cleanBookId.isdigit():
			raise forms.ValidationError(u"please input num.")
			return cleanBookId
		if len(cleanBookId) < 7:
			raise forms.ValidationError(u"too short.")
			return cleanBookId
		is_exist=BookOnShelf.objects.filter(bookId=cleanBookId).exists()
		if not is_exist:
			raise forms.ValidationError(u"no this book.")
			return cleanBookId
		returnBook = BookOnShelf.objects.get(bookId=cleanBookId)
		hasLendRecord = TransactionRecord.objects.filter(returnedTime = None).filter(bookOnShelf = returnBook).exists()
		is_in = (BookOnShelf.objects.get(bookId=cleanBookId).get_state_display() == 'in')
		if not hasLendRecord:
			if not is_in:
				raise forms.ValidationError(u"no lend record.")
			else:
				raise forms.ValidationError(u"had not lend out.")
				return cleanBookId
		if is_in:
			raise forms.ValidationError(u"had return in.")
		return cleanBookId

