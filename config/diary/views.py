from django.shortcuts import render, get_object_or_404, redirect
from .models import Diary
from .forms import DiaryForm
from django.contrib.auth.decorators import login_required

import logging

logger = logging.getLogger(__name__)

@login_required
def create_diary(request):
    if request.method == 'POST':
        form = DiaryForm(request.POST)
        if form.is_valid():
            diary = form.save(commit=False)
            diary.user = request.user
            diary.save()
            return redirect('image_select',pk=diary.pk) 
    else:
        form = DiaryForm()

    return render(request, 'create_diary.html', {'form': form})

@login_required
def diary_list(request):
    diaries = Diary.objects.filter(user=request.user)
    return render(request, 'diary_list.html', {'diaries': diaries})

@login_required
def view_diary(request, pk):
    user = request.user
    diary = get_object_or_404(Diary, pk=pk, user=user)
    return render(request, 'view_diary.html', {'diary': diary})

@login_required
def edit_diary(request, pk):
    user = request.user
    diary = get_object_or_404(Diary, pk=pk, user=user)

    if request.method == 'POST':
        form = DiaryForm(request.POST, instance=diary)
        if form.is_valid():
            form.save()
            return redirect('diary_list')  
    else:
        form = DiaryForm(instance=diary)

    return render(request, 'edit_diary.html', {'form': form, 'diary': diary})

@login_required
def delete_diary(request, pk):
    user = request.user
    diary = get_object_or_404(Diary, pk=pk, user=user)

    if request.method == 'POST':
        diary.delete()
        return redirect('diary_list') 
    return render(request, 'delete_diary.html', {'diary': diary})