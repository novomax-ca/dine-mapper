from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Marker
from .forms import MarkerForm, CustomUserCreationForm, LoginForm
from django.conf import settings
from django.core import serializers
import json


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('home')
            except Exception as e:
                form.add_error(None, str(e))

    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def home(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()

    marker_form = MarkerForm()

    return render(request, 'map/map_page.html', {
        'form': form,
        'marker_form': marker_form,
        'mapbox_access_token': settings.MAPBOX_ACCESS_TOKEN,
        'google_maps_api_key': settings.GOOGLE_API_KEY
    })


def get_markers(request):
    offset = int(request.GET.get('offset', 0))
    markers = Marker.objects.all().order_by('-pk')[offset:offset+20]
    markers_json = serializers.serialize('json', markers)

    return JsonResponse(markers_json, safe=False)


def add_marker(request):
    print(request.POST)
    print(request.FILES)
    try:
        if request.method == 'POST':
            form = MarkerForm(request.POST, request.FILES)
            if form.is_valid():
                marker = form.save(commit=False)
                marker.user = request.user
                marker.save()

                marker_json = serializers.serialize('json', [marker])

                return JsonResponse({'status': 'success', 'message': 'Marker added successfully', 'data': marker_json})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid form data', 'errors': form.errors}, status=400)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid REQUEST'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def delete_marker(request, marker_id):
    try:
        if request.method == 'DELETE':
            print(marker_id)
            marker = Marker.objects.get(pk=marker_id)
            if marker.user == request.user:
                marker.delete()
                return JsonResponse({'status': 'success', 'message': 'Marker deleted successfully'})
            else:
                return JsonResponse({'status': 'error', 'message': 'You are not authorized to delete this marker'}, status=403)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid REQUEST'}, status=400)
    except Marker.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Marker not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def load_marker_form(request) -> HttpResponse:
    form = MarkerForm()
    return render(request, 'fragments/form_add_marker.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')
