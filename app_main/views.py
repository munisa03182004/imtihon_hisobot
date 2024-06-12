from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth.decorators import login_required



from .forms import CostForm
from .models import Cost
from datetime import datetime, timedelta
from django.db.models import Q, Sum
from .models import Cost


def home_page(request):

    """
    View function for the home page.

    If the user is not authenticated, redirects to the login page.
    Otherwise, fetches the user's full name and lists of income and expense transactions.
    Renders the home page with the user's full name and transaction lists.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects to the login page if the user is not authenticated.
        HttpResponse: Renders the home page with the user's full name and transaction lists.
    """

    if not request.user.is_authenticated:
        return redirect('login')

    full_name = request.user.get_full_name()
    Chiqim_list = Cost.objects.filter(owner_id=request.user,transaction_type='Chiqim')  
    Kirim_list = Cost.objects.filter(owner_id=request.user,transaction_type='Kirim')  

    context = {
        "full_name": full_name,
        'Kirim': Kirim_list,
        'Chiqim':Chiqim_list
    }

    return render(request, 'app_main/home.html', context)

    



@login_required
def get_cost_info(request, cost_id):
    """
    View function to retrieve information about a specific cost.

    Fetches the cost object with the specified ID, belonging to the authenticated user.
    Renders the cost information page with the retrieved cost object.

    Parameters:
        request (HttpRequest): The HTTP request object.
        cost_id (int): The ID of the cost object to retrieve.

    Returns:
        HttpResponse: Renders the cost information page with the retrieved cost object.
    """

    cost = get_object_or_404(Cost, id=cost_id, owner_id=request.user)
    context = {
        'Cost': cost
    }

    return render(request, 'app_main/cost_info.html', context)



@login_required
def add_cost(request):
    """
    View function to add a new cost entry.

    This view is accessible only to authenticated users. On a POST request:
        - Extracts cost details from the request.
        - Creates a new Cost object with the provided details and the current user as the owner.
        - Redirects to the home page after successfully adding the cost.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects to the home page after adding the cost.
        HttpResponse: Renders the form for adding costs if the request method is not POST.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        amount = request.POST.get('amount')
        transaction_type = request.POST.get('transaction_type')

        if name and amount and transaction_type: 
            cost = Cost.objects.create(
                name=name,
                amount=amount,
                transaction_type=transaction_type,
                owner_id=request.user
            )
            cost.save()
            return redirect('home')  

    return render(request, 'app_main/add_cost.html')  


@login_required
def update_cost(request, cost_id):
    """"
    View function to update an existing cost entry.

    This view is accessible only to authenticated users. It retrieves the cost object
    with the specified ID belonging to the authenticated user. On a POST request:
        - Updates the cost object with the data from the submitted form.
        - Redirects to the home page after successfully updating the cost.
    On a GET request:
        - Renders the form to update the cost with the pre-filled data.

    Parameters:
        request (HttpRequest): The HTTP request object.
        cost_id (int): The ID of the cost object to update.

    Returns:
        HttpResponseRedirect: Redirects to the home page after updating the cost.
        HttpResponse: Renders the form to update the cost with pre-filled data if the request method is GET.
    """
    cost = get_object_or_404(Cost, id=cost_id, owner_id=request.user)

    if request.method == 'POST':
        form = CostForm(request.POST, instance=cost)
        if form.is_valid():
            form.save()
            return redirect('home')  
    else:
        form = CostForm(instance=cost)

    return render(request, 'app_main/update_cost.html', {'form': form, 'cost': cost})


@login_required
def delete_cost(request, cost_id): 
    """
    View function to delete an existing cost entry.

    This view is accessible only to authenticated users. It retrieves the cost object
    with the specified ID belonging to the authenticated user. On a POST request:
        - Deletes the cost object.
        - Redirects to the home page after successfully deleting the cost.
    On a GET request:
        - Renders a confirmation page to confirm deletion of the cost.

    Parameters:
        request (HttpRequest): The HTTP request object.
        cost_id (int): The ID of the cost object to delete.

    Returns:
        HttpResponseRedirect: Redirects to the home page after deleting the cost.
        HttpResponse: Renders a confirmation page to confirm deletion of the cost if the request method is GET.
    """ 
    cost = get_object_or_404(Cost, id=cost_id, owner_id=request.user)
    if request.method == 'POST':
        cost.delete()
        return redirect('home')  
    return render(request, 'app_main/confirm_delete.html', {'cost': cost})



@login_required
def chiqim_get_costs_within_7_days(request):

    """
    View function to retrieve costs added within the last 7 days for the current user.

    This view is accessible only to authenticated users. It retrieves the costs added within
    the last 7 days (including today) for the current authenticated user. It calculates the total
    amount of costs within this period.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'chiqim_7_days.html' template with the following context:
            - 'costs_within_7_days_chiqim': A queryset containing costs within the last 7 days.
            - 'summa': The total amount of costs within the last 7 days.
    """
    # Get the current user
    current_user = request.user

    # Get the current date
    today = datetime.now().date()

    # Calculate the date 7 days ago
    seven_days_ago = today - timedelta(days=7)

    # Filter costs added within the last 7 days for the current user
    costs_within_7_days_chiqim = current_user.cost_set.filter(
        Q(created__date__gte=seven_days_ago) & Q(created__date__lte=today) & Q(transaction_type='Chiqim')
    )
    summa = costs_within_7_days_chiqim.aggregate(Sum('amount'))['amount__sum'] or 0

    return render(request, 'app_main/chiqim_7_days.html', {
        'costs_within_7_days_chiqim': costs_within_7_days_chiqim,
        'summa': summa
    })




@login_required
def chiqim_get_costs_within_30_days(request):
    """
    View function to retrieve costs added within the last 30 days for the current user.

    This view is accessible only to authenticated users. It retrieves the costs added within
    the last 30 days (including today) for the current authenticated user. It calculates the total
    amount of costs within this period.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'chiqim_30_days.html' template with the following context:
            - 'costs_within_30_days_chiqim': A queryset containing costs within the last 30 days.
            - 'summa': The total amount of costs within the last 30 days.
    """
    # Get the current user
    current_user = request.user

    # Get the current date
    today = datetime.now().date()

    # Calculate the date 30 days ago
    thirty_days_ago = today - timedelta(days=30)

    # Filter costs added within the last 30 days for the current user
    costs_within_30_days_chiqim = current_user.cost_set.filter(
        Q(created__date__gte=thirty_days_ago) & Q(created__date__lte=today) & Q(transaction_type='Chiqim')
    )

    # Calculate the total amount of costs within the last 30 days
    summa = costs_within_30_days_chiqim.aggregate(Sum('amount'))['amount__sum'] or 0

    # Render the template with the context
    return render(request, 'app_main/chiqim_30_days.html', {
        'costs_within_30_days_chiqim': costs_within_30_days_chiqim,
        'summa': summa
    })



@login_required
def kirim_get_costs_within_7_days(request):
    """
    View function to retrieve costs added within the last 7 days for the current user.

    This view is accessible only to authenticated users. It retrieves the costs added within
    the last 7 days (including today) for the current authenticated user with transaction type 'Kirim'.
    It calculates the total amount of costs within this period.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'chiqim_7_days.html' template with the following context:
            - 'costs_within_7_days_chiqim': A queryset containing costs within the last 7 days.
            - 'summa': The total amount of costs within the last 7 days.
    """
    # Get the current user
    current_user = request.user

    # Get the current date
    today = datetime.now().date()

    # Calculate the date 7 days ago
    seven_days_ago = today - timedelta(days=7)

    # Filter costs added within the last 7 days for the current user with transaction type 'Kirim'
    costs_within_7_days_kirim = current_user.cost_set.filter(
        Q(created__date__gte=seven_days_ago) & Q(created__date__lte=today) & Q(transaction_type='Kirim')
    )

    # Calculate the total amount of costs within the last 7 days
    summa = costs_within_7_days_kirim.aggregate(Sum('amount'))['amount__sum'] or 0

    # Render the template with the context
    return render(request, 'app_main/chiqim_7_days.html', {
        'costs_within_7_days_chiqim': costs_within_7_days_kirim,
        'summa': summa
    })



@login_required
def kirim_get_costs_within_30_days(request):
    """
    View function to retrieve costs added within the last 30 days for the current user.

    This view is accessible only to authenticated users. It retrieves the costs added within
    the last 30 days (including today) for the current authenticated user with transaction type 'Kirim'.
    It calculates the total amount of costs within this period.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'kirim_30_days.html' template with the following context:
            - 'costs_within_30_days_kirim': A queryset containing costs within the last 30 days.
            - 'summa': The total amount of costs within the last 30 days.
    """
    # Get the current user
    current_user = request.user

    # Get the current date
    today = datetime.now().date()

    # Calculate the date 30 days ago
    thirty_days_ago = today - timedelta(days=30)

    # Filter costs added within the last 30 days for the current user with transaction type 'Kirim'
    costs_within_30_days_kirim = current_user.cost_set.filter(
        Q(created__date__gte=thirty_days_ago) & Q(created__date__lte=today) & Q(transaction_type='Kirim')
    )

    # Calculate the total amount of costs within the last 30 days
    summa = costs_within_30_days_kirim.aggregate(Sum('amount'))['amount__sum'] or 0

    # Render the template with the context
    return render(request, 'app_main/kirim_30_days.html', {
        'costs_within_30_days_kirim': costs_within_30_days_kirim,
        'summa': summa
    })
