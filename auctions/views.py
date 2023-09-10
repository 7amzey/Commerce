from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import create_post, NewBidForm, CommentsForm
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import *


def index(request):
    return render(request, "auctions/index.html",{
        "auctions": Product.objects.filter(is_active=True).order_by('-created_at')
    })


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

@login_required
def create_listing(request):
    if request.method == "POST":
        form = create_post(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            form = create_post()
            return render(request, "auctions/create_post.html",{
                "form": form
            })
        else:
            return render(request, "auctions/create_post.html",{
                "form": form,
                "message": "Invalid Credentials"
            })
    else:
        return render(request, "auctions/create_post.html",{
            "form": create_post()
        })

def listing_page(request, auction_id):
    auction = Product.objects.get(pk=auction_id)
    form = NewBidForm()
    comment = CommentsForm()
    comments = Comment.objects.filter(product=auction)
    return render(request, "auctions/listing_page.html", {
        "auction": auction,
        "form": form,
        "comment_form": comment,
        "comments": comments,
    })

@login_required
def bidding(request, auction_id):
    auction = Product.objects.get(pk=auction_id)
    offer = float(request.POST['offer'])
    if validation1(offer, auction):
        auction.current_price = offer
        form = NewBidForm(request.POST)
        NewBid = form.save(commit=False)
        NewBid.product = auction
        NewBid.user = request.user
        NewBid.save()
        auction.save()
        return HttpResponseRedirect(reverse("listing_page", args=[auction_id]))
    else:
        return render(request, "auctions/listing_page.html",{
            "auction": auction,
            "form": NewBidForm(),
            "error_min_value": True,
            "comment_form": CommentsForm(),
            "comments": Comment.objects.filter(product=auction)
        })

def validation1(offer, auction):
    if offer >= auction.start_price and (auction.current_price is None or offer > auction.current_price):
        return True
    else:
        return False

def closing(request, auction_id):
    auction = Product.objects.get(pk=auction_id)
    if request.user == auction.user:
        if Bid.objects.filter(product=auction).last() == None:
            return render(request, "auctions/confirm_closing.html", {
                "auction": auction
            })
        else:
            auction.is_active = False
            auction.buyer = Bid.objects.filter(product=auction).last().user
            auction.save()
            return HttpResponseRedirect(reverse("index"))

def confirm_closing(request, auction_id):
    auction = Product.objects.get(pk=auction_id)
    if request.user == auction.user:
        if "Cancel" in request.POST:
            return HttpResponseRedirect(reverse("listing_page", args=[auction_id]))
        else:
            auction.is_active = False
            auction.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("listing_page", args=[auction_id]))

@login_required
def comments(request, auction_id):
    auction = Product.objects.get(pk=auction_id)
    comments = Comment.objects.filter(product=auction)
    form = NewBidForm()
    if request.method == "POST":
        comment = CommentsForm(request.POST)
        if comment.is_valid():
            form = comment.save(commit=False)
            form.product = auction
            form.user = request.user
            form.save()
            return HttpResponseRedirect(reverse("listing_page", args=[auction_id]))
        else:
            comment = CommentsForm()
            return render(request, "auctions/listing_page.html",{
                "auction":auction,
                "comment_form": comment,
                "comments": comments,
                "form": form,
                "comment_error": True
            })

def category(request):
    categories = Category.objects.order_by('name')
    return render(request, "auctions/category_page.html", {
        "categories": categories
    })

def auction_by_category(request, name):
    category_name = Category.objects.get(name=name)
    auction = Product.objects.filter(category=category_name, is_active=True).order_by('-created_at')
    return render(request, "auctions/auction_by_category.html",{
        "auctions": auction,
        "categories": category_name
    })

@login_required
def watchlists(request,auction_id):
    if request.method == "POST":
        auction = Product.objects.get(pk=auction_id)
        mywatchlist = request.user.watchlist
        if auction in mywatchlist.all():
            mywatchlist.remove(auction)
        else:
            mywatchlist.add(auction)
        return HttpResponseRedirect(reverse('listing_page', args=[auction_id]))

@login_required
def watchlist_page(request):
    mywatchlist = request.user.watchlist.all()
    return render(request, "auctions/my_watchlist.html",{
        "mywatchlist": mywatchlist
    })

def search_bar(request):
    if request.method == "GET":
        search = request.GET.get('search','')
        auctions = Product.objects.all().filter(is_active=True,title__icontains=search)
        return render(request, "auctions/search_page.html",{
            "auctions": auctions,
            "search_query": search
        })

def closed_auctions(request):
    return render(request, "auctions/closed_auctions.html",{
        "auctions": Product.objects.filter(is_active=False)
    })

@login_required
def my_auctions(request, username):
    user_name = User.objects.get(username=username)
    auctions = Product.objects.filter(user=user_name, is_active=True).order_by('-created_at')
    return render(request, "auctions/users_auctions.html",{
        "auctions": auctions,
        "user": user_name
    })
