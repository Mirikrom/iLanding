from django.contrib import admin
from .models import MenuItem, Hero, CustomerAvatar, SiteConfig, About, FeatureTab, FeatureSection, BasicPage
from django import forms

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'sort_order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title',)
    ordering = ('sort_order',)  # Tartib bo'yicha saralash
    autocomplete_fields = ['parent']  # Parent menu uchun ham dropdown

@admin.register(CustomerAvatar)
class CustomerAvatarAdmin(admin.ModelAdmin):
    list_display = ('alt_text', 'sort_order','image')
    search_fields = ('alt_text',)

@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Badge & Title', {
            'fields': ('badge_text', 'title_line', 'description')
        }),
        ('Get Started Button', {
            'fields': ('start_button_text', 'start_button_url'),
            'classes': ('collapse',),
            'description': "Ixtiyoriy. Agar button kerak bo'lmasa bo'sh qoldiring"
        }),
        ('Video', {
            'fields': ('video_button_text', 'video_url', 'video_file'),
            'classes': ('collapse',),
            'description': "Ixtiyoriy. Video URL yoki fayl yuklang. Agar video kerak bo'lmasa bo'sh qoldiring"
        }),
        ('Hero Image', {
            'fields': ('hero_image',),
            'description': "Ixtiyoriy. Agar rasm kerak bo'lmasa bo'sh qoldiring"
        }),
        ('Customers', {
            'fields': ('customers_text', 'customer_avatars', 'additional_customers_count'),
            'description': "Mijozlar haqida ma'lumot"
        })
    )

    def has_add_permission(self, request):
        # Agar allaqachon Hero mavjud bo'lsa, yangi qo'shishga ruxsat bermaydi
        return not Hero.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Heroни o'chirishga ruxsat beradi
        return True



@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Agar allaqachon SiteConfig mavjud bo'lsa, yangi qo'shishga ruxsat bermaydi
        return not SiteConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # SiteConfigni o'chirishga ruxsat beradi
        return True

    fieldsets = (
        ('Site Information', {
            'fields': ('site_name',),
            'description': "Sayt nomi va asosiy konfiguratsiyasi"
        }),
        ('Logo', {
            'fields': ('logo',),
            'description': "Sayt logosi (ixtiyoriy)"
        }),
        ('Favicon', {
            'fields': ('favicon',),
            'description': "Sayt favicon ikonkasi (ixtiyoriy)"
        })
    )

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    fieldsets = (
        ('About Section', {
            'fields': ('title', 'description', 'feature_list', 'phone_number', 'phone_label', 'main_image', 'small_image', 'url', 'url_name'),
        }),
    )

    def save_model(self, request, obj, form, change):
        # feature_list ni vergul bilan ajratilgan ro'yxatga aylantirish
        if obj.feature_list:
            obj.feature_list = ','.join([feature.strip() for feature in obj.feature_list.split(',')])
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        # Agar allaqachon About mavjud bo'lsa, yangi qo'shishga ruxsat bermaydi
        return not About.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Aboutni o'chirishga ruxsat beradi
        return True


class FeatureTabInline(admin.TabularInline):
    model = FeatureTab
    extra = 1  # Admin panelda qo'shimcha joy ochiladi

@admin.register(FeatureSection)
class FeatureSectionAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Agar allaqachon SiteConfig mavjud bo'lsa, yangi qo'shishga ruxsat bermaydi
        return not FeatureSection.objects.exists()
    list_display = ("title",)
    inlines = [FeatureTabInline]


@admin.register(FeatureTab)
class FeatureTabAdmin(admin.ModelAdmin):
    list_display = ("title", "section", "order")
    list_editable = ("order",)
    search_fields = ("title", "section__title")
    ordering = ("section", "order")


class BasicPageForm(forms.ModelForm):
    class Meta:
        model = BasicPage
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # menu_item field borligini tekshiramiz
        if 'menu_item' in self.fields:
            # Har doim basic_page__isnull=True ni tekshiramiz
            self.fields['menu_item'].queryset = MenuItem.objects.filter(
                url__startswith='/basic/',
                basic_page__isnull=True
            )
            # Agar bu tahrirlash bo'lsa, hozirgi menu_item ni ham qo'shamiz
            if self.instance.pk and self.instance.menu_item:
                self.fields['menu_item'].queryset = self.fields['menu_item'].queryset | MenuItem.objects.filter(id=self.instance.menu_item.id)
                
@admin.register(BasicPage)
class BasicPageAdmin(admin.ModelAdmin):
    form = BasicPageForm
    list_display = ('title', 'menu_item', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'menu_item')
    search_fields = ('title', 'content', 'menu_item__title')
    ordering = ('-created_at',)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # agar obyekt mavjud bo'lsa (ya'ni tahrirlash rejimida)
            return self.readonly_fields + ('menu_item',)
        return self.readonly_fields