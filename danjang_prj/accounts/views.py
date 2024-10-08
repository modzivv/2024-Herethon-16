from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from portfolios.models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from itertools import groupby


def comming_soon(request):
    return render(request, 'accounts/comming_soon.html')

def index(request):
    return render(request, 'accounts/index.html')

def signup_view(request):
    if request.method == "GET":
        form = SignUpForm()
        return render(request, 'accounts/signup.html', {'form' : form})

    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save()
        return redirect('accounts:login')
    else:
        return render(request, 'accounts/signup.html', {'form' : form})

def login_view(request):
    if request.method == "GET":
        return render(request, 'accounts/login.html', {'form' : AuthenticationForm})

    form = AuthenticationForm(request, data = request.POST)
    if form.is_valid():
        login(request, form.user_cache)
        return redirect('videos:video_list')
    return render(request, 'accounts/login.html', {'form' : form})

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('accounts:index')

@login_required
def mypage(request):
    # 찜
    likes = Like.objects.filter(user=request.user).order_by('-created_at')
    videos = [like.video for like in likes][:3]
    # 시청기록
    myhistories = WatchHistory.objects.filter(user=request.user).order_by('-watched_at')
    seen_videos = set()
    unique_histories = []
    for history in myhistories:
        if history.video.id not in seen_videos:
            unique_histories.append(history)
            seen_videos.add(history.video.id)
    try:
        myportfolio = Portfolio.objects.get(user=request.user)
        return render(request, 'accounts/mypage.html', {'myportfolio' : myportfolio, 'likes' : likes, 'videos' : videos, 'myhistories': unique_histories, "watch_videos" : [history.video for history in unique_histories]})
    except Portfolio.DoesNotExist:
        return render(request, 'accounts/mypage.html', {'likes' : likes, 'videos' : videos, 'myhistories': unique_histories, "watch_videos" : [history.video for history in unique_histories]})

@login_required
def mypage_image_update(request, id):
    User = get_user_model()
    user = User.objects.get(id=id)

    if request.method == "POST":
        mypage_image = request.FILES.get('mypage_image')
        if mypage_image:
            user.mypage_image.delete()
            user.mypage_image = mypage_image       
        user.save()
        return redirect('accounts:mypage')
    return render(request, 'accounts/mypage.html', {'user' : user})

@login_required
def create_myportfolio(request):
    roles = Role.objects.all()

    if request.method == "POST":
        name = request.POST.get('name')
        profile_photo = request.FILES.get('profile_photo')
        email = request.POST.get('email')
        one_line = request.POST.get('one_line')
        intro = request.POST.get('intro')

        role_ids = request.POST.getlist('role')
        role_list = [get_object_or_404(Role, id = role_id) for role_id in role_ids]

        portfolios = Portfolio.objects.create(
            name = name,
            profile_photo = profile_photo,
            email = email,
            one_line = one_line,
            intro = intro,
            user = request.user,
        )

        for role in role_list:
            portfolios.role.add(role)

        return redirect('accounts:mypage')
    return render(request, 'accounts/create_myportfolio.html', {'roles' : roles})

@login_required
def create_my_career(request):
    if request.method == 'POST':
        Career.objects.create(
            user=request.user,
            portfolio=Portfolio.objects.get(user=request.user),
            career_title = request.POST.get('career_title'),
            career_role = request.POST.get('career_role'),
            career_year = request.POST.get('career_year'),
        )
        return redirect('accounts:update_myportfolio')
    return render(request, 'accounts:update_myportfolio.html')

@login_required
def delete_my_career(request, id):
    my_career = get_object_or_404(Career, id = id)
    my_career.delete()
    return redirect('accounts:update_myportfolio')

@login_required
def update_myportfolio(request):
    if request.method == "GET":
        myportfolio = Portfolio.objects.get(user=request.user)
        roles = Role.objects.all()

        # 사용자의 포트폴리오에 해당하는 모든 사진과 동영상을 가져옴
        photos = Photo.objects.filter(portfolio__user=request.user)
        videos = Video.objects.filter(portfolio__user=request.user)
        posts = list(photos) + list(videos)  # 두 쿼리셋을 합칩니다.

        careers = Career.objects.filter(portfolio__user=request.user)

        return render(request, 'accounts/update_myportfolio.html', {'myportfolio': myportfolio, 'roles': roles, 'posts':posts, 'careers':careers})
    elif request.method == "POST":
        myportfolio = Portfolio.objects.get(user=request.user)
        myportfolio.name = request.POST.get('name')
        #전문 분야
        role_ids = request.POST.getlist('role')
        role_list = [get_object_or_404(Role, id=role_id) for role_id in role_ids]
        myportfolio.role.set(role_list)
        #프로필 이미지
        profile_photo = request.FILES.get('profile_photo')
        myportfolio.email = request.POST.get('email')
        myportfolio.one_line = request.POST.get('one_line')
        myportfolio.intro = request.POST.get('intro')

        if profile_photo:
            myportfolio.profile_photo.delete()
            myportfolio.profile_photo = profile_photo

        myportfolio.save()
        return redirect('accounts:update_myportfolio')

@login_required
def create_my_video(request):
    if request.method == 'POST':
        video = request.FILES.get('video')
        if video:
            Video.objects.create(
                user=request.user,
                video=video,
                portfolio=Portfolio.objects.get(user=request.user),
                title=request.POST.get('title'),
                cast=request.POST.get('cast'),
                staff=request.POST.get('staff'),
                keyword=request.POST.get('keyword'),
                synopsis=request.POST.get('synopsis'),
            )
        return redirect('accounts:update_myportfolio')
    return render(request, 'accounts/create_my_video.html')

@login_required
def delete_my_video(request, id):
    video = get_object_or_404(Video, id = id)
    video.delete()
    return redirect('accounts:update_myportfolio')

@login_required
def delete_my_photo(request, id):
    photo = get_object_or_404(Photo, id = id)
    photo.delete()
    return redirect('accounts:update_myportfolio')

@login_required
def update_my_video(request, id):
    post = get_object_or_404(Video, id = id)
    if request.method == "POST":
        post.title = request.POST.get('title')
        post.cast = request.POST.get('cast')
        post.staff = request.POST.get('staff')
        post.keyword = request.POST.get('keyword')
        post.synopsis = request.POST.get('synopsis')
        video = request.FILES.get('video')

        if video:
            post.video.delete()
            post.video = video

        post.save()
        return redirect('accounts:update_myportfolio')
    return render(request, 'accounts/update_my_video.html', {'post':post})

# 내 찜
@login_required
def mylike(request):
    likes = Like.objects.filter(user=request.user).order_by('-created_at')
    videos = [like.video for like in likes]
    return render(request, 'accounts/mylike.html', {"likes" : likes, "videos" : videos})

# 기록
@login_required
def myviewhistory(request):
    # 모든 기록을 가져오지만, 중복 제거를 위해 Python에서 필터링
    myhistories = WatchHistory.objects.filter(user=request.user).order_by('-watched_at')

    # 중복된 비디오 제거를 위해 비디오 ID를 추적
    seen_videos = set()
    unique_histories = []

    for history in myhistories:
        if history.video.id not in seen_videos:
            unique_histories.append(history)
            seen_videos.add(history.video.id)

    return render(request, 'accounts/myviewhistory.html', {'myhistories': unique_histories, "watch_videos" : [history.video for history in unique_histories]})