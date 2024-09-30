#  formdata/views.py
from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
def show_form(request):
    '''
    A function to respond to the /show_all URL.
    This function will delegate work to an HTML template
    '''
    template_name = 'formdata/form.html'
    return render(request, template_name)

def submit(request):
    '''
    Handles the form submission.
    Read our the form data. 
    Generate a reasponse
    '''
    template_name = 'formdata/confirmation.html'
    # print(request)

    # Check if the request is a POST (vs. GET)
    if request.POST:

        # Read the form data into python variable
        name = request.POST['name']
        favorite_color = request.POST['favorite_color']

        # package the data up to be used in response
        context = {
            'name': name,
            'favorite_color': favorite_color
        }

        # Generate a repsonse
        return render(request, template_name, context)

    ## GET lands down here: no return statements!

    # this is an okay solution: a graceful failure
    # return HttpResponse("Nope.")


    # if the client got here by making a GET on this ,send back the form
    # this is a better solution:
    # template_name = 'formdata/form.html'
    # return render(request, template_name)


    # this is the "best" solution: redirect to the GET function
    return redirect("show_form") # name on urls.py to the page

