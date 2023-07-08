from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auction_Listings, Bids


def index(request):
    if request.method == "POST":
        new_listing = Auction_Listings()
        new_listing.title = request.POST["title"]
        new_listing.starting_bid = request.POST["bid"]
        new_listing.url_img = request.POST["url"]
        if request.POST["category"] != "":
            new_listing.category = request.POST["category"]
        if request.POST["desc"] != "":
            new_listing.description = request.POST["desc"]
        new_listing.status = "A"
        new_listing.creator = User.objects.get(pk = request.user.pk)
        new_listing.save()
        listings = Auction_Listings.objects.filter(status = "A")
        return render(request, "auctions/index.html", {"listings":listings})
    listings = Auction_Listings.objects.filter(status = "A")
    return render(request, "auctions/index.html", {"listings":listings})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def add_listing(request):
    return render(request, "auctions/add_listing.html")
def show_listing(request, listing_num):
    li = Auction_Listings.objects.get(pk = listing_num)
    winning_bid = Bids.objects.get(listing = li, value = li.highest_bid)
    winner = winning_bid.user
    if request.method == "POST":
        if "add_bid" in request.POST:
            if int(request.POST["add_bid"])>li.highest_bid and int(request.POST["add_bid"])>li.starting_bid:
                li.highest_bid = int(request.POST["add_bid"])
                li.save()
                new_bid = Bids()
                new_bid.value = int(request.POST["add_bid"])
                new_bid.user = request.user
                new_bid.listing = li
                new_bid.save()
                return render(request, "auctions/listing.html", {"listing":li, "watchli": request.user in li.users_watchlist.all()})
            else:
                return render(request, "auctions/listing.html", {"listing":li, "watchli": request.user in li.users_watchlist.all(), "message": "Bid not high enough!"})
        elif "close" in request.POST:
            li.status = "I"
            li.save()
            return render(request, "auctions/listing.html", {"listing":li, "watchli": request.user in li.users_watchlist.all(), "winner":winner})
        else:
            if "remove" in request.POST:
                li.users_watchlist.remove(request.user)
                return render(request, "auctions/listing.html", {"listing":li, "watchli":False, "winner":winner})
            if "add" in request.POST:
                li.users_watchlist.add(request.user)
                return render(request, "auctions/listing.html", {"listing":li, "watchli":True, "winner":winner})
    return render(request, "auctions/listing.html", {"listing":li,"watchli": request.user in li.users_watchlist.all(), "winner":winner})
def categories(request):
    ca = []
    for i in Auction_Listings.objects.all():
        c = i.category
        if (c not in ca) and (c != ""):
            ca.append(c)
    return render(request, "auctions/categories.html", {"categories":ca})
def watchlist(request):
    ll = []
    for ob in Auction_Listings.objects.all():
        if request.user in ob.users_watchlist.all():
            ll.append(ob)
    return render(request, "auctions/watchlist.html", {"listings":ll})
def category(request, categoryy):
    listings = Auction_Listings.objects.filter(category = categoryy)
    return render(request, "auctions/category.html", {"category":categoryy,"listings":listings})