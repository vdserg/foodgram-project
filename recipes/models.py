from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(
        max_length=20,
    )
    dimension = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.title}, {self.dimension}"


class RecipeTag(models.Model):
    title = models.CharField(max_length=10)
    slug = models.SlugField()

    def __str__(self):
        return f"{self.title}"


class Recipe(models.Model):

    title = models.CharField(max_length=40, null=False)
    author = models.ForeignKey(
        User, related_name="recipes", on_delete=models.CASCADE
    )
    image = models.ImageField()
    pub_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=500, null=False)
    ingredients = models.ManyToManyField(
        Ingredient, through="RecipeIngredient"
    )
    tags = models.ManyToManyField(
        RecipeTag,
        related_name="recipe_tags",
    )
    time_to_cook = models.PositiveSmallIntegerField(
        help_text="Длительность в минутах"
    )

    class Meta:
        ordering = ("-pub_date",)

    def __str__(self):
        return f"{self.title}"

    @property
    def favorite_count(self):
        return self.favorites.count()


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="recipe_ingredients"
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name="recipes"
    )
    amount = models.PositiveIntegerField()

    def __str__(self):
        return (
            f"{self.ingredient.title} {self.amount}{self.ingredient.dimension}"
        )


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="favorites"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="favorites"
    )

    class Meta:
        unique_together = ("recipe", "user")

    def __str__(self):
        return f"{self.recipe} в избранном у {self.user}"


class Subscription(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower"
    )

    class Meta:
        unique_together = ("user", "author")

    def __str__(self):
        return f"{self.user} подписан на {self.author}"


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="shopping_list"
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="shopping_list"
    )

    class Meta:
        unique_together = (
            "user",
            "recipe",
        )

    def __str__(self):
        return f"User: {self.user.username} Recipe: {self.recipe.title}"
