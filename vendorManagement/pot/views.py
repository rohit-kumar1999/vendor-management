from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Avg
from datetime import datetime
from .models import PurchaseOrder
from vms.models import Vendor, Performance
from .manager import validate_purchase_order_data


class PurchaseOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = PurchaseOrder.objects.all()
        return Response(orders.values(), status=status.HTTP_200_OK)

    def post(self, request):
        order_data = request.data
        try:
            validate_purchase_order_data(order_data)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        order = PurchaseOrder.objects.create(
            po_number=order_data.get('po_number'),
            delivery_date=order_data.get('delivery_date'),
            items=order_data.get('items'),
            vendor_id=order_data.get('vendor_id'),
            quantity=order_data.get('quantity'),
            status=order_data.get('status'),
            quality_rating=order_data.get('quality_rating'),
            issue_date=order_data.get('issue_date'),
            acknowledgment_date=order_data.get('acknowledgment_date')
        )
        modified_order = model_to_dict(order)
        modified_order['id'] = order.id
        return Response(modified_order, status=status.HTTP_201_CREATED)


class PurchaseOrderById(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            order = PurchaseOrder.objects.get(id=order_id)
        except PurchaseOrder.DoesNotExist:
            return Response({'error': 'Purchase Order does not exist of given id'}, status=status.HTTP_404_NOT_FOUND)
        modified_order = model_to_dict(order)
        modified_order['id'] = order.id
        return Response(modified_order, status=status.HTTP_200_OK)

    def put(self, request, order_id):
        order_data = request.data
        try:
            validate_purchase_order_data(order_data)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        try:
            PurchaseOrder.objects.filter(id=order_id).update(
                order_date=order_data.get('order_date'),
                delivery_date=order_data.get('delivery_date'),
                items=order_data.get('items'),
                vendor_id=order_data.get('vendor_id'),
                quantity=order_data.get('quantity'),
                status=order_data.get('status'),
                quality_rating=order_data.get('quality_rating'),
                issue_date=order_data.get('issue_date'),
                acknowledgment_date=order_data.get('acknowledgment_date')
            )

            if order_data.get('status') == 'completed':
                orders = PurchaseOrder.objects.filter(vendor__id=order_data.get('vendor_id'), status='completed')
                delivered_orders = orders.filter(delivery_date__lte=datetime.now())
                delivery_rate = delivered_orders.count()*100/orders.count()
                try:
                    performace = Performance.objects.get(vendor__id=order_data.get('vendor_id'))
                    performace.on_time_delivery_rate = delivery_rate
                    performace.quality_rating_avg = PurchaseOrder.objects.filter(
                            vendor__id=order_data.get('vendor_id'), status='completed').aggregate(Avg('quality_rating'))
                    performace.save(update_fields=['on_time_delivery_rate', 'quality_rating_avg'])

                except:
                    Performance.objects.create(
                        vendor_id=order_data.get('vendor_id'),
                        date=datetime.now(),
                        on_time_delivery_rate=delivery_rate,
                        quality_rating_avg=PurchaseOrder.objects.filter(
                            vendor__id=order_data.get('vendor_id'), status='completed').aggregate(Avg('quality_rating')),
                        average_response_time=0,
                        fulfillment_rate=0
                    )

            order = PurchaseOrder.objects.get(id=order_id)
            modified_order = model_to_dict(order)
            modified_order['id'] = order.id
            return Response(modified_order, status=status.HTTP_200_OK)
        except PurchaseOrder.DoesNotExist:
            return Response({'error': 'Purchase Order does not exist of given id'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, order_id):
        try:
            order = PurchaseOrder.objects.get(id=order_id)
        except PurchaseOrder.DoesNotExist:
            return Response({'error': 'Purchase Order does not exist of given id'}, status=status.HTTP_404_NOT_FOUND)
        order.delete()
        return Response("Purchase Order deleted successfully", status=status.HTTP_200_OK)