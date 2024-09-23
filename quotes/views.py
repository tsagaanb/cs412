## hw/views.py
# description: the logic to handle URL requests

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random
# Create your views here.

# List of quotes
quotes = [
    "' Life is what happens while you are busy making other plans. '",
    "' We've got this gift of love, but love is like a precious plant. You can't just \
    accept it and leave it in the cupboard or just think it's going to get on by \
    itself. You've got to keep watering it. You've got to really look after it and \
    nurture it. '",
    "' As usual, there is a great woman behind every idiot. '",
    "' Everything will be okay in the end. If it's not okay, it's not the end. '",
    "' Love is the answer, and you know that for sure; Love is a flower, you've got \
    to let it grow. '",
    "' Yeah we all shine on, like the moon, and the stars, and the sun. '",
    "' Time you enjoy wasting, was not wasted. '",
    "' Reality leaves a lot to the imagination. '",
    "' You don't need anybody to tell you who you are or what you are. \
    You are what you are! '",
    "' Everybody loves you when you're six foot in the ground. '"
]
# List of images
images = [
    "/static/images/john_lennon.jpg",
    "/static/images/john_lennon_1.jpg",
    "/static/images/john_lennon_2.jpg",
    "/static/images/john_lennon_3.jpg",
    "/static/images/john_lennon_4.jpg",
    "/static/images/john_lennon_5.jpg",
    "/static/images/john_lennon_6.jpg",
    "/static/images/john_lennon_7.jpg",
    "/static/images/john_lennon_8.jpg",
    "/static/images/john_lennon_9.jpg"
]


def quote(request):
    ''' A function to respond to the / and /quote URL.
    This function will delegate work to an HTML template
    '''
    # this template will present the response
    template_name = "quotes/quote.html"

    # Randomly select a quote and an image
    random_quote = random.choice(quotes)
    random_image = random.choice(images)   
    context = {
        'quote': random_quote,
        'image': random_image
    }
    # delegate response to the template:
    return render(request, template_name, context)

def show_all(request):
    '''
    A function to respond to the /show_all URL.
    This function will delegate work to an HTML template
    '''
    template_name = 'quotes/show_all.html'

    random.shuffle(quotes)
    random.shuffle(images)
    quotes_and_images = zip(quotes, images)  # Combine quotes and images
    context = {
        'quotes_and_images': quotes_and_images
    }
    return render(request, template_name, context)

def about(request):
    '''
    A function to respond to the /about URL.
    This function will delegate work to an HTML template
    '''
    template_name = 'quotes/about.html'
    context = {
        'image': "/static/images/john_lennon_about.jpg",
        'wife': "/static/images/john_lennon_with_wife.jpg"
    }
    return render(request, template_name, context)




