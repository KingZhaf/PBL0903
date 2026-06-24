from django.shortcuts import render, redirect
from django.urls import reverse
import requests
import json


def safe_get_json(url, expect_single=False, timeout=3):
    """Fetch `url` and return parsed JSON. On error return [] or {} based on expect_single.
    Logs a warning to stdout for debugging.
    """
    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"Warning: could not fetch {url}: {e}")
        return {} if expect_single else []


def safe_post(url, data=None, headers=None, timeout=3):
    try:
        resp = requests.post(url, data=data, headers=headers, timeout=timeout)
        resp.raise_for_status()
        return resp
    except Exception as e:
        print(f"Warning: POST to {url} failed: {e}")
        return None


def safe_put(url, data=None, headers=None, timeout=3):
    try:
        resp = requests.put(url, data=data, headers=headers, timeout=timeout)
        resp.raise_for_status()
        return resp
    except Exception as e:
        print(f"Warning: PUT to {url} failed: {e}")
        return None


def safe_delete(url, timeout=3):
    try:
        resp = requests.delete(url, timeout=timeout)
        resp.raise_for_status()
        return resp
    except Exception as e:
        print(f"Warning: DELETE to {url} failed: {e}")
        return None

def get_server_url(ms):
    """Return the base URL for the given microservice."""
    servers = {
        'MS1': 'http://localhost:5051',
        'MS2': 'http://localhost:5052',
        'MS3': 'http://localhost:5053'
    }
    return servers.get(ms, 'http://localhost:5051')

def get_db_name(ms):
    """Return the database name for the given microservice."""
    if ms in ['MS1', 'MS2']:
        return 'DB-A'
    return 'DB-B'

def masukkeindeks(request):
    # Try to fetch car lists from MS1 (DB-A) and MS3 (DB-B).
    # If a service is down or refuses connection, continue and show an empty list
    # instead of raising a server error.
    alamatserver_ms1_dba = "http://localhost:5051/cars/"
    alamatserver_ms3_dbb = "http://localhost:5053/cars/"

    rows_dba = []
    rows_dbb = []

    try:
        resp = requests.get(alamatserver_ms1_dba, timeout=3)
        resp.raise_for_status()
        rows_dba = resp.json()
    except Exception as e:
        # Log to console for developer debugging; render page with empty data.
        print(f"Warning: could not fetch MS1 data: {e}")

    try:
        resp = requests.get(alamatserver_ms3_dbb, timeout=3)
        resp.raise_for_status()
        rows_dbb = resp.json()
    except Exception as e:
        print(f"Warning: could not fetch MS3 data: {e}")

    return render(request, 'index.html', {'rows_dba': rows_dba, 'rows_dbb': rows_dbb})

def ms1(request):
    servermana = 'MS1'
    alamatserver = "http://localhost:5051/cars/"
    rows = safe_get_json(alamatserver)
    return render(request, 'indexms.html', {'rows': rows, 'servermana': servermana, 'DB': 'DB-A'})

def ms2(request):
    servermana = 'MS2'
    alamatserver = "http://localhost:5052/cars/"
    rows = safe_get_json(alamatserver)
    return render(request, 'indexms.html', {'rows': rows, 'servermana': servermana, 'DB': 'DB-A'})

def ms3(request):
    servermana = 'MS3'
    alamatserver = "http://localhost:5053/cars/"
    rows = safe_get_json(alamatserver)
    return render(request, 'indexms.html', {'rows': rows, 'servermana': servermana, 'DB': 'DB-B'})

def createcar(request, ms):
    try:
        return render(request, 'createcar.html', {'servermana': ms})
    except:
        ms = 'MS1'
        return render(request, 'createcar.html', {'servermana': ms})

def createcarsave_ms1(request):
    if request.method == 'POST':
        fName = request.POST.get('carName', '')
        fBrand = request.POST.get('carBrand', '')
        fModel = request.POST.get('carModel', '')
        fPrice = request.POST.get('carPrice', '')
        fdesc = "input from appx to MS1"

        datacar = {
            "carname": fName,
            "carbrand": fBrand, 
            "carmodel": fModel,
            "carprice": fPrice,
            "description": fdesc
        }
        
        datacar_json = json.dumps(datacar)
        alamatserver = "http://localhost:5051/cars/"
        headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
        resp = safe_post(alamatserver, data=datacar_json, headers=headers)
        if resp is None:
            # Backend unreachable — log and continue without raising
            print(f"Warning: createcarsave_ms1 could not reach {alamatserver}")

    return redirect('ms1')

def createcarsave_ms2(request):
    if request.method == 'POST':
        fName = request.POST.get('carName', '')
        fBrand = request.POST.get('carBrand', '')
        fModel = request.POST.get('carModel', '')
        fPrice = request.POST.get('carPrice', '')
        fdesc = "input from appx to MS2"

        datacar = {
            "carname": fName,
            "carbrand": fBrand, 
            "carmodel": fModel,
            "carprice": fPrice,
            "description": fdesc
        }
        
        datacar_json = json.dumps(datacar)
        alamatserver = "http://localhost:5052/cars/"
        headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
        resp = safe_post(alamatserver, data=datacar_json, headers=headers)
        if resp is None:
            print(f"Warning: createcarsave_ms2 could not reach {alamatserver}")

    return redirect('ms2')

def createcarsave_ms3(request):
    if request.method == 'POST':
        fName = request.POST.get('carName', '')
        fBrand = request.POST.get('carBrand', '')
        fModel = request.POST.get('carModel', '')
        fPrice = request.POST.get('carPrice', '')
        fdesc = "input from appx to MS3"

        datacar = {
            "carname": fName,
            "carbrand": fBrand, 
            "carmodel": fModel,
            "carprice": fPrice,
            "description": fdesc
        }
        
        datacar_json = json.dumps(datacar)
        alamatserver = "http://localhost:5053/cars/"
        headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
        resp = safe_post(alamatserver, data=datacar_json, headers=headers)
        if resp is None:
            print(f"Warning: createcarsave_ms3 could not reach {alamatserver}")

    return redirect('ms3')

def readcar(request, ms):
    if ms in ['MS1', 'MS2']:
        alamatserver = "http://localhost:5051/cars/"
        rows = safe_get_json(alamatserver)
        return render(request, 'readcar.html', {'rows': rows, 'servermana': ms, 'DB': 'DB-A'})

    elif ms in ['MS3']:
        alamatserver = "http://localhost:5053/cars/"
        rows = safe_get_json(alamatserver)
        return render(request, 'readcar.html', {'rows': rows, 'servermana': ms, 'DB': 'DB-B'})
    
    return redirect('masukkeindeks')

def updatecar(request, ms):
    server_url = get_server_url(ms)
    alamatserver = server_url + "/cars/"
    rows = safe_get_json(alamatserver)
    db_name = get_db_name(ms)
    return render(request, 'updatecar.html', {'rows': rows, 'servermana': ms, 'DB': db_name})

def updatecarform(request, ms, car_id):
    server_url = get_server_url(ms)
    alamatserver = server_url + "/cars/" + str(car_id)
    car = safe_get_json(alamatserver, expect_single=True)
    db_name = get_db_name(ms)
    return render(request, 'updatecarform.html', {'car': car, 'servermana': ms, 'DB': db_name})

def updatecarsave(request, ms, car_id):
    if request.method == 'POST':
        fName = request.POST.get('carName', '')
        fBrand = request.POST.get('carBrand', '')
        fModel = request.POST.get('carModel', '')
        fPrice = request.POST.get('carPrice', '')
        fdesc = "updated from appx via " + ms

        datacar = {
            "carname": fName,
            "carbrand": fBrand,
            "carmodel": fModel,
            "carprice": fPrice,
            "description": fdesc
        }

        datacar_json = json.dumps(datacar)
        server_url = get_server_url(ms)
        alamatserver = server_url + "/cars/" + str(car_id)

        headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
        resp = safe_put(alamatserver, data=datacar_json, headers=headers)
        if resp is None:
            print(f"Warning: updatecarsave could not reach {alamatserver}")

    return redirect('updatecar', ms=ms)

def deletecar(request, ms):
    server_url = get_server_url(ms)
    alamatserver = server_url + "/cars/"
    rows = safe_get_json(alamatserver)
    db_name = get_db_name(ms)
    return render(request, 'deletecar.html', {'rows': rows, 'servermana': ms, 'DB': db_name})

def deletecarsave(request, ms, car_id):
    if request.method == 'POST':
        server_url = get_server_url(ms)
        alamatserver = server_url + "/cars/" + str(car_id)
        resp = safe_delete(alamatserver)
        if resp is None:
            print(f"Warning: deletecarsave could not reach {alamatserver}")

    return redirect('deletecar', ms=ms)

def searchcar(request, ms):
    db_name = get_db_name(ms)
    return render(request, 'searchcar.html', {'rows': [], 'servermana': ms, 'DB': db_name, 'query': ''})

def searchcarsave(request, ms):
    query = request.POST.get('searchQuery', '') if request.method == 'POST' else request.GET.get('q', '')

    server_url = get_server_url(ms)
    alamatserver = server_url + "/cars/search?q=" + query
    rows = safe_get_json(alamatserver)
    db_name = get_db_name(ms)

    return render(request, 'searchcar.html', {'rows': rows, 'servermana': ms, 'DB': db_name, 'query': query})
