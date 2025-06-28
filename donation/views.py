from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from .models import Donation
from .forms import DonationForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.contrib import messages
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactMessage

from django.utils import timezone
from .forms import ContactReplyForm
from django.contrib.admin.views.decorators import staff_member_required


from .forms import RegisterForm, DonationForm
from .models import Donation

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        else:
            
            return render(request, 'register.html', {'form': form})
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')




@login_required
def dashboard_view(request):
   if request.user.is_superuser:
        # Admin dashboard
        donations = Donation.objects.all()
        users = User.objects.all()
        return render(request, 'admin_dashboard.html', {
            'donations': donations,
            'users': users,
            'admin': True,
        })
   else:
        # Normal user dashboard
        donations = Donation.objects.filter(donor=request.user)
        return render(request, 'user_dashboard.html', {
            'donations': donations,
            'admin': False,
        })






@login_required
def donate_view(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.donor = request.user
            donation.save()
            return redirect('dashboard')
    else:
        form = DonationForm()

    return render(request, 'donate.html', {
        'form': form,
        'editing': False  # This tells the template we're not editing
    })

@login_required
def update_donation(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id, donor=request.user)
    if request.method == 'POST':
        form = DonationForm(request.POST, instance=donation)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = DonationForm(instance=donation)
        donations = Donation.objects.filter(donor=request.user)

    return render(request, 'donate.html', {
        'form': form,
        'donations': donations,
        'editing': True ,
        
    })

@login_required
@require_POST
def delete_donation(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id, donor=request.user)
    donation.delete()
    return redirect('dashboard')



def about_view(request):
    return render(request, 'about.html')


def food_safety_view(request):
    return render(request, 'food_safety.html')


def impact_view(request):
    total_users = User.objects.count()
    total_donations = Donation.objects.count()
    total_meals = Donation.objects.aggregate(total=Sum('quantity'))['total'] or 0  # Assuming 1 quantity = 1 meal

    context = {
        'total_users': total_users,
        'total_donations': total_donations,
        'total_meals': total_meals
    }
    return render(request, 'impact.html', context)


@login_required
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            if request.user.is_authenticated:
                contact.user = request.user
            contact.save()

            # ✅ Send email notification to admin
            send_mail(
                subject=f"New Contact from {contact.name}",
                message=contact.message,
                from_email=contact.email,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=True,
            )

            messages.success(request, 'Your message has been sent successfully.')
            return redirect('contact')
    else:
        if request.user.is_authenticated:
            form = ContactForm(initial={
                'name': request.user.get_full_name() or request.user.username,
                'email': request.user.email
            })
        else:
            form = ContactForm()

    return render(request, 'contact.html', {'form': form})


@login_required
def message_history_view(request):
    messages = ContactMessage.objects.filter(email=request.user.email).order_by('-submitted_at')
    return render(request, 'message_history.html', {'messages': messages})


@staff_member_required
def admin_messages_view(request):
    messages = ContactMessage.objects.all().order_by('-submitted_at')
    return render(request, 'admin_messages.html', {'messages': messages})

@staff_member_required
def admin_reply_message(request, message_id):
    message = get_object_or_404(ContactMessage, id=message_id)

    if request.method == 'POST':
        form = ContactReplyForm(request.POST, instance=message)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.replied = True
            reply.replied_at = timezone.now()
            reply.save()

            # Send email to user
            send_mail(
                subject=f"Reply to your message - Food Donation Platform",
                message=reply.reply_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[reply.email],
                fail_silently=False,
            )

            return redirect('admin_messages')

    else:
        form = ContactReplyForm(instance=message)

    return render(request, 'admin_reply.html', {
        'form': form,
        'message': message
    })