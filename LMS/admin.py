from django.contrib import admin
from .models import BookInfo,Catagory,BookLocation,PublishingHouse,BookOnShelf,TransactionRecord,Admin,FrontDeskLibrarian,StackLibrarian, Member, BackupRecords

# Register your models here.
admin.site.register(BookInfo)
admin.site.register(Catagory)
admin.site.register(BookLocation)
admin.site.register(PublishingHouse)
admin.site.register(BookOnShelf)
admin.site.register(TransactionRecord)
admin.site.register(Admin)
admin.site.register(FrontDeskLibrarian)
admin.site.register(StackLibrarian)
admin.site.register(Member)
admin.site.register(BackupRecords)