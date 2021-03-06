from rest_framework.response import Response
from rest_framework.views import APIView

from utils.create_recipe_name_choices import create_recipe_name_choice


class RecipeNameChoicesListAPIView(APIView):

    def get(self, request):
        recipe_name_choices_list = create_recipe_name_choice()
        print(recipe_name_choices_list)

        return Response({'recipe_name_choices_list': recipe_name_choices_list})
