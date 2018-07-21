from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
import os.path
from shutil import copyfile


from .forms import RegisterForm, LoginForm, ImageUpload, AuthorizeForm, LikeForm

from .models import Images, LikeTable

from django.views.generic.list import ListView

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class IndexView(ListView):
    model = Images
    template_name = 'photos/index.html'
    paginate_by = 9  # if pagination is desired
    variable_order= 'like_count'
    warnings= []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ImageUpload()
        context['warnings']= IndexView.warnings
        return context

    def get_queryset(self):
        aux= Images.objects.filter(authorized=True)
        return aux.order_by(self.variable_order).reverse()

    def post(self,request, *args, **kwargs):
        IndexView.warnings = []
        if request.method == 'POST' and 'add' in request.POST:  # add image
            print(request.FILES.getlist('image'))
            cont= 0
            for cont, f in enumerate(request.FILES.getlist('image')):
                if request.user.is_authenticated:  # Save new image
                    fname= os.path.splitext(str(f))[1].strip()
                    title = 'uploads/{}_{}_{}{}'.format(request.user.username, cont,
                                                    datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"),
                                                    fname)
                    with open(BASE_DIR+'/'+title, 'wb+') as destination:
                        for chunk in f.chunks():
                            destination.write(chunk)

                    modelImage = Images(user=request.user, path=title, description=request.POST['description'])
                    modelImage.save()
                else:
                    IndexView.warnings.append("Only the image formats can been added.")
            return HttpResponseRedirect('/#about')

            # form = ImageUpload(request.POST, request.FILES)
            # if form.is_valid():
            #     f = request.FILES['image']
            #     if request.user.is_authenticated:  # Save new image
            #         title = 'uploads/{}_{}{}'.format(request.user.username,
            #                                          datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"),
            #                                          os.path.splitext(str(f))[1])
            #         with open(BASE_DIR+'/'+title, 'wb+') as destination:
            #             for chunk in f.chunks():
            #                 destination.write(chunk)

            #         modelImage = Images(user=request.user, path=title, description=form.cleaned_data['description'])
            #         modelImage.save()

            #         return HttpResponseRedirect('/#about')
            

        elif request.method == 'POST' and 'like' in request.POST:  # like count
            idObj = request.POST['like']
            obj = Images.objects.get(id=idObj)

            if not request.user.is_authenticated:
                return HttpResponseRedirect('/#portfolio')

            elif (LikeTable.objects.filter(image=obj, user=request.user).exists()):  # delete like and row in likeTable
                imageObj = LikeTable.objects.get(image=obj, user=request.user)
                imageObj.delete()

                obj.like_count = LikeTable.objects.filter(image=obj).count()
                obj.save()

            else:  # add image in likeTable
                imageObj = LikeTable(image=obj, user=request.user)
                imageObj.save()

                obj.like_count = LikeTable.objects.filter(image=obj).count()
                obj.save()
            return HttpResponseRedirect('/#portfolio')

        elif request.method == 'POST' and 'filter' in request.POST:
            IndexView.variable_order = str(request.POST['filter'])

        return HttpResponseRedirect('/#portfolio')
        #return render(request, 'photos/index.html', {'form': form, 'warnings': warnings})

@csrf_protect
def register(request):
    warnings = []

    if request.method == 'POST' and 'register' in request.POST:
        form = RegisterForm(request.POST)

        if form.is_valid():
            if not auth.models.User.objects.filter(username=form.cleaned_data['name']):
                group_users = auth.models.Group.objects.get_or_create(name='Friends')[0]
                user = auth.models.User.objects.create_user(form.cleaned_data['name'],
                                                            form.cleaned_data['email'],
                                                            form.cleaned_data['password'])
                user.groups.add(group_users)
                user.save()
                user = auth.authenticate(username=form.cleaned_data['name'],
                                         password=form.cleaned_data['password'])
                auth.login(request, user)
                return HttpResponseRedirect('/')
            else:
                warnings.append('User exist')
                form = RegisterForm()
    else:
        form = RegisterForm()

    return render(request, 'photos/register.html', {'form': form, 'warnings': warnings})

@csrf_protect
def login(request):
    warnings = []

    if request.method == 'POST' and ('login' in request.POST):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data.get('name'),
                                     password=form.cleaned_data.get('password'))
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    warnings.append('This account has been disabled.')
            else:
                warnings.append('Password or username incorrect.')
    else:
        form = LoginForm()

    return render(request, 'photos/login.html', {'form': form, 'warnings': warnings})


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


@csrf_protect
@login_required
@permission_required("sessions.add_session")
def authorize(request):
    form= AuthorizeForm(Images.objects.all())

    if request.method == 'POST':
        form = AuthorizeForm(Images.objects.all(), request.POST)
        if form.is_valid():
            for k in form.cleaned_data:
                if form.cleaned_data[k] and 'autho' in request.POST:
                    obj = Images.objects.get(id=k)
                    obj.authorized = True
                    obj.save()

                elif form.cleaned_data[k] and 'disallow' in request.POST:
                    obj = Images.objects.get(id=k)
                    obj.authorized = False
                    obj.save()


    return render(request, 'photos/authorize.html', {'form': form, 'images':Images.objects.all()})

#@login_required
#@permission_required("sessions.add_session")
def retrieve_file(request,img,ext):
    obj= Images.objects.filter(path__contains=img)
    if len(obj)==0:
        return HttpResponse('Unauthorized', status=401)
    obj= obj[0]
    if request.user.is_authenticated:
        if request.user.has_perm('sessions.add_session'):
            try:
                image_data = open(BASE_DIR+'/uploads/{}.{}'.format(img,ext), "rb").read()
                return HttpResponse(image_data, content_type="image/png")
            except:
                return HttpResponse('Image Not Found', status=404)


    if obj.authorized:
        try:
            image_data = open(BASE_DIR+'/uploads/{}.{}'.format(img,ext), "rb").read()
            return HttpResponse(image_data, content_type="image/png")
        except:
            return HttpResponse('Image Not Found', status=401)

    return HttpResponse('Unauthorized', status=401)

def help(request):
    return render(request, 'photos/help.html')