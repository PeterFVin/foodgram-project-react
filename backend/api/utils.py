from datetime import datetime
from django.http import HttpResponse


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
    response = HttpResponse(shopping_cart, content_type="text/plain")
    response["Content-Disposition"] = f"attachment; filename={filename}"
    return response
