from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    ShoppingList,
    Subscription,
)

User = get_user_model()


class RecipesSerializerMixin(metaclass=serializers.SerializerMetaclass):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        fields = ["id", "user"]
        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(), fields=["id", "user"]
            )
        ]


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["title", "dimension"]


class SubscriptionSerializer(
    RecipesSerializerMixin, serializers.ModelSerializer
):
    id = serializers.SlugRelatedField(
        slug_field="id", queryset=User.objects.all(), source="author"
    )

    class Meta:
        model = Subscription
        fields = RecipesSerializerMixin.Meta.fields


class FavoriteSerializer(RecipesSerializerMixin, serializers.ModelSerializer):
    id = serializers.SlugRelatedField(
        slug_field="id", queryset=Recipe.objects.all(), source="recipe"
    )

    class Meta:
        model = Favorite
        fields = RecipesSerializerMixin.Meta.fields


class ShoppingListSerializer(
    RecipesSerializerMixin, serializers.ModelSerializer
):
    id = serializers.SlugRelatedField(
        slug_field="id", queryset=Recipe.objects.all(), source="recipe"
    )

    class Meta:
        model = ShoppingList
        fields = RecipesSerializerMixin.Meta.fields
