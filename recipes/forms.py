from django import forms
from django.core.exceptions import ValidationError

from .models import Ingredient, Recipe, RecipeIngredient, RecipeTag


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            "title",
            "tags",
            "ingredients",
            "description",
            "time_to_cook",
            "image",
        ]

    def __init__(self, data=None, *args, **kwargs):
        if data:
            data = data.copy()
            for tag in RecipeTag.DINNER, RecipeTag.LUNCH, RecipeTag.BREAKFAST:
                if tag in data:
                    data.update({"tags": RecipeTag.objects.get(slug=tag)})
            ingredients = self.get_ingredients(data)
            for item in ingredients:
                try:
                    data.update(
                        {"ingredients": Ingredient.objects.get(title=item)}
                    )
                except Ingredient.DoesNotExist:
                    ValidationError(
                        "Ингредиент не существует, выберите из списка"
                    )
            self.amount = self.get_amount(data)
        super().__init__(data=data, *args, **kwargs)

    def save(self, commit=True):
        recipe = super().save(commit=False)
        recipe.save()

        ingredients_amount = self.amount
        recipe.ingredients.all().delete()
        recipe_ingredients = [
            RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient,
                amount=ingredients_amount[ingredient.title],
            )
            for ingredient in self.cleaned_data["ingredients"]
        ]
        recipe.recipe_ingredients.set(recipe_ingredients, bulk=False)

        recipe.tags.set(self.cleaned_data["tags"])

        self.save_m2m()
        return recipe

    def get_ingredients(self, query):
        ingredients = [
            query[key]
            for key in query.keys()
            if key.startswith("nameIngredient")
        ]
        return ingredients

    def get_amount(self, query):
        result = {}
        for key in query.keys():
            if key.startswith("nameIngredient"):
                n = key.split("_")[1]
                result[query[f"nameIngredient_{n}"]] = query[
                    f"valueIngredient_{n}"
                ]
        return result
