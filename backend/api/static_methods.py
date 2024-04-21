from datetime import datetime

from django.http import FileResponse

from recipes.models import IngredientRecipe


def download_shopping_cart_static(ingredients):
    today = datetime.today()
    shopping_cart = f"Список покупок для Вас на {today:%d-%m-%Y}\n\n"
    shopping_cart += "\n".join(
        [
            f'- {ingredient["ingredient__name"]} '
            f'({ingredient["ingredient__measurement_unit"]})'
            f' - {ingredient["amount"]}'
            for ingredient in ingredients
        ],
    )
    shopping_cart += f"\n\nFoodgram. Виноградов Петр. {today:%Y}"

    filename = "shopping_cart.txt"
    response = FileResponse(shopping_cart, content_type="text/plain")
    response["Content-Disposition"] = f"attachment; filename={filename}"
    return response


def bulk_create_ingredients(self, ingredients_data, recipe):
    IngredientRecipe.objects.bulk_create(
        [
            IngredientRecipe(
                ingredient_id=(self.initial_data["ingredients"][number]["id"]),
                recipe=recipe,
                amount=ingredient["amount"],
            )
            for number, ingredient in enumerate(ingredients_data)
        ],
    )
