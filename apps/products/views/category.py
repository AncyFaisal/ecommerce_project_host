# views/category.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator




from apps.sanjeri_models import Category
from apps.sanjeri_forms import CategoryForm

def admin_required(function):
    """
    Decorator to ensure user is admin/staff
    """
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Please login to access admin panel.")
            return redirect('user_login')
        if not request.user.is_staff and not request.user.is_superuser:
            messages.error(request, "You don't have permission to access this page.")
            return redirect('homepage')
        return function(request, *args, **kwargs)
    return wrapper

@admin_required
def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            try:
                category = form.save()
                messages.success(request, f"Category '{category.name}' added successfully!")
                return redirect('category_manage')
            except Exception as e:
                messages.error(request, f"Error creating category: {str(e)}")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CategoryForm()

    return render(request, 'category_add.html', {'form': form})

@admin_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            try:
                category = form.save()
                messages.success(request, f"Category '{category.name}' updated successfully!")
                return redirect('category_manage')
            except Exception as e:
                messages.error(request, f"Error updating category: {str(e)}")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CategoryForm(instance=category)

    return render(request, 'category_edit.html', {'form': form, 'category': category})

@admin_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.is_deleted = True
    category.save()
    messages.success(request, "Category deleted successfully!")
    return redirect('category_manage')

@admin_required
def category_manage(request):
    categories = Category.objects.filter(is_deleted=False)

    # Get filter parameters
    query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    sort_by = request.GET.get('sort', 'newest')

    # Apply search filter
    if query:
        categories = categories.filter(name__icontains=query)

    # Apply status filter
    if status_filter == 'active':
        categories = categories.filter(is_active=True)
    elif status_filter == 'inactive':
        categories = categories.filter(is_active=False)

    # Apply sorting
    if sort_by == 'oldest':
        categories = categories.order_by('id')
    elif sort_by == 'name_asc':
        categories = categories.order_by('name')
    elif sort_by == 'name_desc':
        categories = categories.order_by('-name')
    else:  # newest first (default)
        categories = categories.order_by('-id')

    # Pagination
    paginator = Paginator(categories, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "query": query,
        "status_filter": status_filter,
        "sort_by": sort_by,
    }
    return render(request, "category_manage.html", context)

# @login_required
@admin_required
def category_filter(request):
    # Placeholder for future expansion
    return render(request, "category_filter.html")

# @login_required
@admin_required
def category_success(request):
    return render(request, 'category_success.html')

