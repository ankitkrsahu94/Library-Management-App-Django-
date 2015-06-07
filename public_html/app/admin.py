from django.contrib import admin
from app.models import *
# Register your models here.

class MemberAdmin(admin.ModelAdmin):
	list_display = ('user','contactNo','member_since','membership_type','hasBooks','request','verified')

class BookAdmin(admin.ModelAdmin):
	list_display = ('title','isbn','author','pub_date','category','available')

class IssueAdmin(admin.ModelAdmin):
	list_display = ('isbn','user_id','issue_date','due_date','fine','status')
admin.site.register(Book,BookAdmin)
admin.site.register(Member,MemberAdmin)
admin.site.register(Books_Issued,IssueAdmin)