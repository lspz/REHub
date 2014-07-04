from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
# from django.contrib.auth import get_user_model
# from django.http import HttpResponseRedirect, Http404
# from django.contrib.auth import logout
# from django.contrib.auth.decorators import login_required, user_passes_test

def home(request):
  return render_to_response('index.html', {}, RequestContext(request))    