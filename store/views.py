from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from .models import Course
from django.shortcuts import get_object_or_404


# Create your views here.

def home(request):
    return render(request, 'index.html',{})
    
    
    
def user_profile(request):
    return render(request, 'user_profile.html',{})

def short_course_view(request):
    courses = Course.objects.all( )
    return render(request, 'short_course_view.html',{'courses':courses})


def short_course_create(request):
    return render(request, 'short_course_create.html',{})

###
def course_delete(request, course_id):
    # course = Course().objects.get(pk=course_id)
    course = get_object_or_404(Course, pk=course_id)
    course.delete()
    return redirect('short_course_view')


def course_create(request):
    if request.method == "POST":
        title = request.POST.get('title')
        subtitle = request.POST.get('subtitle')
        description = request.POST.get('description')
        status = request.POST.get('status')

        # Handle image upload
        image = request.FILES.get('image')
        
        # Map the form values to boolean
        status = (status == "Active")  # True if "Active," False if "Deactive"

        # Create a new course object and save it to the database
        course = Course(
            title=title,
            subtitle=subtitle,
            description=description,
            status=status,
            image=image  # Assign the uploaded image to the model's image field
        )
        course.save()

        # Redirect to the page where you want to display the list of courses
        return redirect('short_course_view')

    return redirect('short_course_view')




def course_edit(request, course_id):
    # Retrieve the course based on the course_id
    course = get_object_or_404(Course, pk=course_id)

    if request.method == "POST":
        title = request.POST.get('title')
        subtitle = request.POST.get('subtitle')
        description = request.POST.get('description')
        status = request.POST.get('status')

        # Handle image upload
        image = request.FILES.get('image')
        if image:
            course.image = image

        # Update course details
        course.title = title
        course.subtitle = subtitle
        course.description = description
        course.status = (status == "Active")

        # Save the updated course
        course.save()

        # Redirect to the page where you want to display the list of courses
        return redirect('short_course_view')

    return render(request, 'course_edit.html', {'course': course})


from django.http import JsonResponse

def search_courses(request):
    query = request.GET.get('q', '')

    # Perform the search query, e.g., using the filter() method
    courses = Course.objects.filter(title__icontains=query)

    # Serialize the search results into JSON
    results = [{'title': course.title, 'subtitle': course.subtitle, 'description': course.description} for course in courses]

    return JsonResponse({'results': results})




#################
def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			# messages.success(request, ("You Have Been Logged In!"))
			return redirect('home')
		else:
			# messages.success(request, ("There was an error, please try again..."))
			return redirect('login')

	else:
		return render(request, 'login_user.html', {})
    

def logout_user(request):
    logout(request)
    # messages.success(request, ("you have been logged out"))
    return redirect('home')
    
# @login_required
# def resetPassword(request):
#     if request.method == "POST":
#         password = request.POST['new_password']
#         confirm_password = request.POST['confirm_password']
        
#         if password == confirm_password:
#             uid = request.session.get('uid')
#             user = User.objects.get(pk=uid)
#             user.set_password(password)
#             user.save()
#             # messages.success(request, 'Password reset sucessfully')
#             return redirect('home')
#         else:
#             # messages.error(request, 'Password is does not match!')
#             return redirect('resetPassword')
                                    
#     else:
#         return render(request, 'index.html')
    
    
@login_required
def resetPassword(request):
    if request.method == "POST":
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password == confirm_password:
            user = request.user
            if user.check_password(current_password):
                user.set_password(new_password)
                user.save()
                return redirect('home')
            else:
                # Handle the case where the current password is incorrect
                return redirect('resetPassword')
        else:
            pass
            # Handle the case where the new and confirm passwords do not match
            return redirect('resetPassword')
    return render(request, 'index.html')
# return 