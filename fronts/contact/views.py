from django.shortcuts import render, redirect
from fronts.contact.forms import ContactForm
from django.contrib import messages



def contacts(request):

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully")
            return redirect('home.contacts')
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'

    else:
        form = ContactForm()

    context = {
        "contact_page": "active",
        "form": form

    }
    return render(request, 'frontends/contact.html', context)