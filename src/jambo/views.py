from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from jambo.forms import CSVImportForm
from jambo.models import Business, BusinessCategory, BusinessItem, Item, UserBusinessVolume
from jambo.util import generate_email
import csv

from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger,
)
import logging

# Create your views here.
def user_business_create(request):
    # import pdb; pdb.set_trace()
    if request.method == 'POST':
        form = CSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file'].read().decode('utf-8').splitlines()
            csv_reader = csv.DictReader(csv_file)

            User = get_user_model()

            for row in csv_reader:
                user = User.objects.filter(full_name=row['Customer name']).first()
                logging.info('User: %s' % user.__str__())
                # if user does not exist
                if not user:
                    email = generate_email(row['Customer name'])
                    user = User.objects.create_customeruser(email=email, full_name=row['Customer name'], password=email, phone_number=row['Customer Phone number'])

                if user:
                    logging.info('User: %s' % user.__str__())
                    # check if business category exists else create
                    category, _ = BusinessCategory.objects.get_or_create(name=row['Business Category'])
                    # check if business exists else create
                    business, _ = Business.objects.get_or_create(category=category, name=row['Business Name'])
                    # check if item exists else create
                    item, _ = Item.objects.get_or_create(name=row['Item'], amount=Decimal(row['Amount']))
                    # then link all of the above into business item object
                    if category and business and item:
                        # create business item
                        _, created = BusinessItem.objects.get_or_create(user=user, business=business, item=item, year=int(row['Year']))

        return redirect('jambo:list')
    else:
        form = CSVImportForm()
    return render(request, 'jambo/create.html', {'form': form})

def user_business_list_view(request):
    # Get page number from request, 
    # default to first page
    default_page = 1
    page = request.GET.get('page', default_page)
    # Get queryset of items to paginate
    items = UserBusinessVolume.objects.all()
    logging.info('items: %s\n', items.count())
    # Paginate items
    items_per_page = 10
    paginator = Paginator(items, items_per_page)

    try:
        items_page = paginator.page(page)
    except PageNotAnInteger:
        items_page = paginator.page(default_page)
    except EmptyPage:
        items_page = paginator.page(paginator.num_pages)
    return render(request, "jambo/list.html", {"items_page": items_page})
