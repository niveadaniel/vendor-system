from django.shortcuts import render
from core.models import Vendor
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
# Create your views here.

def index(request):
    return render(request, 'home-page.html')


@csrf_exempt
def list_vendor(request):
    return render(request, 'list-vendor.html')


@csrf_exempt
def edit_vendor(request):
    vendor_id = request.GET.get('id')
    if vendor_id:
        vendor = Vendor.objects.get(id=vendor_id)
    else:
        vendor = None

    dic = {'vendor': vendor}
    return render(request, 'edit-vendor.html', dic)


@csrf_exempt
def save_vendor(request):
    vendor_id = request.POST['id']
    name = request.POST['name']
    cnpj = request.POST['cnpj']
    city = request.POST['city']

    if len(cnpj) < 14:
        return JsonResponse({'success': False, 'message': 'CNPJ incorreto'})
    else:
        if vendor_id:
            vendor_data = Vendor.objects.get(id=vendor_id)
            if cnpj != vendor_data.cnpj_vendor:
                existing_vendor_cnpj = Vendor.objects.filter(cnpj_vendor=cnpj)
                if existing_vendor_cnpj:
                    return JsonResponse({'success': False, 'message': 'CNPJ já cadastrado no sistema'})
            else:
                vendor = Vendor.objects.filter(id=vendor_id).update(name=name, cnpj_vendor=cnpj, city=city)
                vendor = Vendor.objects.get(id=vendor_id)
                return JsonResponse({'success': True, 'id': vendor.id})
        else:
            existing_vendor_cnpj = Vendor.objects.filter(cnpj_vendor=cnpj)
            if existing_vendor_cnpj:
                return JsonResponse({'success': False, 'message': 'CNPJ já cadastrado no sistema'})
            else:
                vendor = Vendor.objects.create(name=name, cnpj_vendor=cnpj, city=city)

                return JsonResponse({'success': True ,'id': vendor.id})


def create_data_table_vendor(vendor):
    vendor_list = []
    if vendor:
        for v in vendor:
            vendor_list.append([v.name,
                                v.cnpj_vendor,
                                v.city,
                                "<a href='/delete/vendor/?id=%s' notification-modal='1'>"
                                    "<button type='button' class='btn btn-danger btn-sm' id=''>"
                                        "<span class='glyphicon glyphicon-remove'></span>"
                                    "</button>"
                                "</a>" % str(v.id) +
                                "<a href='/edit/vendor/?id=%s'>"
                                    "<button type='button' class='btn btn-success btn-sm' id=''>"
                                        "<span class='glyphicon glyphicon-edit'></span></button>"
                                "</a>" % str(v.id) +
                                   "<button type='button' class='btn btn-primary btn-sm'>"
                                        "Cadastrar Produtos"
                                   "</button>"])
    return vendor_list


@csrf_exempt
def get_vendor_list(request):
    draw = int(request.GET['draw'])
    value = request.GET['search[value]']
    vendor = Vendor.objects.all()
    if value:
        vendor = vendor.filter(Q(name__icontains=value) |
                               Q(cnpj_vendor__icontains=value) |
                               Q(city__icontains=value))

    total = vendor.count()
    vendor_list = create_data_table_vendor(vendor)
    return JsonResponse({'data': vendor_list, 'draw': draw + 1, 'recordsTotal': total, 'recordsFiltered': total})


@csrf_exempt
def delete_vendor(request):
    vendor_id = request.GET.get('id')
    if vendor_id:
        vendor = Vendor.objects.get(id=vendor_id)
    dic = {'vendor': vendor}
    return render(request, 'delete-vendor.html', dic)


@csrf_exempt
def action_delete_vendor(request, vendor_id):
    if vendor_id:
        Vendor.objects.filter(id=vendor_id).delete()
        return JsonResponse({'success':True})
    else:
        return JsonResponse({'success': False, 'message': 'Não foi possível excluir'})

