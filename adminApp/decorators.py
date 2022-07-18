from django.shortcuts import redirect, render, HttpResponse


def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_superuser == True:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('home')
    return wrapper_func


def admin_redirect(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_superuser == True:
            return redirect('adminHome')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func