import requests
from django.shortcuts import redirect, render
from django.urls import reverse



def survivors(request):
    response = requests.get('http://127.0.0.1:8000/api/survivors/')
    survivors = response.json()
    context = {'survivors': survivors}
    return render(request, 'interface/survivors.html', context)


def survivor_detail(request, pk):
    response = requests.get(f'http://127.0.0.1:8000/api/survivors/{pk}/')
    survivor = response.json()

    response = requests.get(f'http://127.0.0.1:8000/api/survivors/')
    survivors = response.json()


    context = {'survivor': survivor, 'survivors': survivors}
    return render(request, 'interface/survivor_detail.html', context)


def resources_report(request):
    response = requests.get(
        'http://127.0.0.1:8000/api/survivors/get_resources_report/'
    )
    context = {'report': response.json()}
    return render(request, 'interface/resources_report.html', context)


def report_infected(request, pk):
    data = {
        'survivor_reported': request.POST.get('survivor_reported'),
    }
    response = requests.put(
        f'http://127.0.0.1:8000/api/survivors/{pk}/report_infected/', json=data
    )
    return redirect(reverse('interface:survivor_detail', kwargs={'pk': pk}))


def update_location(request, pk):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        data = {'latitude': latitude, 'longitude': longitude}
        requests.patch(f'http://127.0.0.1:8000/api/survivors/{pk}/', data=data)
        return redirect(
            reverse('interface:survivor_detail', kwargs={'pk': pk})
        )
    response = requests.get(f'http://127.0.0.1:8000/api/survivors/{pk}/')
    survivor = response.json()
    return render(
        request, 'interface/update_location.html', {'survivor': survivor}
    )


def add_survivor(request):
    if request.method == 'POST':
        data = {
            'name': request.POST.get('name'),
            'age': request.POST.get('age'),
            'gender': request.POST.get('gender'),
            'latitude': request.POST.get('latitude'),
            'longitude': request.POST.get('longitude'),
            'water': request.POST.get('water'),
            'food': request.POST.get('food'),
            'medication': request.POST.get('medication'),
            'ammunition': request.POST.get('ammunition'),
            'is_infected': request.POST.get('is_infected', False),
            'total_points': 0,
            'received_reports': 0,
        }
        requests.post('http://127.0.0.1:8000/api/survivors/', data=data)
        return redirect(reverse('interface:survivors'))
    return render(request, 'interface/add_survivor.html')


def make_trade(request, pk):
    if request.method == 'POST':
        data = {
            'survivor1': pk,
            'survivor2': request.POST['survivor2'],
            'survivor1_items': request.POST.getlist('survivor1_items'),
            'survivor2_items': request.POST.getlist('survivor2_items'),
        }

        requests.post(
            f'http://127.0.0.1:8000/api/survivors/make_trade/', data=data
        )
        return redirect(
            reverse('interface:survivor_detail', kwargs={'pk': pk})
        )

    response = requests.get(f'http://127.0.0.1:8000/api/survivors/{pk}/')
    survivor1 = response.json()

    response = requests.get(
        f'http://127.0.0.1:8000/api/survivors/{request.GET["survivor2"]}/'
    )
    survivor2 = response.json()

    context = {'survivor1': survivor1, 'survivor2': survivor2}
    return render(request, 'interface/make_trade.html', context)
