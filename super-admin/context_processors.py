from django.shortcuts import render, redirect

def add_variable_to_context(request):
    user = request.user
    return {
        'user': user
    }