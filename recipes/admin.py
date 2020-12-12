from django.contrib import admin

from .models import (
    Recipe,
    RecipeTag,
    Ingredient,
    Subscription,
    Favorite,
    ShoppingList,
)


class RecipeIngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through


class RecipeAdmin(admin.ModelAdmin):
    readonly_fields = ("favorite_count",)

    list_display = ("title", "author")
    search_fields = (
        "title",
        "author__username",
    )
    list_filter = ("author", "tags")
    inlines = (RecipeIngredientInline,)


class IngredientAdmin(admin.ModelAdmin):
    pass


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeTag)
admin.site.register(Favorite)
admin.site.register(Subscription)
admin.site.register(ShoppingList)
