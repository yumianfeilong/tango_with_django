from django.contrib.auth.models import User
from django.shortcuts import render,redirect

from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse

from rango.models import Category, Page ,UserProfile

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,login,authenticate
from datetime import datetime
"""
def visitor_cookie_handler(request, response):
    visits = int(request.COOKIES.get('visits','1'))
    last_visit_cookie = request.COOKIES.get('last_visit',str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')
    if (datetime.now() - last_visit_time).seconds > 0:
        visits = visits + 1
    response.set_cookie('last_visit',str(datetime.now()))
    response.set_cookie('visits',str(visits))
"""
def track_url(request):
    page_id = None
    url = "/rango/"
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            try:
                page = Page.objects.get(id=page_id)
                page.views = page.views + 1
                page.save()
                url = page.url
            except:
                pass
    return redirect(url)


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request,'visits','1'))
    last_visit_cookie = get_server_side_cookie(request,'last_visit',str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')
    if (datetime.now() - last_visit_time).seconds > 0:
        visits = visits + 1
    request.session['last_visit'] = str(datetime.now())
    request.session['visits'] = visits

def user_login(request):
    if request.method == 'POST' :
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your rango account is disabled.")
        else:
            print("Invalid login details: %s, %s" % (username,password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request,'rango_login.html',{})


@login_required
def user_logout(request):
    logout(request)
    return index(request)

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this page")

def index(request):
    category_list = Category.objects.order_by("-likes")[:5]
    page_list = Page.objects.order_by("-views")[:5]
    context_dict = { "categories":category_list,"pages":page_list}
    #context_dict = { "boldmessage": "Crunchy, creamy, cookie, candy, cpucake !"}
    #request.session.set_test_cookie()
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    context_dict['last_visit'] = request.session['last_visit']
    return render(request,'rango_index.html',context=context_dict)

def show_category(request,category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category).order_by('-views')
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
    return render(request,'rango_category.html',context=context_dict)

def about(request):
    #return HttpResponse("This is an about page ! Go <a href='/rango/'>Index</a>.  ")
    context_dict = { "boldmessage": "Site is built via django."}
    visits = int(get_server_side_cookie(request,'visits','1'))
    last_visit_cookie = get_server_side_cookie(request,'last_visit',str(datetime.now()))
    context_dict['visits']=visits
    context_dict['last_visit_cookie']=last_visit_cookie
    #if request.session.test_cookie_worked():
    #    print("test cooki worked!")
    #    request.session.delete_test_cookie()
    return render(request,'rango_about.html',context=context_dict)

from rango.forms import CategoryForm
@login_required
def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # Have we been provided with a valid form?
        if form.is_valid():
        # Save the new category to the database.
            form.save(commit=True)
            return index(request)
        else:
           # The supplied form contained errors -
           # just print them to the terminal.
            print(form.errors)
    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'rango/rango_add_category.html', {'form': form})

from rango.forms import PageForm
@login_required
def add_page(request,category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Catgory.DoesNotExist:
        category = None
    form = PageForm()
    if request.method=='POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print (form.errors)
    context_dict = {'form':form,'category':category}
    return render(request,'rango_add_page.html',context_dict)

from rango.forms import UserForm,UserProfileForm

@login_required
def register_profile(request):
    form = UserProfileForm()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect('index')
        else:
            print(form.errors)
    context_dict = {'form':form}
    return render(request,'rango/profile_registration.html', context_dict)





def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request,'rango/rango_register.html', {'user_form':user_form,'profile_form':profile_form,'registered':registered})

@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')
    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm({'website':userprofile.website, 'picture':userprofile.picture})
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('profile', user.username)
        else:
            print(form.errors)
    return render(request, 'rango/user_profile.html',{'userprofile':userprofile,'selecteduser':user,'form':form})


@login_required
def list_profiles(request):
    userprofile_list = UserProfile.objects.all()
    return render(request,'rango/list_profiles.html',{'userprofile_list':userprofile_list})

@login_required
def like_category(request):
    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id'] 
    likes = 0
    if cat_id:
        cat = Category.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes = likes
            cat.save()
    return HttpResponse(likes)


def get_category_list(max_result=0, starts_with=''):
    cat_list = []
    if starts_with:
        cat_list = Category.objects.filter(name__istartswith=starts_with)
    if max_result > 0 :
        if len(cat_list) > max_result:
            cat_list = cat_list[:max_results]
    return cat_list

def suggest_category(request):
    cat_list = []
    starts_with = ""
    if request.method == 'GET':
        starts_with = request.GET['suggestion']
    cat_list = get_category_list(8, starts_with)
    print(" get %s" % starts_with )
    for c in cat_list:
        print c
    return render(request, 'rango/cats.html',{'cats':cat_list })
 
