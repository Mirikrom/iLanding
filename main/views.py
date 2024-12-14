from django.shortcuts import render, get_object_or_404
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from main.models import MenuItem, Hero, CustomerAvatar, SiteConfig, About, FeatureTab, FeatureSection


def get_menu_with_subitems(menu_items):
    """
    Rekursiv ravishda menu strukturasini yaratuvchi funksiya
    
    :param menu_items: Barcha menu elementlari
    :return: Hierarchik menu strukturasi
    """
    def build_menu(items, parent=None):
        result = []
        for item in items:
            if item.parent == parent:
                children = build_menu(items, item)
                result.append({
                    'item': item,
                    'children': children
                })
        return result

    return build_menu(menu_items)

def home(request):
    """
    Asosiy sahifa view funksiyasi
    
    :param request: HTTP so'rov
    :return: Render qilingan index sahifasi
    """
    # Faol menu elementlarini olish
    menu_items = MenuItem.objects.filter(is_active=True).order_by('sort_order')
    menu_structure = get_menu_with_subitems(menu_items)
    sections = FeatureSection.objects.prefetch_related("tabs").all()
    abouts = About.objects.all()
    for about in abouts:
        about.feature_list_split = about.feature_list.split(",") if about.feature_list else []
    
    # Hero section uchun xatoliklarni oldini olish
    hero = None
    try:
        hero = Hero.objects.first()
        
        # Agar hero_image bo'lmasa, None qilamiz
        if hero:
            # Agar hero_image mavjud bo'lmasa, None qilamiz
            if not hero.hero_image or not default_storage.exists(hero.hero_image.name):
                hero.hero_image = None
            
            # Video fayl yoki URL mavjud bo'lmasa, None qilamiz
            if hero.video_file:
                if not default_storage.exists(hero.video_file.name):
                    hero.video_file = None
            
            # Agar video_url bo'sh bo'lsa, None qilamiz
            if not hero.video_url:
                hero.video_url = None
    except Hero.DoesNotExist:
        hero = None
    
    context = {
        'menu_structure': menu_structure,
        'hero': hero,
        'site_config': SiteConfig.objects.first() or SiteConfig.objects.create(),
        'abouts': abouts,
        'sections': sections
    }
    return render(request, 'main/index.html', context)


def basic_page(request, menu_id=None):
    menu_items = MenuItem.objects.filter(is_active=True).order_by('sort_order')
    menu_structure = get_menu_with_subitems(menu_items)
    
    # Agar menu_id berilgan bo'lsa, o'sha menuni topamiz
    current_menu = None
    basic_page = None
    if menu_id:
        current_menu = get_object_or_404(MenuItem, id=menu_id)
        try:
            basic_page = current_menu.basic_page  # MenuItem ga bog'langan BasicPage ni olamiz
        except:
            basic_page = None  # Agar BasicPage topilmasa None qo'yamiz
    
    context = {
        'menu_structure': menu_structure,
        'site_config': SiteConfig.objects.first() or SiteConfig.objects.create(),
        'current_menu': current_menu,
        'basic_page': basic_page,  # BasicPage ma'lumotlarini qo'shdik
    }
    return render(request, 'main/basicpage.html', context)