from django.shortcuts import render
from core.models import Vendor, Products
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
    city = request.POST['city'] if request.POST['city'] else None

    if len(cnpj) < 18:

        return JsonResponse({'success': False, 'message': 'CNPJ incorreto'})
    else:
        if vendor_id:
            vendor_data = Vendor.objects.get(id=vendor_id)
            if cnpj != vendor_data.cnpj_vendor:
                existing_vendor_cnpj = Vendor.objects.filter(cnpj_vendor=cnpj)
                if existing_vendor_cnpj:
                    return JsonResponse({'success': False, 'message': 'CNPJ já cadastrado no sistema'})
                else:
                    Vendor.objects.filter(id=vendor_id).update(name=name,
                                                                        cnpj_vendor=cnpj,
                                                                        city=city)
                    return JsonResponse({'success': True})
            else:
                Vendor.objects.filter(id=vendor_id).update(name=name,
                                                                    cnpj_vendor=cnpj,
                                                                    city=city)
                return JsonResponse({'success': True})
        else:
            existing_vendor_cnpj = Vendor.objects.filter(cnpj_vendor=cnpj)
            if existing_vendor_cnpj:
                return JsonResponse({'success': False, 'message': 'CNPJ já cadastrado no sistema'})
            else:
                Vendor.objects.create(name=name, cnpj_vendor=cnpj, city=city)

                return JsonResponse({'success': True})


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
                                "<a href='/edit/product/?vendor=%s'>"
                                   "<button type='button' class='btn btn-primary btn-sm'>"
                                        "<span class='glyphicon glyphicon-plus'></span> Produto"
                                   "</button>"
                                "</a>" % str(v.id)])
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
    return JsonResponse({'data': vendor_list, 'draw': draw + 1,
                         'recordsTotal': total, 'recordsFiltered': total})


@csrf_exempt
def delete_vendor(request):
    vendor_id = request.GET.get('id')
    if vendor_id:
        vendor = Vendor.objects.get(id=vendor_id)
    dic = {'vendor': vendor}
    return render(request, 'delete-vendor.html', dic)


@csrf_exempt
def action_delete_vendor(request):
    print(request.POST)
    vendor_id = request.POST['vendor_id']
    if vendor_id:
        Products.objects.filter(vendor_id=vendor_id).delete()
        Vendor.objects.filter(id=vendor_id).delete()
        return JsonResponse({'success':True})
    else:
        return JsonResponse({'success': False, 'message': 'Não foi possível excluir'})


def create_data_table_products(products):
    products_list = []
    if products:
        for product in products:
            products_list.append([product.name,
                                product.code,
                                'R$' + str(product.price),
                                product.vendor.name,
                                "<a href='/delete/product/?id=%s' notification-modal='1'>"
                                    "<button type='button' class='btn btn-danger btn-sm' id=''>"
                                        "<span class='glyphicon glyphicon-remove'></span>"
                                    "</button>"
                                "</a>" % str(product.id) +
                                "<a href='/edit/product/?id=%s'>"
                                    "<button type='button' class='btn btn-success btn-sm' id=''>"
                                        "<span class='glyphicon glyphicon-edit'></span></button>"
                                "</a>" % str(product.id)])
    return products_list


@csrf_exempt
def list_products(request):
    vendor = Vendor.objects.all()
    dic = {'vendor': vendor}
    return render(request, 'list-products.html', dic)


@csrf_exempt
def get_list_products(request):
    vendor = request.POST['vendor'] if request.POST['vendor'] else None
    draw = int(request.POST['draw'])
    value = request.POST['search[value]']
    products = Products.objects.all()
    if vendor:
        products = Products.objects.filter(vendor_id=vendor)
    if value:
        products = Products.objects.filter(Q(name__icontains=value) |
                                   Q(code__icontains=value) |
                                   Q(price__icontains=value) |
                                   Q(vendor__name__icontains=value))

    total = products.count()
    products_list = create_data_table_products(products)
    return JsonResponse({'data': products_list, 'draw': draw + 1, 'recordsTotal': total, 'recordsFiltered': total})


@csrf_exempt
def edit_product(request):
    vendor_id = request.GET['vendor'] if 'vendor' in request.GET else None
    product_id = request.GET.get('id')
    if product_id:
        product = Products.objects.get(id=product_id)
    else:
        product = None
    vendor = Vendor.objects.all()
    selected_vendor = None
    existed_vendor = False
    if vendor_id:
        selected_vendor = Vendor.objects.get(id=vendor_id)
        existed_vendor = True
    dic = {'vendor': vendor, 'product': product, 'selected_vendor': selected_vendor, 'existed_vendor': existed_vendor}
    return render(request, 'edit-product.html', dic)


@csrf_exempt
def get_vendor_data(request, vendor_id):
    vendor = Vendor.objects.get(id=vendor_id)
    cnpj = vendor.cnpj_vendor
    city = vendor.city
    return JsonResponse({'cnpj': cnpj, 'city': city})


@csrf_exempt
def save_product(request):
    product_id = request.POST['id']
    name = request.POST['name']
    code = request.POST['code']
    price = request.POST['price'].replace('.', '').replace(',', '.') if request.POST['price'] else None
    vendor = request.POST['vendor']
    existed_vendor = request.POST['existed_vendor']
    if product_id:
        Products.objects.filter(id=product_id).update(name=name,
                                                      code=code,
                                                      price=price)
    else:
        Products.objects.create(name=name,
                                code=code,
                                price=price,
                                vendor_id=vendor)

    if existed_vendor == 'False':
        return JsonResponse({'success': True, 'existed_vendor': False})
    else:
        return JsonResponse({'success': True, 'existed_vendor': True})



@csrf_exempt
def delete_product(request):
    product_id = request.GET.get('id')
    vendor_products = Vendor.objects.all()
    product = None
    if product_id:
        product = Products.objects.get(id=product_id)
    dic = {'product': product, 'vendor_products': vendor_products}
    return render(request, 'delete-product.html', dic)


@csrf_exempt
def action_delete_product(request):
    product_id = request.POST['product_id'] if 'product_id' in request.POST else None
    vendor_products = request.POST['vendor_products'] if 'vendor_products' in request.POST else None
    if product_id:
        Products.objects.filter(id=product_id).delete()
        return JsonResponse({'success':True})
    elif vendor_products:
        products = Products.objects.filter(vendor_id=vendor_products).delete()
        return JsonResponse({'success': True})
    elif 'vendor_products' in request.POST and not vendor_products:
        Products.objects.all().delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Não foi possível excluir'})