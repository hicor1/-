from django.shortcuts import  render


# 400에러(error)
def error_400(request, exception):
    templates = 'app/error_400_page.html'
    context = {'':''}
    return render(request, templates, context)

# 404에러(error)
def error_404(request, exception):
    templates = 'app/error_404_page.html'
    context = {'':''}
    return render(request, templates, context)

# 500에러(error)
def error_500(request):
    templates = 'app/error_500_page.html'
    context = {'':''}
    return render(request, templates, context)