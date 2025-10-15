from django.shortcuts import render


def bmi_calculator(request):
    bmi = None
    weight_kg = ''
    height_cm = ''
    category = ''

    if request.method == 'POST':
        try:
            height_cm = float(request.POST.get('height_cm'))
            weight_kg = float(request.POST.get('weight_kg'))
            height_m = height_cm / 100
            bmi = round(weight_kg / (height_m  ** 2),2)

            if bmi < 18.5:
                category = 'Underweight'
            elif 18.5 <= bmi < 24.9:
                category = 'Normal weight'
            elif 25 <= bmi < 29.9:
                category = 'Overweight'
            else:
                category = 'Obese'
        except:  
            bmi = 'Invalid input'
            category = ''

    print(bmi)

    return render(request,'fitness/bmi.html',{'bmi':bmi,'category':category,'weight_kg':weight_kg,'height_cm':height_cm})


def bmr_calculator(request):
    bmr = None
    tdee = None
    weight_kg = ''
    height_cm = ''
    age = ''
    gender = ''
    activity  = ''

    if request.method == 'POST':
        try:
            weight_kg = float(request.POST.get('weight_kg'))
            height_cm = float(request.POST.get('height_cm'))
            age = int(request.POST.get('age'))
            gender = request.POST.get('gender')
            activity = request.POST.get('activity')

            if gender == 'male':
                bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
            elif gender == 'female':
                bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

            
            factors = {
                '1.2':'Sedentary',
                '1.375':'Light Active',
                '1.55':'Moderately Active',
                '1.725':'Very Active',
                '1.9':'Extra Active'
            }

            tdee = round(bmr * float(activity),2)
        
        except Exception as e:
            bmr = 'Invalid input'
            print(e)


    context = {
        'bmr':bmr,
        'tdee':tdee,
        'weight_kg':weight_kg,
        'height_cm':height_cm,
        'age':age,
        'gender':gender,
        'activity':activity
    }

    return render(request,'fitness/bmr.html',context)