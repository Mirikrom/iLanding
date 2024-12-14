from django.db import models
from django.core.exceptions import ValidationError


class MenuItem(models.Model):
    title = models.CharField(max_length=255)  # Menyu elementining nomi
    url = models.CharField(max_length=255, blank=True, null=True)  # Havola manzili
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="children"
    )  # Ota-ona menyu elementi
    sort_order = models.IntegerField(default=0)  # Tartib raqami
    is_active = models.BooleanField(default=True)  # Faollik holati

    class Meta:
        ordering = ["sort_order"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Avval saqlash kerak
        if not self.url:  # agar url berilmagan bo'lsa
            self.url = f"/basic/{self.id}/"  # id endi mavjud
            super().save(*args, **kwargs)  # qayta saqlash


class CustomerAvatar(models.Model):
    image = models.ImageField(upload_to="avatars/")
    alt_text = models.CharField(max_length=100)
    sort_order = models.IntegerField(default=0)
    list_display = ("alt_text", "sort_order", "image")

    class Meta:
        ordering = ["sort_order"]

    def __str__(self):
        return self.alt_text


class Hero(models.Model):
    badge_text = models.CharField(max_length=255)
    title_line = models.CharField(max_length=255)
    description = models.TextField()

    # Buttons
    start_button_text = models.CharField(max_length=100, blank=True, null=True)
    start_button_url = models.CharField(max_length=255, blank=True, null=True)

    # Video
    video_button_text = models.CharField(max_length=100, blank=True, null=True)
    video_url = models.CharField(max_length=255, blank=True, null=True)
    video_file = models.FileField(upload_to="videos/", blank=True, null=True)

    # Hero image
    hero_image = models.ImageField(upload_to="hero/", blank=True, null=True)

    # Customers section
    customers_text = models.CharField(max_length=255)
    customer_avatars = models.ManyToManyField(CustomerAvatar)
    additional_customers_count = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Section"

    def __str__(self):
        return "Hero Section"

    @property
    def visible_avatars(self):
        """Faqat birinchi 5ta avatarni qaytaradi"""
        return self.customer_avatars.all().order_by("sort_order")[:5]


class SiteConfig(models.Model):
    site_name = models.CharField(max_length=255, default="iLanding")
    logo = models.ImageField(upload_to="logo/", blank=True, null=True)
    favicon = models.ImageField(upload_to="favicon/", blank=True, null=True)

    def __str__(self):
        return f"Site Configuration: {self.site_name}"

    def save(self, *args, **kwargs):
        # Faqat bitta site konfiguratsiyasini saqlash
        if not self.pk and SiteConfig.objects.exists():
            raise ValidationError("Faqat bitta site konfiguratsiyasi yaratish mumkin")
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Site Configuration"


class About(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    feature_list = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    phone_label = models.CharField(max_length=20, null=True, blank=True)
    main_image = models.ImageField(upload_to="about/", null=True, blank=True)
    small_image = models.ImageField(upload_to="about/", null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    url_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return "About Section"

    class Meta:
        verbose_name = "About Section"


class FeatureSection(models.Model):
    """
    Bo'lim haqida umumiy ma'lumot (bir marta kiritiladi).
    """

    title = models.CharField(
        max_length=200, default="Features", help_text="Bo'limning nomi."
    )
    description = models.TextField(
        default="Necessitatibus eius consequatur ex aliquid fuga eum quidem sint consectetur velit",
        help_text="Bo'limning umumiy izohi.",
    )

    def __str__(self):
        return self.title


class FeatureTab(models.Model):
    """
    Har bir tab (oyna) uchun alohida ma'lumotlar.
    """

    section = models.ForeignKey(
        FeatureSection,
        on_delete=models.CASCADE,
        related_name="tabs",
        help_text="Qaysi bo'limga tegishli ekanligini belgilaydi.",
    )
    title = models.CharField(
        max_length=200, help_text="Tabning nomi (masalan, 'Modisit')."
    )
    heading = models.CharField(max_length=200, help_text="Tab ichidagi katta sarlavha.")
    description = models.TextField(help_text="Tab uchun qisqacha matn.")
    points = models.TextField(
        help_text="Tab ichidagi ro'yxatdagi elementlar (yangi qatordan yozing).",
        null=True,
        blank=True,
    )
    image = models.ImageField(upload_to="features/", help_text="Tab uchun tasvir.")
    order = models.PositiveIntegerField(
        default=0, help_text="Tabning tartib raqami (kichik raqam birinchi bo'ladi)."
    )

    class Meta:
        ordering = ["order"]  # Tartibga solish
        verbose_name = "Feature Tab"
        verbose_name_plural = "Feature Tabs"

    def get_points_as_list(self):
        """Ro'yxat elementlarini (points) qaytaradi."""
        if self.points:  # Agar points mavjud bo'lsa
            return self.points.split("\n")
        return []  # Agar points bo'sh bo'lsa, bo'sh ro'yxat qaytaradi

    def __str__(self):
        return f"{self.title} ({self.section.title})"


class BasicPage(models.Model):
    title = models.CharField(
        max_length=255, verbose_name="Sarlavha"
    )  # Basic Page sarlavhasi
    menu_item = models.OneToOneField(
        MenuItem,
        on_delete=models.CASCADE,
        null=True,  # Maydon nullable bo'lishi uchun
        blank=True, # Adminda to'ldirilmasligi mumkin
        related_name='basic_page',
        verbose_name="Menu elementi",
        help_text="Bu sahifa qaysi menu elementi uchun",
        limit_choices_to={
            'url__startswith': '/basic/', # Faqat /basic/ URL li menular
        }
    )
    content = models.TextField(
        verbose_name="Kontent", blank=True, null=True
    )  # Basic Page asosiy matni
    image = models.ImageField(
        upload_to="basic_pages/", verbose_name="Rasm", blank=True, null=True
    )  # Sahifaga rasm
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Yaratilgan sana"
    )  # Avtomatik sana
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Yangilangan sana"
    )  # Avtomatik yangilanish sanasi
    is_active = models.BooleanField(
        default=True, verbose_name="Faolmi?"
    )  # Sahifa faollik holati

    def __str__(self):
        return self.title  # Admin interfeysda sahifani nomi ko'rinadi