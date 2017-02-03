
from django.shortcuts import render, redirect, HttpResponse
from . models import User, Quote, Favorite
from django.contrib import messages


# Create your views here.
def index(request):
	return render(request, 'login_app/index.html')

def user(request, user_id):
	if 'login' not in request.session:
		messages.warning(request, 'You must be login')
		return redirect('/')

	user = User.objects.filter(id=user_id)
	quotes = Quote.objects.filter(submit_by=user)
	print (user[0].first_name)
	context = {
		'user': user[0],
		'post': quotes,
		'count': len(quotes),
	}
	return render(request, 'login_app/user_profile.html', context)

def register(request):
	# validate that the email and register the user
	if User.objects.filter(email=request.POST['email']):
		messages.warning(request, 'Look like you already registered, try logging in!')
		return redirect('/')
	try:
		User.objects.register(request.POST['first_name'], request.POST['last_name'], request.POST['email'], request.POST['password'], request.POST['password2'], request.POST['date_of_birth'])
		try:
			success = User.objects.login(request.POST['email'], request.POST['password'])
			if success == False:
				message.warning(request, 'Incorrect email / password')
				return redirect('/')
			else:
				user = User.objects.filter(email=request.POST['email'])
				request.session['user_id'] = user[0].id
				request.session['first_name'] = user[0].first_name
				request.session['login'] = True
				messages.success(request, 'Successfully login')
				return redirect('/quotes')
		except Exception as e:
			messages.warning(request, e)
			return redirect('/')
	except Exception as e:
		print e
		if e == 'password error':
			messages.warning(request, 'Password must be at least 8 characters long')
		else:
			messages.warning(request, e)
		return redirect('/')

def login(request):
	errors = 0
	if len(request.POST['email'])<1:
		messages.warning(request, 'Email field required')
		errors + 1

	if len(request.POST['password'])<1:
		messages.warning(request, 'Password field required')

	if errors > 0:
		return redirect('/')

	try:
		success = User.objects.login(request.POST['email'],request.POST['password'])
		if success == False:
			messages.warning(request, 'Incorrect Login')
			return redirect('/')
		else:
			user = User.objects.filter(email=request.POST['email'])
			request.session['user_id'] = user[0].id
			request.session['first_name'] = user[0].first_name
			request.session['login'] = True
			messages.warning(request, 'Successfully login')
			return redirect('/quotes')
	except Exception as e:
		messages.warning(request, e)
		return redirect('/')


def success(request):
	return render(request, 'login_app/quotes.html')


def quotes(request):
	if 'login' not in request.session:
		messages.warning(request, 'You must be login')
		return redirect('/')

	user = User.objects.filter(id=request.session['user_id'])
	favorites = Favorite.objects.filter(user_id=user[0])
	quote = Quote.objects.exclude(favorite__user_id_id=user[0])
	print "*" *50
	print quote
	context = {
		'quotes': quote,
		'favorites': favorites
	}
	return render(request, 'login_app/quotes.html', context)

def create(request):
	user = User.objects.filter(id=request.session['user_id'])
	errors = 0
	if len(request.POST['quoted_by']) < 3:
		messages.warning(request, 'Quoted by must be at least 3 characters in length')
		errors = error + 1
	if len(request.POST['quote_message']) < 10:
		messages.warning(request, 'Message must be at least 10 characters in length')
		errors = error +1
	if errors > 0:
		return redirect('/quotes')
	new_quote = Quote(quoted_by=request.POST['quoted_by'], message=request.POST['quote_message'], submit_by=user[0])

	try:
		new_quote.save()
		messages.success(request, 'Quote sucessfully saved')
		return redirect('/quotes')
	except Exception as e:
		 messages.warning(request, e)
		 return redirect('/quotes')

def addFavorite(request, quoteid):
	user = User.objects.filter(id=request.session['user_id'])
	quote = Quote.objects.filter(id=quoteid)
	try:
		favorite_quote = Favorite(quote_id=quote[0], user_id=user[0])
		favorite_quote.save()
		return redirect('/quotes')
		messages.success(request, 'Favorite quotes successfully saved')
	except Exception as e:
		messages.warning(request, e)
		return redirect('/quotes')

def destroyFavorite(request, favoriteid):
	user = User.objects.filter(id=request.session['user_id'])
	favorite_quote = Favorite.objects.get(id=favoriteid)
	try:
		favorite_quote.delete()
		messages.warning(request, 'Favorite successfully deleted')
		return redirect('/quotes')
	except Exception as e:
		messages.warning(request, e)
		return redirect('/quotes')



def logout(request):
	del request.session['login']
	del request.session['first_name']
	del request.session['user_id']
	messages.warning(request, 'User successfully logout')
	return redirect('/')



			





































































