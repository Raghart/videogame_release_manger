from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomLoginForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model

from .util import get_igdb_data, html_signup
from .models import Games_Data, Games_Genres

def index(request):
    if request.user.is_authenticated:      
        genres = Games_Genres.objects.all()
        return render(request, "vid_man/index.html", {'genres': genres})
    
    else:
        return render(request, "vid_man/welcome.html")

def signup(request):
    print("Signup view called")
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            form.save()
            
            email = form.cleaned_data.get("email")
            username = form.cleaned_data.get("username")

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activate_url = request.build_absolute_uri(
                reverse('account_confirm_email', args=[uid, token])
            )

            try:
                send_mail(
                    "Welcome to my Site",
                    f"Hi {request.user}, thank you for registering.",
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                    html_message=html_signup(username, activate_url),
                )

            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            

            return render(request, "account/confirm_email.html")
    else:
        form = CustomUserCreationForm()

    return render(request, "account/signup.html", {"form": form})

def confirm_email(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated successfully!')
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')
    
def login_view(request):
    if request.method == "POST":
        form = CustomLoginForm(request, data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user:
                login(request, user)
                return redirect("index")
    else:
        form = CustomLoginForm()

    return render(request, "account/login.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
    
@login_required    
def get_games_data(request):
    igdb_data = get_igdb_data()
    followed_games = list(request.user.followed_games.values('id'))
    
    games_data = {
        "game_events": igdb_data["game_events"],
        "followed_games": followed_games
        }
    return JsonResponse(games_data)

@login_required
def wishlist(request):
    followed_games = request.user.followed_games.all()
    return render(request, "vid_man/wishlist.html", {"followed_games": followed_games})

@login_required
def game_detail(request, game_id):
    game_data = Games_Data.objects.get(id=game_id)
    is_followed = game_data in request.user.followed_games.all()
    return render(request, "vid_man/game_detail.html", {"game_data": game_data, "is_followed": is_followed})

@login_required
def follow_game(request, game_id):
    if request.method == "POST":
        game = get_object_or_404(Games_Data, id=game_id)
        
        if game in request.user.followed_games.all():
            request.user.followed_games.remove(game)
            return JsonResponse({"status": "unfollowed"})
        
        else:
            request.user.followed_games.add(game)
            return JsonResponse({"status": "followed"})
    return JsonResponse({"status": "fail"}, status=405)

@login_required
def search_games(request):
    query = request.GET.get('q','')
    games = Games_Data.objects.filter(name__icontains = query)
    game_list = [{'id': game.id, 'name': game.name} for game in games]
    return JsonResponse({'games': game_list})

