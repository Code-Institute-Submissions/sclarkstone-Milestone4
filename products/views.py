from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower
from django.db.models import Avg

from .models import Product, Category
from .forms import ProductForm
from profiles.models import UserProfile
from checkout.models import Order, OrderLineItem

from reviews.models import Review


# Create your views here.

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            if 'Plans' in categories:
                plans = True
            else:
                plans = False
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)
        else:
            plans = False

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                if 'category' in request.GET:
                    categories = request.GET['category'].split(',')
                    if 'Plans' in categories:
                        plans = True
                    else:
                        plans = False
                else:
                    plans = False
            else:
                product_type = products.filter(category__pk=5, name__contains=query)
                if not product_type:
                    plans = False
                else:
                    plans = True

            queries = Q(name__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
        'plans': plans,

    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)
    review_total = Review.objects.filter(product_id=product_id).count()
    review_sum = Review.objects.filter(product_id=product_id).aggregate(Avg('rating'))['rating__avg']

    if request.user.is_authenticated:
        profile_name = get_object_or_404(UserProfile, user=request.user)
        orders = profile_name.orders.all()
        order_item = Order.objects.filter(user_profile=request.user.userprofile)
        order_items = OrderLineItem.objects.filter(order__user_profile=request.user.userprofile, product=product_id).values_list('product')
        if not order_items:
            plan_owned = False
        else:
            plan_owned = True
    else:
        plan_owned = False
    context = {
        'product': product,
        'review_total': review_total,
        'review_sum': review_sum,
        'plan_owned': plan_owned,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return render(request, 'home/index.html')
