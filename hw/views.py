## hw/views.py
# description: the logic to handle URL requests

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random
# Create your views here.


# def home(request):
#     ''' A function to respond to the /hw URL.
#     '''
#     # create some text
#     #               V the "f' is NECESSARY"
#     response_text = f'''  
#     <html>
#         <h1>Hello, world!</h1>
#         <p>
#            This is our first django web page!
#         </p>
#         <hr>
#         This page was generated at {time.ctime()}
#     '''

#     #return a response to the client
#     return HttpResponse(response_text)


def home(request):
    ''' A function to respond to the /hw URL.
    This function will delegate work to an HTML template
    '''
    # this template will present the response
    template_name = "hw/home.html"

    # create a dictionary of context variables
    context = {
        'current_time': time.ctime(),
        'letter1': chr(random.randint(65,90)), # a letter in the range A...Z
        'letter2': chr(random.randint(65,90)), # a letter in the range A...Z
        'number': random.randint(1,10), # a number in the range 1...10
    }
    # delegate response to the template:
    return render(request, template_name, context)

def about(request):
    '''
    A function to respond to the /hw/about URL.
    This function will delegate work to an HTML template
    '''
    template_name = '/hw/about.html'
    # context = {
    #     'current_time': time.ctime(),
    #     'letter1': chr(random.randint(65,90)), # a letter in the range A...Z
    #     'letter2': chr(random.randint(65,90)), # a letter in the range A...Z
    #     'number': random.randint(1,10), # a number in the range 1...10
    # }
    return render(request, template_name, context)




