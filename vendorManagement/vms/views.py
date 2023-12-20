from django.forms.models import model_to_dict
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Vendor, Performance
from .manager import validate_vendor_data


class VendorView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        vendors = Vendor.objects.all()
        return Response(vendors.values(), status=status.HTTP_200_OK)

    def post(self, request):
        vendor_data = request.data
        try:
            validate_vendor_data(vendor_data)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        vendor = Vendor.objects.create(
            name=vendor_data.get('name'),
            phone=vendor_data.get('phone'),
            address=vendor_data.get('address'),
            code=vendor_data.get('code'),
        )
        modified_vendor = model_to_dict(vendor, exclude=['phone'])
        modified_vendor['id'] = vendor.id
        modified_vendor['phone'] = str(vendor.phone)
        return Response(modified_vendor, status=status.HTTP_201_CREATED)


class VendorById(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(id=vendor_id)
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor does not exist of given id'}, status=status.HTTP_404_NOT_FOUND)
        modified_vendor = model_to_dict(vendor, exclude=['phone'])
        modified_vendor['id'] = vendor.id
        modified_vendor['phone'] = str(vendor.phone)
        return Response(modified_vendor, status=status.HTTP_200_OK)

    def put(self, request, vendor_id):
        vendor_data = request.data
        try:
            validate_vendor_data(vendor_data)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        try:
            Vendor.objects.filter(id=vendor_id).update(
                name=vendor_data.get('name'),
                phone=vendor_data.get('phone'),
                address=vendor_data.get('address'),
            )
            vendor = Vendor.objects.get(id=vendor_id)
            modified_vendor = model_to_dict(vendor, exclude=['phone'])
            modified_vendor['id'] = vendor.id
            modified_vendor['phone'] = str(vendor.phone)
            return Response(modified_vendor, status=status.HTTP_200_OK)
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor does not exist of given id'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(id=vendor_id)
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor does not exist of given id'}, status=status.HTTP_404_NOT_FOUND)
        vendor.delete()
        return Response("Vendor deleted successfully", status=status.HTTP_200_OK)


class PerformanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, vendor_id):
        try:
            performance = Performance.objects.filter(vendor__id=vendor_id)
        except Performance.DoesNotExist:
            return Response({'error': 'Performance does not exist for given vendor id'}, status=status.HTTP_404_NOT_FOUND)

        return Response(performance.values(), status=status.HTTP_200_OK)