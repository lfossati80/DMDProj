# Generic Python imports
import json, mimetypes, os, urllib

# Django imports
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# geopy imports
from geopy.distance import vincenty
from geopy.point import Point

# Project specific imports
from .models import Location
from .forms import LocationForm

# The index view shows a form asking for the search parameters
def index(request):

    # If this is a POST request we process the form data
    if request.method == 'POST':

        # If Clear button was pressed, clear form and return
        if 'clear' in request.POST:
            form = LocationForm()
            return render(request, 'findshop/index.html', {'form': form})

        # Otherwise, start data processing 
        form = LocationForm(request.POST)

        # First, check if form is valid
        if form.is_valid():

            query_result_obj = Location.objects.all()

            # If a category was provided, filter against it
            if form.cleaned_data['category']:
                query_result_obj = query_result_obj.filter(category=form.cleaned_data['category'])

            # For each location in the db, check if distance is within radius
            for loc in query_result_obj:
                p1 = Point(latitude=loc.latitude, longitude=loc.longitude)
                p2 = Point(latitude=form.cleaned_data['latitude'], longitude=form.cleaned_data['longitude'])
                geodist = vincenty(p1,p2).meters
                if geodist > form.cleaned_data['radius']:
                    query_result_obj = query_result_obj.exclude(pk = loc.pk)

            # Select only number of results specified (at random, no particular order required)
            query_result_obj = query_result_obj.all()[:form.cleaned_data['count']]

            # Pack results in session and pass control to download view
            result_list = list(query_result_obj.values())
            request.session['result_json'] = result_list
            return HttpResponseRedirect(reverse('download'))

    # if GET or any other method, create a blank form
    else:
        form = LocationForm()

    return render(request, 'findshop/index.html', {'form': form})


# The download view returns a Json file with the locations that match the search criteria
def download(request):

    # If a Json doc was passed, perform download 
    if 'result_json' in request.session:

        result_list = request.session.get('result_json')

        try:
            del request.session['result_json']
        except KeyError:
            pass

        # Create file and dump Json data in it
        original_filename = 'data.json'
        file_path = './' + original_filename
        with open('data.json', 'w') as outfile:
            json.dump(result_list, outfile)
        outfile.close()

        # Re-open file in read mode and format response
        outfile = open(file_path, 'rb')
        response = HttpResponse(outfile.read())
        outfile.close()
        type, encoding = mimetypes.guess_type(original_filename)
        if type is None:
            type = 'application/octet-stream'
        response['Content-Type'] = type
        response['Content-Length'] = str(os.stat(file_path).st_size)
        if encoding is not None:
            response['Content-Encoding'] = encoding

        # Format header differently for each browser
        if u'WebKit' in request.META['HTTP_USER_AGENT']:
            # Safari 3.0 and Chrome 2.0 accepts UTF-8 encoded string directly.
            filename_header = 'filename=%s' % original_filename.encode('utf-8')
        elif u'MSIE' in request.META['HTTP_USER_AGENT']:
            # IE does not support internationalized filename at all.
            # It can only recognize internationalized URL, so we do the trick via routing rules.
            filename_header = ''
        else:
            # For others like Firefox, we follow RFC2231 (encoding extension in HTTP headers).
            filename_header = 'filename*=UTF-8\'\'%s' % urllib.parse.quote(original_filename.encode('utf-8'))
        response['Content-Disposition'] = 'attachment; ' + filename_header
        return response

    # if 'result_json' did not come through, or in case anything else went wrong, render new form
    form = LocationForm()
    return render(request, 'findshop/index.html', {'form': form})




