from io import BytesIO
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common.permissions import RolePermission
from apps.appointments.models import Appointment
from .models import Bill, BillLineItem
from .serializers import BillSerializer

User = get_user_model()


class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.select_related("appointment", "appointment__guest").prefetch_related("items").all()
    serializer_class = BillSerializer
    permission_classes = [RolePermission]
    allowed_roles = [User.Roles.ADMIN, User.Roles.MANAGER, User.Roles.ACCOUNTANT, User.Roles.FRONT_DESK]

    @action(detail=False, methods=["post"])
    def generate(self, request):
        booking_id = request.data.get("booking") or request.data.get("appointment")
        if not booking_id:
            return Response({"detail": "booking is required"}, status=status.HTTP_400_BAD_REQUEST)

        booking = Appointment.objects.get(pk=booking_id)
        bill, _ = Bill.objects.get_or_create(appointment=booking)
        if not bill.items.exists():
            BillLineItem.objects.create(
                bill=bill,
                description="Room stay charge",
                quantity=1,
                unit_price=Decimal("120.00"),
                amount=Decimal("120.00"),
            )
        bill.status = Bill.Status.ISSUED
        bill.save(update_fields=["status"])
        bill.recalculate()
        return Response(BillSerializer(bill).data)

    @action(detail=True, methods=["post"])
    def mark_paid(self, request, pk=None):
        bill = self.get_object()
        bill.status = Bill.Status.PAID
        bill.save(update_fields=["status"])
        return Response(BillSerializer(bill).data)

    @action(detail=True, methods=["get"])
    def invoice_pdf(self, request, pk=None):
        bill = self.get_object()
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas

            buffer = BytesIO()
            pdf = canvas.Canvas(buffer, pagesize=letter)
            pdf.drawString(50, 760, f"Invoice #{bill.id}")
            pdf.drawString(50, 740, f"Guest: {bill.appointment.guest.first_name} {bill.appointment.guest.last_name}")
            y = 700
            for item in bill.items.all():
                pdf.drawString(50, y, f"{item.description} x{item.quantity} = ${item.amount}")
                y -= 20
            pdf.drawString(50, y - 10, f"Tax: ${bill.tax}")
            pdf.drawString(50, y - 30, f"Total: ${bill.total}")
            pdf.save()
            buffer.seek(0)
            response = HttpResponse(buffer.read(), content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="invoice_{bill.id}.pdf"'
            return response
        except Exception:
            return Response(
                {
                    "invoice": {
                        "invoice_id": bill.id,
                        "total": str(bill.total),
                        "status": bill.status,
                    }
                }
            )
