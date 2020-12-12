from django.urls import reverse_lazy

from .models import RecipeTag, ShoppingList


class IsAuthorMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user != self.get_object().author:
            return reverse_lazy("recipes:recipe", kwargs.get("pk"))
        return super().dispatch(request, *args, **kwargs)


class TagFilterMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.getlist("tag")
        if q:
            return queryset.filter(tags__slug__in=q).distinct()
        return queryset


class RecipeMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["tags"] = RecipeTag.objects.all()
        if self.request.user.is_authenticated:
            context[
                "favorite_list"
            ] = self.request.user.favorites.all().values_list(
                "recipe_id", flat=True
            )
            context["subscribers"] = (
                self.request.user.follower.all()
                .values_list("author__id", flat=True)
                .distinct()
            )
            context["cart_list"] = ShoppingList.objects.filter(
                user=self.request.user
            ).values_list("recipe__id", flat=True)

        return context
