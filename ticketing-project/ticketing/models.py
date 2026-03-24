from django.db import models

# Create your models here.
class EquipmentRequest(models.Model):
    REQUEST_TYPE_CHOICES = [
        ("laptop", "Ноутбук")
        , ("monitor", "Монітор")
        , ("mouse", "Мишка")
        , ("software", "Доступ до ПО")
    ]

    PRIORITY_CHOICES = [
        (1, "Низкий")
        , (2, "Середній")
        , (3, "Високий")
        , (4, "Терміновий")
    ]

    STATUS_CHOICES = [
        (1, "Нова")
        , (2, "В роботі")
        , (3, "Зроблено")
        , (4, "Відхилено")
    ]

    employee_name = models.CharField(verbose_name="Ім'я працівника", max_length=120)
    employee_email = models.EmailField(verbose_name="email працівника")
    request_type = models.CharField(verbose_name="Тип запиту", max_length=20, choices=REQUEST_TYPE_CHOICES)
    priority = models.IntegerField(verbose_name="Пріорітет", choices=PRIORITY_CHOICES)
    description = models.TextField(verbose_name="Опис")
    status = models.IntegerField(verbose_name="Статус", choices=STATUS_CHOICES, default=1)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee_name} - {self.status}"
