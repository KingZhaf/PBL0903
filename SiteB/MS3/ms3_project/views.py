import json
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import TBCarsWeb

def index_view(request):
    return HttpResponse("MS3 Server Ready")

@csrf_exempt
def cars_view(request):
    if request.method == 'GET':
        rows = TBCarsWeb.objects.all()
        datas = []
        for row in rows:
            datas.append({
                'id': row.id,
                'carname': row.carname,
                'carbrand': row.carbrand,
                'carmodel': row.carmodel,
                'carprice': row.carprice,
                'description': row.description
            })
        return JsonResponse(datas, safe=False)

    elif request.method == 'POST':
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)

        fName = body.get('carname')
        fBrand = body.get('carbrand')
        fModel = body.get('carmodel')
        fPrice = body.get('carprice')
        fDescription = body.get('description')

        # Create in default (DB-B)
        TBCarsWeb.objects.create(
            carname=fName,
            carbrand=fBrand,
            carmodel=fModel,
            carprice=fPrice,
            description=fDescription
        )
        # Also mirror into DB-A
        try:
            TBCarsWeb.objects.using('db_a').create(
                carname=fName,
                carbrand=fBrand,
                carmodel=fModel,
                carprice=fPrice,
                description=fDescription
            )
        except Exception:
            pass

        rows = TBCarsWeb.objects.all()
        datas = []
        for row in rows:
            datas.append({
                'id': row.id,
                'carname': row.carname,
                'carbrand': row.carbrand,
                'carmodel': row.carmodel,
                'carprice': row.carprice,
                'description': row.description
            })
        return JsonResponse(datas, safe=False)

    return HttpResponseNotAllowed(['GET', 'POST'])

@csrf_exempt
def car_detail_view(request, car_id):
    try:
        car = TBCarsWeb.objects.get(id=car_id)
    except TBCarsWeb.DoesNotExist:
        return JsonResponse({'message': 'Car not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse({
            'id': car.id,
            'carname': car.carname,
            'carbrand': car.carbrand,
            'carmodel': car.carmodel,
            'carprice': car.carprice,
            'description': car.description
        })

    elif request.method == 'PUT':
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)

        # Update primary record in default DB
        old_values = {
            'carname': car.carname,
            'carbrand': car.carbrand,
            'carmodel': car.carmodel,
            'carprice': car.carprice,
            'description': car.description,
        }
        car.carname = body.get('carname', car.carname)
        car.carbrand = body.get('carbrand', car.carbrand)
        car.carmodel = body.get('carmodel', car.carmodel)
        car.carprice = body.get('carprice', car.carprice)
        car.description = body.get('description', car.description)
        car.save()

        # Best-effort mirror update to DB-A
        try:
            match = TBCarsWeb.objects.using('db_a').filter(
                carname=old_values['carname'],
                carbrand=old_values['carbrand'],
                carmodel=old_values['carmodel'],
                carprice=old_values['carprice'],
            ).first()
            if match:
                match.carname = car.carname
                match.carbrand = car.carbrand
                match.carmodel = car.carmodel
                match.carprice = car.carprice
                match.description = car.description
                match.save(using='db_a')
        except Exception:
            pass

        return JsonResponse({
            'id': car.id,
            'carname': car.carname,
            'carbrand': car.carbrand,
            'carmodel': car.carmodel,
            'carprice': car.carprice,
            'description': car.description
        })

    elif request.method == 'DELETE':
        old_values = {
            'carname': car.carname,
            'carbrand': car.carbrand,
            'carmodel': car.carmodel,
            'carprice': car.carprice,
        }
        car.delete()
        try:
            TBCarsWeb.objects.using('db_a').filter(
                carname=old_values['carname'],
                carbrand=old_values['carbrand'],
                carmodel=old_values['carmodel'],
                carprice=old_values['carprice'],
            ).delete()
        except Exception:
            pass
        return JsonResponse({'message': 'Car deleted successfully'}, status=200)

    return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])

def car_search_view(request):
    if request.method == 'GET':
        query = request.GET.get('q', '')
        rows = TBCarsWeb.objects.filter(
            Q(carname__icontains=query) |
            Q(carbrand__icontains=query) |
            Q(carmodel__icontains=query)
        )
        datas = []
        for row in rows:
            datas.append({
                'id': row.id,
                'carname': row.carname,
                'carbrand': row.carbrand,
                'carmodel': row.carmodel,
                'carprice': row.carprice,
                'description': row.description
            })
        return JsonResponse(datas, safe=False)

    return HttpResponseNotAllowed(['GET'])
