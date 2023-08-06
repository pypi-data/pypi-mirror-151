from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from avocados.serializers import AvocadoSerializer
from rest_framework.parsers import JSONParser
from rest_framework import status

@csrf_exempt
def predict_price(request):
    if request.method == 'GET':
        data = request.GET.dict()
        serializer = AvocadoSerializer(data=data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AvocadoSerializer(data=data)

    if serializer.is_valid():
        average_price = serializer.data['number_small_hass_sold'] + serializer.data['number_large_hass_sold'] + serializer.data['number_extra_large_hass_sold'] / serializer.data['total_volume']
        data['average_price'] = average_price
        serializer = AvocadoSerializer(data=data)
        serializer.is_valid()
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)