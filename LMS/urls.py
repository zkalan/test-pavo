# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views
from pavo import settings

urlpatterns = [
	#曙光 登陆，搜索
	url(r'^$', views.searchIndex, name = 'searchIndex'),
	url(r'^search_lists/$', views.dosearch, name = 'search_lists'),

    url(r'^book_detail_w/(?P<ISBN>\S+)/$', views.book_detail_w, name = 'book_detail_w'),
    url(r'^login/$', views.login, name = 'login'),
	url(r'^logout/$', views.logout, name = 'logout'),

	# Member 端
	url(r'^member_my_activity/$', views.member_my_activity, name='member_my_activity'),
	url(r'^memberInfo/$', views.memberInfo, name = 'memberInfo'),
	url(r'^MemberInfoChangePassword/$', views.MemberInfoChangePassword, name = 'MemberInfoChangePassword'),
	url(r'^do_changepassword_member/$', views.do_changepassword_member, name = 'do_changepassword_member'),
	
	#唐波 Admin端
	#Book
	url(r'^adminIndex/$', views.book_list, name = 'adminIndex'),
	url(r'^book_list/$', views.book_list, name='book_list'),
	url(r'^dosearch_booklist/$', views.dosearch_booklist, name='dosearch_booklist'),
	url(r'^booklist_detail/(?P<bookId>\S+)/$', views.booklist_detail, name = 'booklist_detail'),
	url(r'^delete_booklist/(?P<bookId>\S+)/$', views.delete_booklist,name='delete_booklist'),
	url(r'^delete_book/(?P<pk>\S+)/$', views.delete_book,name='delete_book'),
	url(r'^book_detail/(?P<pk>\S+)/$', views.book_detail, name='book_detail'),
	url(r'^edit_book/(?P<pk>\S+)/edit/$', views.edit_book, name='edit_book'),
	url(r'^edit_book_admin/$', views.edit_book_admin,name='edit_book_admin'),
	url(r'^add_ISBN/$', views.add_ISBN, name='add_ISBN'),
	url(r'^search/$', views.getInfoFromDouban),
	url(r'^getInfo/$', views.getInfo,name='getInfo'),
	url(r'^book_detail_t/(?P<pk>\S+)/(?P<bookNumber>\S+)/$', views.book_detail_t, name='book_detail_t'),
	#Student
	url(r'^student_list/$', views.student_list, name='student_list'),
	url(r'^dosearch_studentlist/$', views.dosearch_studentlist, name='dosearch_studentlist'),
	url(r'^studentlist_detail/(?P<account>\S+)/$', views.studentlist_detail, name = 'studentlist_detail'),
	url(r'^delete_studentlist/(?P<account>\S+)/$', views.delete_studentlist,name='delete_studentlist'),
	url(r'^delete_student/(?P<pk>\S+)/$', views.delete_student,name='delete_student'),
	url(r'^student_detail/(?P<pk>\S+)/$', views.student_detail,name='student_detail'),
	url(r'^edit_student/(?P<pk>\S+)/edit/$', views.edit_student, name='edit_student'),
	url(r'^add_student/$', views.add_student, name='add_student'),
	#FrontDeskLibrarian
	url(r'^front_list/$', views.front_list, name='front_list'),
	url(r'^dosearch_frontlist/$', views.dosearch_frontlist, name='dosearch_frontlist'),
	url(r'^frontlist_detail/(?P<account>\S+)/$', views.frontlist_detail, name = 'frontlist_detail'),
	url(r'^delete_frontlist/(?P<account>\S+)/$', views.delete_frontlist,name='delete_frontlist'),
	url(r'^delete_front/(?P<pk>\S+)/$', views.delete_front,name='delete_front'),
	url(r'^front_detail/(?P<pk>\S+)/$', views.front_detail,name='front_detail'),
	url(r'^edit_front/(?P<pk>\S+)/edit/$', views.edit_front, name='edit_front'),
	url(r'^add_front/$', views.add_front, name='add_front'),
	#StackLibrarian
	url(r'^stack_list/$', views.stack_list, name='stack_list'),
	url(r'^dosearch_stacklist/$', views.dosearch_stacklist, name='dosearch_stacklist'),
	url(r'^stacklist_detail/(?P<account>\S+)/$', views.stacklist_detail, name = 'stacklist_detail'),
	url(r'^delete_stacklist/(?P<account>\S+)/$', views.delete_stacklist,name='delete_stacklist'),
	url(r'^delete_stack/(?P<pk>\S+)/$', views.delete_stack,name='delete_stack'),
	url(r'^stack_detail/(?P<pk>\S+)/$', views.stack_detail,name='stack_detail'),
	url(r'^edit_stack/(?P<pk>\S+)/edit/$', views.edit_stack, name='edit_stack'),
	url(r'^add_stack/$', views.add_stack, name='add_stack'),
	#Faculty
	url(r'^faculty_list/$', views.faculty_list, name='faculty_list'),
	url(r'^dosearch_facultylist/$', views.dosearch_facultylist, name='dosearch_facultylist'),
	url(r'^facultylist_detail/(?P<account>\S+)/$', views.facultylist_detail, name = 'facultylist_detail'),
	url(r'^delete_facultylist/(?P<account>\S+)/$', views.delete_facultylist,name='delete_facultylist'),
	url(r'^delete_faculty/(?P<pk>\S+)/$', views.delete_faculty,name='delete_faculty'),
	url(r'^faculty_detail/(?P<pk>\S+)/$', views.faculty_detail,name='faculty_detail'),
	url(r'^edit_faculty/(?P<pk>\S+)/edit/$', views.edit_faculty, name='edit_faculty'),
	url(r'^add_faculty/$', views.add_faculty, name='add_faculty'),
	#AdminInfo
	url(r'^adminInfo/$', views.adminInfo, name='adminInfo'),
	url(r'^adminInfoChangePassword/$', views.adminInfoChangePassword, name='adminInfoChangePassword'),
	url(r'^do_changepassword/$', views.do_changepassword, name='do_changepassword'),
	
	
	#浩洋 FrontDeskLibrarian端
    url(r'^frontIndex/$', views.lend_book, name = 'frontIndex'),	
	
	url(r'^lend_book/$', views.lend_book, name='lend_book'),
	url(r'^return_book/$', views.return_book, name='return_book'),
	url(r'^book_activity/$', views.book_activity, name='book_activity'),
	url(r'^member_activity/$', views.member_activity, name='member_activity'),

	
	#FrontStudent
	url(r'^front_student_list/$', views.front_student_list, name='front_student_list'),
	url(r'^dosearch_front_studentlist/$', views.dosearch_front_studentlist, name='dosearch_front_studentlist'),
	url(r'^front_studentlist_detail/(?P<account>\S+)/$', views.front_studentlist_detail, name = 'front_studentlist_detail'),
	url(r'^front_student_detail/(?P<pk>\S+)/$', views.front_student_detail,name='front_student_detail'),
	#FrontFaculty
	url(r'^front_faculty_list/$', views.front_faculty_list, name='front_faculty_list'),
	url(r'^dosearch_front_facultylist/$', views.dosearch_front_facultylist, name='dosearch_front_facultylist'),
	url(r'^front_facultylist_detail/(?P<account>\S+)/$', views.front_facultylist_detail, name = 'front_facultylist_detail'),
	url(r'^front_faculty_detail/(?P<pk>\S+)/$', views.front_faculty_detail,name='front_faculty_detail'),
	#FrontInfo
	url(r'^frontInfo/$', views.frontInfo, name='frontInfo'),
	url(r'^frontInfoChangePassword/$', views.frontInfoChangePassword, name='frontInfoChangePassword'),
	url(r'^do_changepassword_front/$', views.do_changepassword_front, name='do_changepassword_front'),

	#唐波 StackLibrarian端
	url(r'^stackIndex/$', views.book_list_stack, name = 'stackIndex'),
	url(r'^book_list_stack/$', views.book_list_stack, name='book_list_stack'),
	url(r'^dosearch_booklist_stack/$', views.dosearch_booklist_stack, name='dosearch_booklist_stack'),
	url(r'^booklist_detail_stack/(?P<bookId>\S+)/$', views.booklist_detail_stack, name = 'booklist_detail_stack'),
	url(r'^delete_booklist_stack/(?P<bookId>\S+)/$', views.delete_booklist_stack,name='delete_booklist_stack'),
	url(r'^delete_book_stack/(?P<pk>\S+)/$', views.delete_book_stack,name='delete_book_stack'),
	url(r'^book_detail_stack/(?P<pk>\S+)/$', views.book_detail_stack, name='book_detail_stack'),
	url(r'^edit_book_stack/(?P<pk>\S+)/edit/$', views.edit_book_stack, name='edit_book_stack'),
	url(r'^edit_book_stack_stack/$', views.edit_book_stack_stack,name='edit_book_stack_stack'),
	url(r'^add_ISBN_stack/$', views.add_ISBN_stack, name='add_ISBN_stack'),
	url(r'^search_stack/$', views.getInfoFromDouban_stack),
	url(r'^getInfo_stack/$', views.getInfo_stack,name='getInfo_stack'),
	url(r'^book_detail_t_stack/(?P<pk>\S+)/(?P<bookNumber>\S+)/$', views.book_detail_t_stack, name='book_detail_t_stack'),
	#StackInfo
	url(r'^stackInfo/$', views.stackInfo, name='stackInfo'),
	url(r'^stackInfoChangePassword/$', views.stackInfoChangePassword, name='stackInfoChangePassword'),
	url(r'^do_changepassword_stack/$', views.do_changepassword_stack, name='do_changepassword_stack'),
	

	

	#zhangkai

	url(r'^dosearch_booklist_print/$', views.dosearch_booklist_print, name='dosearch_booklist_print'),
	url(r'^dosearch_booklist_print_stack/$', views.dosearch_booklist_print_stack, name='dosearch_booklist_print_stack'),
	url(r'^backup_restore/$',views.backup_restore,name='backup_list'),
	url(r'^backup/$',views.backup_record,name='backup'),
    url(r'^restore/(?P<pk>\S+)/$', views.restore,name='restore'),
    url(r'^delete/(?P<pk>\S+)/$',views.delete_backup,name='delete'),


	url(r'^media/(?P<path>.*)', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}),
]