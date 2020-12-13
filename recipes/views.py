import codecs
import csv

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import RecipeForm
from .models import (
    Favorite,
    Recipe,
    RecipeTag,
    ShoppingList,
    Subscription,
    User,
)
from .viewmixins import IsAuthorMixin, RecipeMixin, TagFilterMixin


class RecipeList(RecipeMixin, TagFilterMixin, ListView):
    model = Recipe
    paginate_by = 6
    queryset = (
        Recipe.objects.all()
        .select_related("author")
        .prefetch_related("tags__recipes")
    )
    extra_context = {"tags": RecipeTag.objects.all()}


class RecipeDetail(RecipeMixin, DetailView):
    model = Recipe
    template_name = "recipes/recipe_detail.html"


class AuthorRecipeList(RecipeList):
    model = Recipe
    template_name = "recipes/author_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["author"] = get_object_or_404(
            User, username=self.kwargs.get("username")
        )
        context["is_subscribed"] = Subscription.objects.filter(
            user=self.request.user,
            author__username=self.kwargs.get("username"),
        ).exists()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author__username=self.kwargs.get("username"))


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    template_name = "recipes/form.html"
    form_class = RecipeForm
    extra_context = {
        "action": "new",
    }

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("recipes:recipe", kwargs={"pk": self.object.pk})


class RecipeUpdateView(IsAuthorMixin, LoginRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "recipes/form.html"
    extra_context = {"action": "update"}

    def get_success_url(self):
        return reverse_lazy("recipes:recipe", kwargs={"pk": self.object.pk})


class RecipeDeleteView(IsAuthorMixin, LoginRequiredMixin, DeleteView):
    model = Recipe
    success_url = "recipes:recipe_list"

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("recipes:index")


class FavoriteListView(LoginRequiredMixin, RecipeList):
    template_name = "recipes/favorite_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        recipes = Favorite.objects.filter(user=self.request.user).values_list(
            "recipe_id", flat=True
        )
        return queryset.filter(id__in=recipes)


class SubscriptionListView(LoginRequiredMixin, ListView):
    template_name = "recipes/subscription_list.html"
    paginate_by = 6

    def get_queryset(self):
        queryset = (
            Subscription.objects.filter(user=self.request.user)
            .select_related(
                "author",
            )
            .prefetch_related("author__recipes")
        )
        return queryset


class ShoppingCartListView(LoginRequiredMixin, ListView):
    template_name = "recipes/shopping_cart_list.html"
    context_object_name = "cart"

    def get_queryset(self):
        queryset = ShoppingList.objects.select_related(
            "user", "recipe"
        ).filter(user=self.request.user)
        return queryset


class ShoppingListDownload(View):
    def get(self, request, *args, **kwargs):
        ingredients = (
            Recipe.objects.values(
                "ingredients__title", "ingredients__dimension"
            )
            .filter(shopping_list__user=request.user)
            .annotate(Sum("recipe_ingredients__amount"))
            .order_by("ingredients__title")
        )

        response = HttpResponse(content_type="text/csv")
        response.write(codecs.BOM_UTF8)
        response["Content-Disposition"] = (
            "attachment; " 'filename="shopping_list.csv"'
        )
        writer = csv.writer(response, delimiter=";")
        writer.writerow(["Ингредиент", "Единица измерения", "Количество"])
        for item in ingredients:
            writer.writerow(item.values())

        return response
