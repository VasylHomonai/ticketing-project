from django import forms
from .models import EquipmentRequest


class EquipmentRequestFilterForm(forms.Form):
    employee_email = forms.EmailField(required=False, label='Email співробітника')

    status = forms.ChoiceField(
        required=False,
        label='Статус',
        choices=[
            ('', 'Всі статуси')
            , (1, 'нова')
            , (2, 'в роботі')
            , (3, 'виконана')
            , (4, 'відхилина')
        ]
    )

    priority = forms.ChoiceField(
        required=False,
        label='Пріоритет',
        choices=[
            ('', 'Всі пріорітети')
            , (1, "Низкий")
            , (2, "Середній")
            , (3, "Високий")
            , (4, "Терміновий")
        ]
    )


class EquipmentRequestForm(forms.ModelForm):
    class Meta:
        model = EquipmentRequest
        fields = [
            'employee_name'
            , 'employee_email'
            , 'request_type'
            , 'priority'
            , 'status'
            , 'description'
        ]
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Опишіть задачу'
            }),
        }

    def __init__(self, *args, **kwargs):
        is_edit = kwargs.pop('is_edit', False)
        super().__init__(*args, **kwargs)

        if not is_edit:
            # ховаємо статус при створенні
            self.fields.pop('status')
        else:
            # блокуємо інші поля при редагуванні
            for field in self.fields:
                if field not in ['status', 'priority']:
                    self.fields[field].disabled = True

    def clean_employee_name(self):
        employee_name = self.cleaned_data.get('employee_name').strip()

        if not employee_name:
            raise forms.ValidationError('Порожнє ім\'я')
        if len(employee_name) < 2:
            raise forms.ValidationError('Ім\'я не може містити менше 2 символів')

        return employee_name

    def clean_description(self):
        description = self.cleaned_data.get('description').strip()

        if len(description) < 10:
            raise forms.ValidationError('Короткий опис, потрібно більше 10 символів')

        if len(description) > 250:
            raise forms.ValidationError('Опис має містити менше 250 символів')

        return description

    def clean(self):
        cleaned_data = super().clean()
        request_type = cleaned_data.get('request_type')
        priority = cleaned_data.get('priority')
        description = cleaned_data.get('description', '').lower()

        if request_type == 'software' and 'злам' not in description and 'не працює' not in description:
            self.add_error('description', 'Для заміни ПО потрібно вказати що саме зламано')

        if priority == 4 and len(description) < 20:
            self.add_error('description', 'Для термінової заявки потрібно детальний опис')

        return cleaned_data
