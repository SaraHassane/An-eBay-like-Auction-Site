from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, auctionComments, Bid

def listingPage(request, id):
    listingDetails = Listing.objects.get(pk=id)
    watchListCheck = request.user in listingDetails.watchlist.all()
    allComments = auctionComments.objects.filter(listing=listingDetails)
    isOwner = request.user.username == listingDetails.owner.username
    return render(request, "auctions/listingPage.html",{
        "listingPage": listingDetails,
        "watchListCheck": watchListCheck,
        "allComments": allComments,
        "isOwner": isOwner
    })

def auctionClosed(request, id):
    listingDetails = Listing.objects.get(pk=id)
    listingDetails.isActive = False
    listingDetails.save()
    isOwner = request.user.username == listingDetails.owner.username
    watchListCheck = request.user in listingDetails.watchlist.all()
    allComments = auctionComments.objects.filter(listing=listingDetails)
    return render(request, "auctions/listingPage.html",{
        "listingPage": listingDetails,
        "watchListCheck": watchListCheck,
        "allComments": allComments,
        "isOwner": isOwner,
        "update": True,
        "message": "Your auction has officially been closed"
    })

def addBid(request, id):
    newBid = request.POST['newBid']
    listingDetails = Listing.objects.get(pk=id)
    watchListCheck = request.user in listingDetails.watchlist.all()
    allComments = auctionComments.objects.filter(listing=listingDetails)
    isOwner = request.user.username == listingDetails.owner.username
    if int(newBid) > listingDetails.price.bid:
        updateBid = Bid(user=request.user, bid=int(newBid))
        updateBid.save()
        listingDetails.price = updateBid
        listingDetails.save()
        return render(request, "auctions/listingPage.html", {
            "listingPage": listingDetails,
            "message": "Bid Updated",
            "update": True,
            "watchListCheck": watchListCheck,
            "allComments": allComments,
            "isOwner": isOwner,
        })
    else:
       return render(request, "auctions/listingPage.html", {
            "listingPage": listingDetails,
            "message": "Bid failed to update",
            "update": False,
            "watchListCheck": watchListCheck,
            "allComments": allComments,
            "isOwner": isOwner,
        })

def watchListPage(request):
    currentUser = request.user
    listing = currentUser.watchlist.all() 
    return render(request, "auctions/watchlist.html", {
        "listings": listing
    })
    
def commentSection(request, id):
    currentUser = request.user
    listingDetails = Listing.objects.get(pk=id)
    message = request.POST['newComment']

    newComment = auctionComments(
        author=currentUser,
        listing=listingDetails,
        message=message
    )

    newComment.save()

    return HttpResponseRedirect(reverse("listingPage",args=(id, )))

def watchListRemove(request, id):
    listingDetails = Listing.objects.get(pk=id)
    currentUser = request.user
    listingDetails.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listingPage",args=(id, )))

def watchListAdd(request, id):
    listingDetails = Listing.objects.get(pk=id)
    currentUser = request.user
    listingDetails.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("listingPage",args=(id, )))

def index(request):
    activeListingsPage = Listing.objects.filter(isActive=True)
    allCategories = Category.objects.all()
    return render(request, "auctions/index.html",{
        "listings": activeListingsPage,
        "categories": allCategories
    })

def displayCategory(request):
    if request.method == "POST":
        formCategory = request.POST['category']
        category = Category.objects.get(nameOfCategory=formCategory)
        activeListingsPage = Listing.objects.filter(isActive=True, category=category)
        allCategories = Category.objects.all()
        return render(request, "auctions/index.html",{
            "listings": activeListingsPage,
            "categories": allCategories
        })

def create_listing(request):
    if request.method == "GET":
        allCategories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": allCategories
        })
    else:
        # Get data from form
        title = request.POST["title"]
        description = request.POST["description"]
        imageurl = request.POST["imageurl"]
        price = request.POST["price"]
        category = request.POST["category"]
        # user active
        currentUser = request.user
        # Get all content of category
        categoryContent = Category.objects.get(nameOfCategory=category)
        # create a bid
        bid = Bid(bid=float(price), user=currentUser)
        bid.save()
        # Create a new listing object
        newList = Listing(
            title=title,
            description=description,
            imageUrl=imageurl,
            price=bid,
            category=categoryContent,
            owner=currentUser
        )
        # Insert object in database
        newList.save()
        # Redcirect to index page
        return HttpResponseRedirect(reverse(index))


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
