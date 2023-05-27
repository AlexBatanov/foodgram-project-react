def chek_is_favorite_and_is_shoping_list(context, obj, model):
    """Проверяет нахождение объекта в избранном или в карте покупок"""

    user = context['request'].user
    return (
        user.is_authenticated and 
        model.objects.filter(recipe=obj, user=user).exists()
    )