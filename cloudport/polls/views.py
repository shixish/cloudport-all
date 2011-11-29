# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.template import RequestContext
from cloudport.polls.forms import *
import datetime

def time(request):
    now = datetime.datetime.now()
    img = "http://www.eyedesignbook.com/ch3/fig3-61retinarods-conesBIG.jpg"
    #html="<html><body><form>First name: <input type=\"text\" name=\"firstname\" /><br /></form> Date and time today : %s.<br><img src=\"%s\" \> </body></html>" % (now,"http://www.eyedesignbook.com/ch3/fig3-61retinarods-conesBIG.jpg ")
    #return HttpResponse(html)
    return render_to_response('time.html', {'time':now,'img':img} )

#def try(request):
   # html="<html><body><form>First name: <input type="text" name="FirstName"/><br />Last name: <input type="text" name="LastName"/><br /><input type="submit" value="Submit" /> </form></body></html>"
  # return HttpResponse(html)
