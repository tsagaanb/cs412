## restaurant/views.py
# description: the logic to handle URL requests

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
import time
import random

MENU_PRICES = {
    "Buuz": 9,
    "Khuushuur": 10,
    "Tsuivan": 12,
    "Boortsog": 6,
}

SAUCE_PRICES = {
    "None": 0,
    "Spicy Sauce": 2,
    "Garlic Sauce": 2
}


dailySpecials = [
    "Ortz Soup: A hearty lamb and potato stew cooked with traditional Mongolian herbs.",
    "Marmot Khorkhog: A special version of khorkhog made with tender marmot meat, cooked using hot stones.",
    "Tavan Bogd Goat Roast: Slowly roasted goat seasoned with cumin, garlic, and served with mashed potatoes.",
    "Yak Meat Tsuivan: Stir-fried yak meat with fresh noodles and vegetables.",
    "Horse Meat Dumplings: Juicy dumplings stuffed with seasoned horse meat and onions.",
    "Baked Boodog: Traditional baked lamb cooked with hot stones and herbs inside the carcass for rich flavor.",
    "Suutei Tsai Brunch: Includes a platter of eggs, sausages, boortsog, fresh bread, and a large pot of salted milk tea."
]

dailySpecialPrices = [
    12,
    24,
    26,
    18,
    17,
    25,
    20
]

dailySpecialPhotos = [
    "/static/images/ortz_soup.jpeg",
    "/static/images/khorkhog.jpeg",
    "/static/images/roast_goat.jpeg",
    "/static/images/yak_tsuivan.jpeg",
    "/static/images/horse_dumplings.jpeg",
    "/static/images/boodog.jpeg",
    "/static/images/brunch.jpeg",
]

def main(request):
    ''' A function to respond to the /main URL.
    This function will delegate work to an HTML template
    '''
    # this template will present the main page
    template_name = "restaurant/main.html"
 
    return render(request, template_name)

def order(request):
    '''
    A function to respond to the /order URL.
    This function will delegate work to an HTML template
    '''
    template_name = 'restaurant/order.html'

   
    # Get a random index within the length of the lists
    random_index = random.randint(0, len(dailySpecials) - 1)

    # Get the corresponding special and photo using the random index
    special = dailySpecials[random_index]
    special_photo = dailySpecialPhotos[random_index]
    daily_special_price = dailySpecialPrices[random_index]

    context = {
        'daily_special': special,
        'daily_special_photo': special_photo,
        'daily_special_price': daily_special_price
    }
    return render(request, template_name, context)

def confirmation(request):
    '''
    Handles the form submission.
    Read our the form data. 
    Generate a reasponse
    '''
    template_name = 'restaurant/confirmation.html'

    # Check if the request is a POST (vs. GET)
    if request.POST:

        # generate a random minute between 30-60 and
        # add it to the current time
        current_time = time.time()
        random_minutes = random.randint(30, 60)
        seconds_to_add = random_minutes * 60
        ready_time_sec = current_time + seconds_to_add
        ready_time = time.ctime(ready_time_sec)

        # read the order data into python variables
        order = request.POST.getlist("order[]") 
        sauce = request.POST.get("sauce", "")
        daily_special = request.POST.get("daily_special", "")
        daily_special_price = request.POST.get("daily_special_price", 0)
        special_instructions = request.POST.get("special_instructions", "")
        name = request.POST.get("name", "")
        phone = request.POST.get("phone", "")
        email = request.POST.get("email", "")


        total_price = 0
        for item in order:
            total_price += MENU_PRICES.get(item, 0)  # Add price of each item to total

        if daily_special:
            total_price += int(daily_special_price)
            daily_special = daily_special.split(':')[0]
            
        if sauce:
            total_price += SAUCE_PRICES.get(sauce, 0)
        # Add the daily special price if it exists (this assumes you store prices for specials)

        # package the data up to be used in response
        context = {
            'ready_time': ready_time,
            'order': order,
            'sauce' : sauce,
            'daily_special': daily_special,
            'special_instructions': special_instructions,
            'name': name,
            'phone': phone,
            'email': email,
            'total_price': total_price,
        }

        # Generate a repsonse
        return render(request, template_name, context)

    return redirect("order") # name on urls.py to the page



