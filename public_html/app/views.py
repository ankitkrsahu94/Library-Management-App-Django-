from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from app.models import *
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,logout,login
from app.forms import *
import logging
from django.views.generic import *
#import datetime


default_context = {'type':'None'}

# Create your views here.

class Books(ListView):
	model = Book
	context_object_name = 'response'

class AdminBooks(Books):
	template_name = 'app/allbooks.html'

	
class UserBooks(Books):
	template_name = 'app/books.html'

class Users(ListView):
	model = Member
	context_object_name = 'response'
	template_name = 'app/allusers.html'


class IssueDetails(TemplateView):
	template_name = 'app/issued.html'

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(IssueDetails, self).get_context_data(**kwargs)
		
		#this alone is not sufficient as isbn field holds the title of the book
		#to overcome this problem filter out the books from book table with these titles
		response = Books_Issued.objects.filter(user_id=self.request.user.member)
		response = response.filter(issued=True)

		#response 1 variable will hold only those books which are issued to the current user
		#searching is done on title field
		#so create an empty list
		response1 = []

		#iterate over the response object and find all the associated books and insert them in the list
		#so now response1 object contains the list of the issued books
		for idx,x in enumerate(response):
			y = Book.objects.get(title=x.isbn)
			response1.insert(idx,y)
		
		response = response1
		context = {'response':response}
		#'''
		return context

class PendingDetails(TemplateView):
	template_name = 'app/pending.html'

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(PendingDetails, self).get_context_data(**kwargs)

		response = Books_Issued.objects.filter(user_id=self.request.user.member)
		response = response.filter(status='NA')

		response1 = []

		for idx,x in enumerate(response):
			y = Book.objects.get(title=x.isbn)
			response1.insert(idx,y)
		
		#assert False,response1[0].isbn
		response = response1
		#assert False,response[0].isbn
		context = {'response':response}
		
		return context


class AddBook(FormView):
    template_name = 'app/addBook.html'
    form_class = BookForm
    success_url = '../books/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        book_form = BookForm(data = self.request.POST)
        book = book_form.save(commit=False)
        book.save()
        return super(AddBook, self).form_valid(form)


class EditBook(TemplateView):
	template_name = 'app/book_edit_form.html'
	context_object_name = 'book'

	def get_context_data(self,**kwargs):
		context = super(EditBook, self).get_context_data(**kwargs)
		isbn = self.request.GET['isbn']
		book = Book.objects.get(isbn=isbn)
		#assert False,book.category
		context['book'] = book
		return context

	def post(self,request):
		oldisbn = request.POST['oldisbn']
		oldbook = Book.objects.get(isbn=oldisbn)

		oldbook.isbn = request.POST['isbn']
		oldbook.title = request.POST['title']
		oldbook.author = request.POST['author']
		oldbook.pub_date = request.POST['pub_date']
		oldbook.category = request.POST['category']
		oldbook.quantity = request.POST['quantity']
		oldbook.available = request.POST['available']
		oldbook.save()

		return HttpResponseRedirect('../books/')

class DeleteBook(TemplateView):

	def post(self,request):

		isbn = request.POST['isbn']
		x = Book.objects.get(isbn=isbn)
		x.delete()
		return HttpResponseRedirect('../books/')


class RequestIssue(TemplateView):
	message = ''
	template_name = 'app/user_profile.html'

	def get_context_data(self,**kwargs):
		context = super(RequestIssue, self).get_context_data(**kwargs)
		
		x = len(Books_Issued.objects.filter(user_id=self.request.user.member))
		#assert False,x
		if x == 5:
			message = 'Quota exceeded. Maximum 5 books can be issued on this account.'
		else:
			books = self.request.GET.getlist('books')
			y = len(books)
			#assert False,y
			if y == 0:
				message = 'Invalid Request. Select atleast 1 book.'

			elif x+y > 5:
				message = 'Quota exceeded. You can have only ' + str(x+y-5) + ' more book(s) issued.'
			
			else:
				message = 'Your request has been accepted and sent to admin for approval'
				result= ''
				for book in books:
					x = Book.objects.get(title = book)
					obj  = Books_Issued.objects.get_or_create(user_id = self.request.user.member,isbn=x)
					#assert False,obj
					obj[0].isbn = x
					obj[0].save()

		context = {'message':message}	#assert False,result
		return context



class AddUser(TemplateView):
	template_name = 'app/new_user.html'
	def get_context_data(self,**kwargs):
		context = super(AddUser, self).get_context_data(**kwargs)
		user_form = UserForm()
		profile_form = UserProfileForm()
		context = {'user_form':user_form,'profile_form':profile_form}
		return context 

	def post(self,request):
		user_form = UserForm(data = request.POST)
		profile_form = UserProfileForm(data = request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			profile = profile_form.save(commit=False)
			profile.user = user
			profile.save()

		return HttpResponseRedirect('../users/')


class DeleteUser(TemplateView):
	
	def post(self,request):
		u_name = request.POST['username']
		x = User.objects.get(username=u_name)
		x.delete()
		return HttpResponseRedirect('../users/')

class EditUser(TemplateView):
	template_name = 'app/user_edit_form.html'

	def get_context_data(self,**kwargs):
		context = super(EditUser, self).get_context_data(**kwargs)
		u_name = self.request.GET['username']
		#assert False,u_name
		x = User.objects.get(username=u_name)
		y = Member.objects.get(user=x)
		#assert False,y
		context = {'lib_user':x,'member':y}
		return context

	def post(self,request):
		oldusername = request.POST['oldusername']
		#assert False,oldusername
		olduser = User.objects.get(username=oldusername)

		olduser.username = request.POST['username']
		olduser.first_name = request.POST['first_name']
		olduser.last_name = request.POST['last_name']
		olduser.email = request.POST['email']

		olduser.save()

		oldmember = Member.objects.get(user=olduser)
		verified = request.POST['verified']
		#assert False,oldmember.user
		#assert False,verified
		if verified == 'T':
			oldmember.verified = True
		else:
			oldmember.verified = False
		#oldmember.dob = request.POST['dob']
		oldmember.contactNo = request.POST['contactNo']
		oldmember.save()
		#assert False,username
		return HttpResponseRedirect('../users/')

	
class MemberRegistration(TemplateView):
	template_name = 'app/register.html'

	def get_context_data(self,**kwargs):
		context = super(MemberRegistration, self).get_context_data(**kwargs)
		user_form = UserForm()
		profile_form = UserProfileForm()
		context = {'user_form':user_form,'profile_form':profile_form}

		return context

	def post(self,request):
		user_form = UserForm(data = request.POST)
		profile_form = UserProfileForm(data = request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			profile = profile_form.save(commit=False)
			profile.user = user
			profile.save()
			registered = True
			context = {'user_form':True}
			
		else:
			print user_form.errors, profile_form.errors

		if context['user_form'] == True:
			return HttpResponseRedirect('app/response_success/')


class Check(TemplateView):

	 def dispatch(self,request):
	 	if request.user.is_authenticated():
			if request.user.member.membership_type == 'A':
				return HttpResponseRedirect('../admin/home/')
			else:
				return HttpResponseRedirect('../user/home/')

		return HttpResponseRedirect('../login/')
	

class UserLogin(TemplateView):
	#template_name = 'app/login.html'
	
	def post(self,request):
		
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username = username, password = password)
		if user:
			if user.is_active:
				login(request,user)
				#assert False,user.username
				#return HttpResponseRedirect('../user_profile')
				member = request.user.member
				if member.membership_type == 'A':
					#return render_to_response('app/admin_profile.html',default_context,context)
					return HttpResponseRedirect('../admin/home/')
				else:
					if member.verified:
						return HttpResponseRedirect('../user/home/')
					else:
						logout(request)
						return HttpResponse('Your account is yet to be verified by Admin')
			else:
				return HttpResponse('Your Library account is disabled')

		else:
			print "Invalid login details:{0}, {1}".format(username,password)
			return HttpResponse('Invalid login details supplied')


		
class Logout(TemplateView):
	template_name = 'app/logout.html'
	def get_context_data(self,**kwargs):
		context = super(Logout, self).get_context_data(**kwargs)
		logout(self.request)
		return context



class Index(TemplateView):
	template_name = 'app/index.html'


class Admin(TemplateView):
	def dispatch(self,request):		
		if request.user.is_authenticated() == False:
			return HttpResponseRedirect('../../login/')
		else:
			if request.user.member.membership_type != 'A':
				logout(request.user)
				return HttpResponseRedirect('../../login/')
			
		return render_to_response('app/admin_profile.html',default_context,RequestContext(request))

class UserHome(TemplateView):
	
	def dispatch(self,request):		
		if request.user.is_authenticated() == False:
			return HttpResponseRedirect('../../login/')
		else:
			if request.user.member.membership_type != 'U':
				logout(request.user)
				return HttpResponseRedirect('../../login/')
			
		return render_to_response('app/user_profile.html',default_context,RequestContext(request))


class ProcessRequests(TemplateView):
	#model = Books_Issued
	template_name = 'app/requests.html'
	context_object_name = 'response'
	#assert False,User.objects.get(username='ankit')
	
	def get_context_data(self,**kwargs):
		context = super(ProcessRequests, self).get_context_data(**kwargs)
		response = Books_Issued.objects.filter(issued=False)
		#assert False, response[0].id
		response1= []

		for idx,x in enumerate(response):
			y = Book.objects.get(title=x.isbn)
			response1.insert(idx,y)
		
		response = zip(response,response1)
		context = {'response':response}
		
		return context

class DiscardRequest(TemplateView):

	def post(self,request):
		id = request.POST['id']
		#isbn = str(isbn)
		#assert False,id
		x = Books_Issued.objects.filter(id=id)
		#assert False,x.isbn
		x.delete()
		return HttpResponseRedirect('../process_requests/')

class ApproveRequest(TemplateView):

	def post(self,request):
		id = request.POST['id']
		#assert False,id
		x = Books_Issued.objects.get(id=id)
		#assert False,x
		x.issued = True
		x.status = 'RP'
		x.save()
		return HttpResponseRedirect('../process_requests/')



class ResponseSuccess(TemplateView):
	template_name = 'app/response_success.html'