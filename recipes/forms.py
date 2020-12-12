from django import forms

from .models import Recipe, RecipeTag, Ingredient, RecipeIngredient


class RecipeForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=RecipeTag.objects.all(), to_field_name="slug"
    )
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(), to_field_name="title"
    )
    amount = []

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
            for tag in (
                "breakfast",
                "lunch",
                "dinner",
            ):
                if tag in data:
                    data.update({"tags": tag})
            ingredients = self.get_ingredients(data)
            for item in ingredients:
                data.update({"ingredients": item})
            self.amount = self.get_amount(data)

        super().__init__(data=data, *args, **kwargs)

    def save(self, commit=True):
        recipe = super().save(commit=False)
        print(self.cleaned_data)
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
