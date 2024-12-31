from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Course, Student, Member, CustomUser  
from .forms import AdminLoginForm, UserRegistrationForm, LoginForm, CourseEnrollmentForm
from django.contrib.auth.decorators import login_required
from .forms import MemberForm


# Home Page
def home(request):
    return render(request, 'edso_app/home.html')

# Student Registration
def register_student(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Create the student instance and link to the user
            student = Student(user=user)
            student.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'edso_app/register_student.html', {'form': form})

# Student Login
def login_student(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(f"Attempting to authenticate user: {username}")  # Debugging
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                print("login user")
                return redirect('student_dashboard')
            else:
                messages.error(request, 'Invalid credentials')
        else:
            print("Form is not valid:", form.errors)  # Debugging
    else:
        form = LoginForm()
    return render(request, 'edso_app/login.html', {'form': form})

# Student Dashboard
@login_required
def student_dashboard(request):
    courses = Course.objects.all()
    return render(request, 'edso_app/student_dashboard.html', {'courses': courses})

# Member Login
def login_member(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(f"Attempting to authenticate user: {username}")  # Debugging
            
            # Authenticate the user with the provided username and password
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Check if the user is an instance of CustomUser and is a member
                if isinstance(user, CustomUser) and user.is_member:
                    login(request, user)  # Log the user in
                    print(user.is_member)
                    print("Login successful, redirecting to member dashboard")
                    return redirect('member_dashboard')  # Redirect to the member dashboard
                else:
                    messages.error(request, 'User is not a member or does not have valid access.')
                    print("User is not a valid member")
            else:
                messages.error(request, 'Invalid credentials')
                print("Invalid credentials")
        else:
            print("Form is not valid:", form.errors)  # Debugging: output form errors

    else:
        form = LoginForm()

    return render(request, 'edso_app/login_member.html', {'form': form})

# Member Dashboard
@login_required
def member_dashboard(request):
    # Ensure that only members have access to the member dashboard
    if not request.user.is_member:
        return redirect('home')  # Redirect to home if the user is not a member

    # Fetch courses for the logged-in member if required
    courses = Course.objects.all()  # You can modify this query if you need to filter courses for the member

    # Optionally, if you want to display specific information about the logged-in user:
    member = request.user  # Since the user is authenticated and is a member, you can directly use request.user

    return render(request, 'edso_app/member_dashboard.html', {'member': member, 'courses': courses})

# Admin Login

def login_admin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Authenticate the user
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            
            # Check if the user exists and is a superuser (admin)
            if user is not None and user.is_superuser:
                # print("user", user)
                login(request, user)  # Log the user in
                return redirect('admin_dashboard')  # Redirect to the admin dashboard (you can change the URL name as needed)
            else:
                messages.error(request, 'Invalid credentials or you do not have permission to access this area.')
    else:
        form = LoginForm()

    # Render the login page with the form
    return render(request, 'edso_app/login_admin.html', {'form': form})

# Admin Dashboard
@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('home')

    members = Member.objects.all()
    courses = Course.objects.all()

    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            # Create a new member (CustomUser)
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Set the password correctly
            user.is_member = True
            user.save()  # Save the user

            # Optionally, create a Member record if you have a separate model
            Member.objects.create(user=user)

            messages.success(request, 'New member added successfully!')
            return redirect('admin_dashboard')  # Redirect back to the dashboard

    else:
        form = MemberForm()

    return render(request, 'edso_app/admin_dashboard.html', {'members': members, 'courses': courses, 'form': form})


def edit_member(request, member_id):
    member = get_object_or_404(CustomUser, id=member_id)  # Retrieve member by ID

    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)  # Bind the form to the existing member
        if form.is_valid():
            form.save()  # Save the updated member details
            messages.success(request, 'Member updated successfully!')
            return redirect('admin_dashboard')  # Redirect to the dashboard after saving
    else:
        form = MemberForm(instance=member)  # Pre-populate the form with existing member data

    return render(request, 'edso_app/edit_member.html', {'form': form, 'member': member})

# Logout
def logout_user(request):
    logout(request)
    return redirect('home')
