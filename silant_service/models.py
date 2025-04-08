from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

# Клиент
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default="Пользователь", verbose_name='Наименование компании')
    created_at = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return f"{self.name}" if self.user else self.name
    
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

# Сервисная компания
class ServiceCompany(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, 
    null=True,
    blank=True
)
    name = models.CharField(max_length=255, default="ООО Сервис", verbose_name='Наименование компании')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.name}" if self.user else self.name
    
    class Meta:
        verbose_name = 'Сервисная компания'
        verbose_name_plural = 'Сервисные компании'

# Менеджер
class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name='Имя менеджера')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name}" if self.user else self.name 
    
    class Meta:
        verbose_name = 'Менеджер'
        verbose_name_plural = 'Менеджеры'

# Модель для справочников
class ReferenceItem(models.Model):
    MODEL_TECH = 'model'
    TYPE_ENGINE = 'engine'
    TYPE_TRANSMISSION = 'transmission'
    TYPE_AXLE = 'axle'
    TYPE_MAN_AXLE = 'managed_axle'
    TYPE_TO = 'TO'
    TO_ORGANIZATION = 'to_organization'
    NODE_FAILURE = 'failure_node'
    RECOVERY_METHOD = 'recovery_method'

    type = models.CharField(
        max_length=50,
        choices=[
            (MODEL_TECH, 'Модель техники'),
            (TYPE_ENGINE, 'Модель двигателя'),
            (TYPE_TRANSMISSION, 'Модель трансмиссии'),
            (TYPE_AXLE, 'Модель моста'),
            (TYPE_MAN_AXLE, 'Модель управляемого моста'),
            (TYPE_TO, 'Вид ТО'),
            (TO_ORGANIZATION, 'Организация, проводившая ТО'),
            (NODE_FAILURE, 'Узел отказа'),
            (RECOVERY_METHOD, 'Способ восстановления'),
        ],
        verbose_name="Справочник"
    )
    name = models.CharField(max_length=255, verbose_name="Название", blank=True, unique=False)
    description = models.TextField(verbose_name="Описание", blank=True, unique=False)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Справочник'
        verbose_name_plural = 'Справочники'
    

# Модель "Машина"
class Vehicle(models.Model):
    serial_number = models.CharField(max_length=255, verbose_name="Зав. № машины", blank=False, unique=True)
    tech_model = models.ForeignKey(
        ReferenceItem,
        on_delete=models.PROTECT,
        related_name='tech_model',
        limit_choices_to={'type': ReferenceItem.MODEL_TECH},
        blank=True,
        null=True,
        verbose_name='Модель техники'
    )
    engine_model = models.ForeignKey(
        ReferenceItem,
        on_delete=models.PROTECT,
        related_name='machines_engine',
        limit_choices_to={'type': ReferenceItem.TYPE_ENGINE},
        blank=True,
        null=True,
        verbose_name='Модель двигателя'
    )
    serial_engine = models.CharField(max_length=255, verbose_name="Зав. № двигателя")
    model_transmission = models.ForeignKey(
        ReferenceItem,
        on_delete=models.PROTECT,
        related_name='machines_transmission',
        limit_choices_to={'type': ReferenceItem.TYPE_TRANSMISSION},
        blank=True,
        null=True,
        verbose_name='Модель трансмиссии'
    )
    serial_transmission = models.CharField(max_length=255, verbose_name="Зав. № трансмиссии")
    model_axle = models.ForeignKey(
        ReferenceItem,
        on_delete=models.PROTECT,
        related_name='machines_axle',
        limit_choices_to={'type': ReferenceItem.TYPE_AXLE},
        blank=True,
        null=True,
        verbose_name='Модель ведущего моста'
    )
    serial_axle = models.CharField(max_length=255, verbose_name="Зав. № ведущего моста")
    model_man_axle = models.ForeignKey(
        ReferenceItem,
        on_delete=models.PROTECT,
        related_name='machines_man_axle',
        limit_choices_to={'type': ReferenceItem.TYPE_MAN_AXLE},
        blank=True,
        null=True,
        verbose_name='Модель управляемого моста'
    )
    serial_man_axle = models.CharField(max_length=255, verbose_name="Зав. № управляемого моста")
    contract_number_data = models.CharField(max_length=255, verbose_name='Договор поставки №, дата')
    ship_date = models.DateField(verbose_name='Дата отгрузки с завода')
    recipient = models.CharField(max_length=255, verbose_name='Грузополучатель (конечный потребитель)')
    delivery_address = models.TextField(verbose_name='Адрес поставки (эксплуатации)')
    configuration = models.TextField(verbose_name='Комплектация (доп.опции)')
    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        null=True,
        related_name='vehicle',
        verbose_name='Клиент'
    )
    service_company = models.ForeignKey(
        ServiceCompany,
        on_delete=models.SET_NULL,
        null=True,
        related_name='vehicle',
        verbose_name='Сервисная компания'
    )

    def __str__(self):
        return f"{self.serial_number} - {self.tech_model.name if self.tech_model else 'Без модели'}"

    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'

# Модель для ТО
class TechnicalService(models.Model):
    service_type = models.ForeignKey(
        ReferenceItem,
        on_delete=models.PROTECT,
        related_name='service_type',
        limit_choices_to={'type': ReferenceItem.TYPE_TO},
        blank=True,
        null=True,
        verbose_name='Вид ТО'
    )
    service_date = models.DateField(verbose_name='Дата проведения ТО')
    operating_hours = models.FloatField(verbose_name='Наработка, м/час')
    order_number = models.CharField(max_length=100, verbose_name="№ заказ-наряда")
    order_date = models.DateField(verbose_name='Дата заказ-наряда')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, related_name='service', verbose_name='Машина')
    tech_company = models.ForeignKey(
        ServiceCompany,
        on_delete=models.SET_NULL,
        null=True,
        related_name='tech_company',
        verbose_name='Организация, проводившая ТО'
    )
    service_company = models.ForeignKey(
        ServiceCompany,
        on_delete=models.SET_NULL,
        null=True,
        related_name='service',
        verbose_name='Сервисная компания'
    )

    def __str__(self):
        return f"{self.service_type.name} for {self.vehicle.serial_number} on {self.service_date}"
    
    class Meta:
        verbose_name = "Техобслуживание"
        verbose_name_plural = "Техобслуживание"

# Модель Рекламации
class Complaint(models.Model):
    failure_date =  models.DateField(verbose_name='Дата отказа')
    operating_hours = models.FloatField(verbose_name='Наработка, м/час')
    failure_node = models.ForeignKey(
        ReferenceItem,
        on_delete=models.PROTECT,
        related_name='failure_nodes',
        limit_choices_to={'type': ReferenceItem.NODE_FAILURE},
        blank=True,
        null=True,
        verbose_name='Узел отказа'
    )
    failure_description = models.TextField(verbose_name='Описание отказа')
    recovery_method = models.ForeignKey(
        ReferenceItem,
        on_delete=models.SET_NULL,
        null=True,
        related_name='recovery_methods',
        limit_choices_to={'type': ReferenceItem.RECOVERY_METHOD},
        verbose_name='Способ восстановления'
    )
    spare_parts = models.TextField(verbose_name='Используемые запасные части')
    recovery_date = models.DateField(verbose_name='Дата восстановления')
    failure_duration = models.DurationField(blank=True, null=True, verbose_name='Время простоя техники')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, related_name='complaint', verbose_name='Машина') 

    def __str__(self):
        return f'Complaint for {self.vehicle.serial_number} - Failure Date: {self.failure_date}'
    
    class Meta:
        verbose_name = "Рекламация"
        verbose_name_plural = "Рекламации"