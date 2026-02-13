from rest_framework import serializers
from .models import Bill, BillLineItem


class BillLineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillLineItem
        fields = ["id", "bill", "description", "quantity", "unit_price", "amount"]
        read_only_fields = ["amount"]


class BillSerializer(serializers.ModelSerializer):
    items = BillLineItemSerializer(many=True, required=False)
    booking = serializers.IntegerField(source="appointment_id", read_only=True)

    class Meta:
        model = Bill
        fields = ["id", "booking", "appointment", "subtotal", "tax", "total", "status", "generated_at", "items"]
        read_only_fields = ["subtotal", "tax", "total", "generated_at"]

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        bill = Bill.objects.create(**validated_data)
        for item_data in items_data:
            BillLineItem.objects.create(bill=bill, **item_data)
        bill.recalculate()
        return bill

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key != "items":
                setattr(instance, key, value)
        instance.save()
        if "items" in validated_data:
            instance.items.all().delete()
            for item_data in validated_data["items"]:
                BillLineItem.objects.create(bill=instance, **item_data)
        instance.recalculate()
        return instance
