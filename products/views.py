from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic

class indexView(generic.ListView):
    template_name = "polls/index.html"
    def get_queryset(self):
        return HttpResponse("You are at products index")