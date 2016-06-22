from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from .models import SignUp
from .forms import ContactForm, SignUpForm


# Create your views here.
def home(request):
    title = "Sign Up Now"
    form = SignUpForm(request.POST or None)
    context = {"title": title, "form": form}

    if request.user.is_authenticated():
        title = "Welcome %s" %(request.user)

    if form.is_valid():
        # print request.POST['email']
        instance = form.save(commit=False)
        full_name = form.cleaned_data.get("full_name")
        if not full_name:
            full_name = "Anonimous User"
        instance.full_name = full_name
        instance.save()
        context = {"title": "Thank you!"}

    if request.user.is_authenticated and request.user.is_staff:
        queryset = SignUp.objects.all().order_by("-timestamp")
        context = {"queryset": queryset}

    return render(request, "home.html", context)


def contact(request):
    title = 'Contact Us'
    title_align_center = True
    form = ContactForm(request.POST or None)
    if form.is_valid(): # Example of getting data from the form.
        # for key, value in form.cleaned_data.items():
            # print key, value
        form_email = form.cleaned_data.get("email")
        form_message = form.cleaned_data.get("message")
        form_full_name = form.cleaned_data.get("full_name")

        subject = "Site contact form"
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email,]
        contact_message = "%s: %s via %s" %(
            form_full_name,
            form_message,
            form_email)

        send_mail(subject, 
            contact_message, 
            from_email, 
            to_email, 
            fail_silently=False)

    context = {
        "form": form,
        "title": title,
        "title_align_center": title_align_center}
    
    return render(request, "forms.html", context)


def about(request):
    return render(request, "about.html", {})
    