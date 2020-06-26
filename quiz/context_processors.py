from .models import Category, Tag


def common(request):
    context = {
        'category_list':Category.objects.all(),
        'tag_list':Tag.objects.all()
    }
    return context