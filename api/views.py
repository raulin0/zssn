from django.db import transaction
from django.db.models import Q, Sum
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Survivor
from .serializers import SurvivorSerializer


class SurvivorViewSet(viewsets.ModelViewSet):
    queryset = Survivor.objects.all()
    serializer_class = SurvivorSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @transaction.atomic
    @action(detail=False, methods=['post'])
    def make_trade(self, request, *args, **kwargs):
        data = dict(request.data)
        survivor1 = Survivor.objects.filter(
            pk=int(request.data['survivor1']), is_infected=False
        ).first()
        survivor2 = Survivor.objects.filter(
            pk=int(request.data['survivor2']), is_infected=False
        ).first()

        if survivor1 == None or survivor2 == None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        items1 = data['survivor1_items']
        items2 = data['survivor2_items']

        survivor1_trade_points = Survivor.calculate_points(
            int(items1[0]), int(items1[1]), int(items1[2]), int(items1[3])
        )
        survivor2_trade_points = Survivor.calculate_points(
            int(items2[0]), int(items2[1]), int(items2[2]), int(items2[3])
        )

        if (
            survivor1.total_points < survivor1_trade_points
            or survivor2.total_points < survivor2_trade_points
        ):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if survivor1_trade_points != survivor2_trade_points:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        items_list = ['water', 'food', 'medication', 'ammunition']

        for item in items_list:
            setattr(
                survivor1,
                item,
                getattr(survivor1, item) - int(items1[items_list.index(item)]),
            )
            setattr(
                survivor2,
                item,
                getattr(survivor2, item) - int(items2[items_list.index(item)]),
            )

        for item in items_list:
            setattr(
                survivor1,
                item,
                getattr(survivor1, item) + int(items2[items_list.index(item)]),
            )
            setattr(
                survivor2,
                item,
                getattr(survivor2, item) + int(items1[items_list.index(item)]),
            )

        survivor1.save()
        survivor2.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    @action(detail=True, methods=['put'])
    def report_infected(self, request, *args, **kwargs):
        data = dict(request.data)
        survivor_reported = Survivor.objects.filter(
            pk=int(request.data['survivor_reported'])).first()


        if survivor_reported.is_infected:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'error': 'The survivor is already infected'},
            )

        survivor_reported.received_reports += 1
        if survivor_reported.received_reports >= 3:
            survivor_reported.is_infected = True
        survivor_reported.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


    @transaction.atomic
    @action(detail=False, methods=['get'])
    def get_resources_report(self, request, *args, **kwargs):

        total_survivors = Survivor.objects.count()
        infected_survivors = Survivor.objects.filter(is_infected=True)
        infected_survivors_counter = infected_survivors.count()
        non_infected_survivors = total_survivors - infected_survivors_counter


        resources = {}    
        for resource in Survivor.ITEMS:

            resources[resource] = {}
            resources[resource]['total'] = Survivor.objects.aggregate(Sum(resource))['{}__sum'.format(resource)]
            resources[resource]['average'] = round((
                resources[resource]['total'] / total_survivors
            ), 2)

        total_points_lost = 0
        for infected_survivor in infected_survivors:
            total_points_lost += infected_survivor.total_points


        return Response(
            data={
                'population': {
                    'total': total_survivors,
                    'infected': infected_survivors_counter,
                    'non_infected': non_infected_survivors,
                    'percent_infected': round((infected_survivors_counter / total_survivors)
                    * 100, 2),
                    'percent_non_infected' : round((non_infected_survivors / total_survivors)
                    * 100, 2),
                },
                'resources': resources,
                'total_points_lost' : total_points_lost
            }
        )
