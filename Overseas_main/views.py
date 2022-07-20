from django.shortcuts import render
from django.http import HttpResponse
from .models import User
from math import ceil
import pandas as pd
import pickle
from datetime import datetime


def index(request):
    return render(request, 'index.html')
    # users = User.objects.all().values()
    # output = ""
    # for x in users:
    #     output+=x['firstname']
    # return HttpResponse(output)


def predict(request):
    # if request.method != "POST":
    #     return render(request,'prediction.html')
    model = pickle.load(open("./Overseas_main/models/flight_rf.pkl", "rb"))
    # Date_of_Journey
    #date_dep = request.form["Dep_Time"]
    date_dep = request.POST['Dep_Time']
    Journey_day = int(pd.to_datetime(date_dep, format="%Y-%m-%d").day)
    Journey_month = int(pd.to_datetime(date_dep, format="%Y-%m-%d").month)
    # print("Journey Date : ",Journey_day, Journey_month)

    # Departure
    #Dep_hour = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").hour)
    #Dep_min = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").minute)
    Dep_hour=2
    Dep_min=30
    # print("Departure : ",Dep_hour, Dep_min)

    # Arrival
    #date_arr = request.POST["Arrival_Time"]
    #Arrival_hour = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").hour)
    #Arrival_min = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").minute)
    Arrival_hour=5
    Arrival_min=30
    # print("Arrival : ", Arrival_hour, Arrival_min)

    # Duration
    dur_hour = abs(Arrival_hour - Dep_hour)
    dur_min = abs(Arrival_min - Dep_min)
    # print("Duration : ", dur_hour, dur_min)

    # Total Stops
    Total_stops = int(request.POST["stops"])
    # print(Total_stops)

    # Airline
    # AIR ASIA = 0 (not in column)
    airline = request.POST['airline']

    Jet_Airways = 0
    IndiGo = 0
    Air_India = 0
    Multiple_carriers = 0
    SpiceJet = 0
    Vistara = 0
    GoAir = 0
    Multiple_carriers_Premium_economy = 0
    Jet_Airways_Business = 0
    Vistara_Premium_economy = 0
    Trujet = 0

    if(airline == 'Jet Airways'):
        Jet_Airways = 1
    elif (airline == 'IndiGo'):
        IndiGo = 1
    elif (airline == 'Air India'):
        Air_India = 1
    elif (airline == 'Multiple carriers'):
        Multiple_carriers = 1
    elif (airline == 'SpiceJet'):
        SpiceJet = 1
    elif (airline == 'Vistara'):
        Vistara = 1
    elif (airline == 'GoAir'):
        GoAir = 1
    elif (airline == 'Multiple carriers Premium economy'):
        Multiple_carriers_Premium_economy = 1
    elif (airline == 'Jet Airways Business'):
        Jet_Airways_Business = 1
    elif (airline == 'Vistara Premium economy'):
        Vistara_Premium_economy = 1
    elif (airline == 'Trujet'):
        Trujet = 1
    else:
        pass


    Source = request.POST["Source"]

    s_Delhi = 0
    s_Kolkata = 0
    s_Mumbai = 0
    s_Chennai = 0

    if (Source == 'Delhi'):
        s_Delhi = 1
    elif (Source == 'Kolkata'):
        s_Kolkata = 1
    elif (Source == 'Mumbai'):
        s_Mumbai = 1
    elif (Source == 'Chennai'):
        s_Chennai = 1
    else:
        pass


    Source = request.POST["Destination"]

    d_Cochin = 0
    d_Delhi = 0
    d_New_Delhi = 0
    d_Hyderabad = 0
    d_Kolkata = 0

    if (Source == 'Cochin'):
        d_Cochin = 1
    elif (Source == 'Delhi'):
        d_Delhi = 1
    elif (Source == 'New_Delhi'):
        d_New_Delhi = 1
    elif (Source == 'Hyderabad'):
        d_Hyderabad = 1
    elif (Source == 'Kolkata'):
        d_Kolkata = 1
    else:
        pass

    prediction = model.predict([[
            Total_stops,
            Journey_day,
            Journey_month,
            Dep_hour,
            Dep_min,
            Arrival_hour,
            Arrival_min,
            dur_hour,
            dur_min,
            Air_India,
            GoAir,
            IndiGo,
            Jet_Airways,
            Jet_Airways_Business,
            Multiple_carriers,
            Multiple_carriers_Premium_economy,
            SpiceJet,
            Trujet,
            Vistara,
            Vistara_Premium_economy,
            s_Chennai,
            s_Delhi,
            s_Kolkata,
            s_Mumbai,
            d_Cochin,
            d_Delhi,
            d_Hyderabad,
            d_Kolkata,
            d_New_Delhi
        ]])

    output = ceil(prediction[0])

    currentMonth = datetime.now().month

    month_map = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
        7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    x = []
    y = []
    # for month in range(currentMonth,Journey_month+1):
    #     x.append(((month-1)%12)+1)
    month = currentMonth
    while(month != Journey_month):
        x.append(month)
        month = (month % 12)+1
    x.append(month)

    for m in x:
        y.append(ceil(model.predict([[
                Total_stops,
                Journey_day,
                m,
                Dep_hour,
                Dep_min,
                Arrival_hour,
                Arrival_min,
                dur_hour,
                dur_min,
                Air_India,
                GoAir,
                IndiGo,
                Jet_Airways,
                Jet_Airways_Business,
                Multiple_carriers,
                Multiple_carriers_Premium_economy,
                SpiceJet,
                Trujet,
                Vistara,
                Vistara_Premium_economy,
                s_Chennai,
                s_Delhi,
                s_Kolkata,
                s_Mumbai,
                d_Cochin,
                d_Delhi,
                d_Hyderabad,
                d_Kolkata,
                d_New_Delhi
            ]])[0]))

    n = len(x)
    # n1=len(y)
    # print(n,n1,sep='----')
    min_price = y[0]
    target_month = currentMonth
    for i in range(n):
        print(min_price)
        if y[i] < min_price:
            min_price = y[i]
            target_month = x[i]
    target_month_name = month_map[target_month]
    # print(target_month)

    # print(x)
    # print(y)

    # x=[1,2,3,4,5]
    # y=[2,4,6,8,10]
    X = []
    for i in x:
        X.append(month_map[i])
    # X=['Jan','Feb','Mar','Apr','Jun']
    arr = list(map(list, zip(X, y)))
    # jdata=json.dumps(arr)

    # print(arr)
    # return render(request,'prediction.html',{'pred':output})
    return render(request, 'prediction.html', {'data': arr, 'pred': output, 'target_month': target_month_name})
