from django.contrib import admin
from .models import Donation
from .models import ContactMessage
from django.core.mail import send_mail
from django.conf import settings

admin.site.register(Donation)



@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at','replied', 'reply')
    search_fields = ('name', 'email', 'message')
    list_filter = ('submitted_at','replied')
    readonly_fields = ('name', 'email', 'message', 'submitted_at')
    fields = ('user', 'name', 'email', 'message','replied', 'reply', 'submitted_at')

   




    def save_model(self, request, obj, form, change):
        # Send email only when replying for the first time
        if obj.reply and not obj.replied:
            subject = "Reply to your message - Food Donation Platform"
            message = f"""
Hi {obj.name},

You sent us this message:
-------------------------------------
{obj.message}

Here is our reply:
-------------------------------------
{obj.reply}

Thank you for reaching out!

- Food Donation Team
            """
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [obj.email],
                fail_silently=False
            )
            obj.replied = True  # mark as replied
        obj.save()       