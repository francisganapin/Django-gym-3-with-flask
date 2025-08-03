from django.shortcuts import render


def bmi_calculator(request):
    bmi = None
    weight_kg = ''
    height_cm = ''

    if request.method == 'POST':
        try:
            height_cm = float(request.POST.get('height_cm'))
            weight_kg = float(request.POST.get('weight_kg'))
            height_m = height_cm / 100
            bmi = round(weight_kg / (height_m  ** 2),2)
        except:  
            bmi = 'Invalid input'
    return render(request,'fitness/bmi.html',{'bmi':bmi})
