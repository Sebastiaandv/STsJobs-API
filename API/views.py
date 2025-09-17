from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import JobCard, TimeTable, PartsList, Settings, CheckList, CustomerTable
from .serializers import *
import json, time


class QueryHomeJobs(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_jobs_list = JobCard.objects.all().order_by('-job_id').values()

        if all_jobs_list:
            data = []

            for job in all_jobs_list:
                try:
                    customer = CustomerTable.objects.get(customer_id=job['customer_id'])
                    name = customer.name
                    car = customer.car

                except:
                    name = 'Not set...'
                    car = 'Not set...'

                temp_data = {
                    "job_id": job['job_id'],
                    "name": name,
                    "car": car,
                    "completed": job['completed'],
                }

                data.append(temp_data)

            return Response(data)
        else:
            return Response({"error": "No job found with this ID"})
        

class QuerySiteSettings(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        setting_object = Settings.objects.get(id=1)

        data = {
            "hour_price": setting_object.hour_price,
        }

        return Response(data)
    
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        setting_object = Settings.objects.get(id=1)

        setting_object.hour_price = data['hour_price']
        setting_object.save()

        return Response({'status': '200'})



class QueryJobCard(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))

        job = JobCard.objects.get(job_id=data['job_id'])
        all_time_list = TimeTable.objects.filter(job_id=data['job_id']).values()
        all_parts_list = PartsList.objects.filter(job_id=data['job_id']).values()

        try:
            customer = CustomerTable.objects.get(customer_id=job.customer_id)
            name = customer.name
            car = customer.car
            license_plate = customer.license_plate
        except:
            name = ''
            car = ''
            license_plate = ''

        time_status = 0
        parts_count_status = 0
        parts_price_status = 0
        job_price_status = float(0)

        if all_parts_list:
            parts_price_status = float(0)
            parts_count_status = len(all_parts_list)

            for item in all_parts_list:
                if item['price']:
                    parts_price_status += float(item['price'].replace(',', '.'))

        if all_time_list:
            for item in all_time_list:
                if item['calculated_bool'] == '0' and item['time_registry']:
                    time_status += float(str(item['time_registry']).replace(',', '.'))

        float_hour_price = float(job.hour_price.replace(',', '.'))
        total_hour_price = float_hour_price * time_status

        job_price_status = parts_price_status + total_hour_price
        job_price_status = f'{job_price_status:.2f}'.replace('.', ',')

        if job:
            data = {
                "job_id": job.job_id,
                "name": name,
                "car": car,
                "license_plate": license_plate,
                "description": job.description,
                "completed": job.completed,
                "time_status": str(time_status).replace('.', ','),
                "parts_count_status": parts_count_status,
                "job_price_status": job_price_status,
            }

            return Response(data)
        else:
            return Response({"error": "No job found with this ID"})


class QuickEditJobstatus(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        job = JobCard.objects.get(job_id=data['job_id'])

        if job.completed == '0':
            job.completed = '1'
        else:
            job.completed = '0'

        job.save()

        data = {
            "completed": job.completed,
        }

        return Response(data)
    

class QuickEditJobCardFields(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        job = JobCard.objects.get(job_id=data['job_id'])

        job.description = data['description']

        job.save()

        data = {
            "description": job.description,
        }

        time.sleep(0.5)

        return Response(data)
    

class QueryNewJob(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        customer_id = data['customer_id']
        last_job_id = JobCard.objects.last()
        site_settings = Settings.objects.get(id=1)

        if last_job_id:
            last_job_id = last_job_id.job_id
        else:
            last_job_id = "#000000"
        new_job_id_int = int(str(last_job_id).replace('#', '')) + 1
        new_job_id = f'#{new_job_id_int:06d}'

        new_job = JobCard.objects.create(job_id=new_job_id)
        new_job.customer_id = customer_id
        new_job.hour_price = site_settings.hour_price
        new_job.description = ''
        new_job.completed = '0'

        new_job.save()

        data = {
            "job_id": new_job_id,
        }

        return Response(data)
    

class QueryDeleteJob(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        job_id = data['job_id']
        
        JobCard.objects.filter(job_id=job_id).delete()
        TimeTable.objects.filter(job_id=job_id).delete()
        PartsList.objects.filter(job_id=job_id).delete()
        CheckList.objects.filter(job_id=job_id).delete()

        data = {
            "status": '200',
        }

        return Response(data)
    

# TimeTable Querys
class QueryTimeTable(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        all_time_list = TimeTable.objects.filter(job_id=data['job_id']).values()
        job_id = data['job_id']

        related_time_entrys = []
        for entry in all_time_list:
            if entry['job_id'] == job_id:
                related_time_entrys.append(
                    {
                        'id': entry['time_id'],
                        'time': entry['time_registry']
                    }
                )

        return Response(related_time_entrys)
    

class QuickEditTimeEntry(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        time_entry = TimeTable.objects.get(job_id=data['job_id'], time_id=data['time_id'])

        time_entry.time_registry = data['new_value']
        time_entry.save()

        return Response({'status': '200'})
    

class DeleteTimeEntry(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        time_entry = TimeTable.objects.get(job_id=data['job_id'], time_id=data['time_id'])

        time_entry.delete()

        return Response({'status': '200'})


class AddTimeEntry(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        last_time_id = TimeTable.objects.filter(job_id=data['job_id']).last()

        if last_time_id:
            last_time_id = last_time_id.time_id
        else:
            last_time_id = "@000"
        new_time_id_int = int(str(last_time_id).replace('@', '')) + 1
        new_time_id = f'@{new_time_id_int:03d}'

        new_time = TimeTable.objects.create(job_id=data['job_id'], time_id=new_time_id)
        new_time.calculated_bool = '0'
        new_time.time_registry = ''

        new_time.save()

        return Response({'time_id': new_time_id})
    

# PartTable Querys
class QueryPartsTable(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        all_part_list = PartsList.objects.filter(job_id=data['job_id']).values()

        related_part_entrys = []
        for entry in all_part_list:
            related_part_entrys.append(
                {
                    'id': entry['part_id'],
                    'part_name': entry['part_name'],
                    'price': entry['price']
                }
            )

        return Response(related_part_entrys)
    

class QuickEditPartEntry(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        part_entry = PartsList.objects.get(job_id=data['job_id'], part_id=data['part_id'])

        part_entry.part_name = data['part_name']
        part_entry.price = data['price']
        part_entry.save()

        return Response({'status': '200'})
    

class DeletePartEntry(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        part_entry = PartsList.objects.get(job_id=data['job_id'], part_id=data['time_id'])

        part_entry.delete()

        return Response({'status': '200'})


class AddPartEntry(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        last_part_id = PartsList.objects.filter(job_id=data['job_id']).last()

        if last_part_id:
            last_part_id = last_part_id.part_id
        else:
            last_part_id = "$0000"
        new_part_id_int = int(str(last_part_id).replace('$', '')) + 1
        new_part_id = f'${new_part_id_int:04d}'

        new_part = PartsList.objects.create(job_id=data['job_id'], part_id=new_part_id)
        new_part.part_name = ''
        new_part.price = ''
        new_part.url = ''

        new_part.save()

        return Response({'part_id': new_part_id})
    

# Customers Querys
class QueryCustomersTable(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_customers_list = CustomerTable.objects.all()

        customers = []
        for entry in all_customers_list:
            customers.append(
                {
                    'customer_id': entry.customer_id,
                    'name': entry.name,
                    'car': entry.car,
                    'license_plate': entry.license_plate,
                }
            )

        return Response(customers)
    

class QueryCustomerCard(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))

        customer = CustomerTable.objects.get(customer_id=data['customer_id'])
        all_customer_jobs = CustomerTable.objects.filter(customer_id=customer.customer_id)

        if customer:
            data = {
                "customer_id": customer.customer_id,
                "name": customer.name,
                "car": customer.car,
                "license_plate": customer.license_plate,
                "description": customer.description
                # "customer_jobs": all_customer_jobs
            }

            return Response(data)
        else:
            return Response({"error": "No job found with this ID"})
    

class QuickEditCustomerEntry(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        customer = CustomerTable.objects.get(customer_id=data['customer_id'])

        customer.name = data['name']
        customer.car = data['car']
        customer.license_plate = data['license_plate']
        customer.description = data['description']
        customer.save()

        time.sleep(0.6)

        return Response({'status': '200'})
    

class DeleteCustomerEntry(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        customer = CustomerTable.objects.get(customer_id=data['customer_id'])

        customer.delete()

        return Response({'status': '200'})


class AddCustomerEntry(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        last_customer_id = CustomerTable.objects.last()

        if last_customer_id:
            last_customer_id = last_customer_id.customer_id
        else:
            last_customer_id = "&0000"
        new_customer_id = int(str(last_customer_id).replace('&', '')) + 1
        new_customer_id = f'&{new_customer_id:04d}'

        new_customer = CustomerTable.objects.create(customer_id=new_customer_id)
        new_customer.name = ''
        new_customer.car = ''
        new_customer.license_plate = ''

        new_customer.save()

        return Response({'customer_id': new_customer_id})