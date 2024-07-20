from rest_framework import serializers


class CountCostsSerializer(serializers.Serializer):
    count = serializers.IntegerField(read_only=True)


class CountOrdersSerializer(CountCostsSerializer):
    pass
