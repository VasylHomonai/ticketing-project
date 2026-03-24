from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from .forms import EquipmentRequestForm, EquipmentRequestFilterForm
from .models import EquipmentRequest


# Create your views here.
def request_create_view(request):
    if request.method == 'POST':
        form = EquipmentRequestForm(request.POST)

        if form.is_valid():
            equipment_request = form.save()

            messages.success(
                request, f'Заявка для {equipment_request.employee_name} успішно створена'
            )

            if equipment_request.priority == 'urgent':
                messages.warning(
                    request,
                    'Термінова задача відправлена'
                )

            return redirect('request_list')
        else:
            messages.error(
                request,
                'Форма має помилки. Перевірте форму.'
            )
    else:
        form = EquipmentRequestForm()

    return render(request, 'applications/request_form.html', {
        'form': form,
        'is_edit': False
    })


def request_list_view(request):
    queryset = EquipmentRequest.objects.all()

    # форма фільтра
    filter_form = EquipmentRequestFilterForm(request.GET or None)

    if filter_form.is_valid():
        employee_email = filter_form.cleaned_data.get('employee_email')
        status = filter_form.cleaned_data.get('status')
        priority = filter_form.cleaned_data.get('priority')

        if employee_email:
            queryset = queryset.filter(employee_email__icontains=employee_email)

        if status:
            queryset = queryset.filter(status=status)

        if priority:
            queryset = queryset.filter(priority=priority)

    # сортування
    sort = request.GET.get('sort', '-created_at')

    allowed_sorts = [
        'created_at', '-created_at',
        'priority', '-priority',
        'status', '-status'
    ]

    if sort in allowed_sorts:
        queryset = queryset.order_by(sort)

    context = {
        'requests': queryset,
        'filter_form': filter_form,
        'current_sort': sort,
        'current_sort_field': sort.lstrip('-'),
        'current_sort_direction': 'desc' if sort.startswith('-') else 'asc',
    }

    return render(request, 'applications/tasks_list.html', context)


def request_update_view(request, pk):
    equipment_request = get_object_or_404(EquipmentRequest, pk=pk)

    if request.method == 'POST':
        form = EquipmentRequestForm(request.POST, instance=equipment_request, is_edit=True)

        if form.is_valid():
            form.save()
            messages.success(request, 'Заявка оновлена')
            return redirect('request_list')
    else:
        form = EquipmentRequestForm(instance=equipment_request, is_edit=True)

    return render(request, 'applications/request_form.html', {
        'form': form,
        'is_edit': True
    })
