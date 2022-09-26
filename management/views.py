from django.shortcuts import render

# Create your views here.

def error_400(request, exception):
	return render(request,'management/400.html', {})

def error_403(request, exception):
    return render(request,'management/403.html', {})


def error_404(request, exception):
    return render(request,'management/404.html', {})

def error_500(request):
    return render(request,'management/500.html', {})
