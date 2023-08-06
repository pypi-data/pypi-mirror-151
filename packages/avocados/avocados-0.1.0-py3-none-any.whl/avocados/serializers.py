from rest_framework import serializers


class AvocadoSerializer(serializers.Serializer):
    date = serializers.DateField()
    average_price = serializers.FloatField(required=False)
    total_volume = serializers.FloatField()
    number_small_hass_sold = serializers.FloatField()
    number_large_hass_sold = serializers.FloatField()
    number_extra_large_hass_sold = serializers.FloatField()
    number_small_bags_sold = serializers.FloatField()
    number_large_bags_sold = serializers.FloatField()
