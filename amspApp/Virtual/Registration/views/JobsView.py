from datetime import datetime

from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from amspApp.CompaniesManagment.Hamkari.models import Hamkari, HamkariJobs, RequestHamkari
from amspApp.CompaniesManagment.Hamkari.serializers.HamkariSerializer import HamkariSerializer, HamkariJobsSerializer, \
    RequestHamkariSerializer
from amspApp.Infrustructures.Classes.DateConvertors import mil_to_sh
from amspApp._Share.ListPagination import DetailsPagination


class JobsViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Hamkari.objects.all().filter(publish=True)
    serializer_class = HamkariSerializer
    pagination_class = DetailsPagination

    def get_queryset(self):
        self.queryset = self.queryset.filter(userID = self.request._request.owner_subdomain_user.id)
        return self.queryset

    @csrf_exempt
    def list(self, request, *args, **kwargs):
        result = super(JobsViewSet, self).list(request, *args, **kwargs)
        for d in result.data["results"]:
            d["startDate"] = mil_to_sh(d["startDate"].split("T")[0])
            d["endDate"] = mil_to_sh(d["endDate"].split("T")[0])

        return result

    @csrf_exempt
    def retrieve(self, request, *args, **kwargs):
        result = super(JobsViewSet, self).retrieve(request, *args, **kwargs)
        hamkariInstance = self.queryset.get(id=kwargs['id'])
        isValid = hamkariInstance.startDate < datetime.now() < hamkariInstance.endDate
        result.data["startDate"] = mil_to_sh(result.data["startDate"].split("T")[0])
        result.data["endDate"] = mil_to_sh(result.data["endDate"].split("T")[0])
        result.data["valid"] = isValid
        return result

    @detail_route(methods=["get"])
    def items(self, request, *args, **kwargs):
        jobItems = HamkariJobs.objects.filter(hamkariID=kwargs['id']).filter(publish=True).order_by("-id")
        jobItems = HamkariJobsSerializer(instance=jobItems, many=True).data
        for j in jobItems:
            f = RequestHamkari.objects.filter(
                userID=request.user.id,
                jobID=j["id"],
            ).count()
            if f != 0:
                j["registered"] = True
            else:
                j["registered"] = False

        return Response(jobItems)

    @list_route(methods=["post"])
    def removeRegisterForJob(self, request, *args, **kwargs):
        RequestHamkari.objects.filter(
            userID=request.user.id,
            hamkariID=request.data['hamkariID'],
            jobID=request.data['id'],
        ).delete()
        return Response({})

    @list_route(methods=["post"])
    def registerForJob(self, request, *args, **kwargs):

        # checking if job expired or not
        hamkariInstance = Hamkari.objects.get(id=request.data['hamkariID'])
        if not (hamkariInstance.startDate < datetime.now() < hamkariInstance.endDate):
            return Response({'msg': "این آگهی منقضی شده است"}, status=status.HTTP_400_BAD_REQUEST)

        # checking if registered in this job before
        hamkariCount = RequestHamkari.objects.filter(
            userID=request.user.id,
            hamkariID=request.data['hamkariID'],
            jobID=request.data['id'],
        ).count()

        if hamkariCount == 0:
            data = {}
            data["userID"] = request.user.id
            data["hamkariID"] = request.data['hamkariID']
            data["jobID"] = request.data['id']
            data["type"] = 1
            data["extra"] = {}
            data["extra"]["extraFields"] = request.data['extraFields']
            serial = RequestHamkariSerializer(data=data)
            serial.is_valid(raise_exception=True)
            serial.save()
            return Response(serial.data)
        else:
            return Response({'msg': "قبلا در این شغل ثبت نام کرده اید"}, status=status.HTTP_400_BAD_REQUEST)
