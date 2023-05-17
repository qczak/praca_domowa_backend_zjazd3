from django.db.models import Count, Avg
from django.db.models.functions import TruncDate, TruncMonth, TruncDay
from django.shortcuts import render, redirect
from .models import Measurement

# Create your views here.
def measurements_all(request):
    measurements = Measurement.objects.order_by('measured_date')

    return render(request,'measurements/measurements_all.html', {'measure':measurements})

def measurement_list(request):
    measurements = Measurement.objects.all()

    return render(request,'measurements/measurement_list.html', {'measure':measurements})

def measurement_detail(request, id):
    measurement = Measurement.objects.get(id=id)
    return render(request,'measurements/measurement_detail.html', {'measurement':measurement})


def chart(request):
    ''' wykres dla każdego dnia (z powtórkami).'''
    measurements = Measurement.objects.order_by('measured_date')
    values = []
    labels = []
    for m in measurements:
        date = m.measured_date.strftime("%Y-%m-%d")
        labels.append(date)
        values.append(m.value)
    context = {'labels': labels, 'values': values}

    return render(request, 'measurements/chart.html', context)

def chart_avr(request):
    '''wykres z unkatowymi dniami, oblicza średniąwartość dla każdego dnia.'''
    measurements = Measurement.objects.order_by('measured_date').values('measured_date').annotate(Avg('value'))   #układa dniami, wybiera unikatowe dni, wylicza średnią wartość dla każdego dnia
    value = {}
    for m in measurements:
        date = m['measured_date'].strftime("%Y-%m-%d")
        value[date] = m['value__avg']
    labels, values = zip(*value.items())
    context = {'labels': labels, 'values': values}

    return render(request, 'measurements/chart_avr.html', context)

def delete(request, id):
    measurement = Measurement.objects.get(id=id)
    print(request)
    if request.method == 'POST':
        # measurement_id = request.POST.get('id')
        if request.POST.get('action') == 'delete':
            # kod usuwający pomiar o identyfikatorze id
            measurement.delete()
            return redirect('/')

        elif request.POST.get('action') == 'back':
            # kod przekierowujący użytkownika na stronę główną
            return redirect('/')

    return render(request,'measurements/delete.html', {'measurement':measurement})

