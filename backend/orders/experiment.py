

class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор пользователя.
    """
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous or user == obj:
            return False
        return obj.subscribers.filter(subscriber=user).exists()


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор тегов.
    """

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор ингредиентов.
    """

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор ингредиентов в рецепте (только чтение).
    """

    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = [
            'id',
            'name',
            'measurement_unit',
            'amount',
        ]


class IngredientInRecipeWritableSerializer(serializers.ModelSerializer):
    """
    Сериализатор ингредиентов в рецепте (для изменения).
    """

    id = serializers.IntegerField()
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = [
            'id',
            'name',
            'measurement_unit',
            'amount',
        ]


class RecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор рецептов.
    """

    tags = TagSerializer(many=True)
    ingredients = IngredientInRecipeSerializer(
        source='ingredientinrecipe_set',
        many=True
    )
    author = UserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(
            user=user,
            recipe=obj,
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return obj.shopping_cart.filter(user=user).exists()


class RecipeWritableSerializer(RecipeSerializer):
    """
    Сериализатор рецептов для изменения.
    """

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    ingredients = IngredientInRecipeWritableSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def set_tags_and_ingredients(self, recipe, tags, ingredients):
        """
        Установка тегов и ингредиентов.
        """
        if tags:
            recipe.tags.clear()
            recipe.tags.set(tags)
        if ingredients:
            IngredientInRecipe.objects.filter(recipe=recipe).delete()
            IngredientInRecipe.objects.bulk_create(
                [IngredientInRecipe(
                    recipe=recipe,
                    ingredient_id=ingredient['id'],
                    amount=ingredient['amount'],
                ) for ingredient in ingredients]
            )

    def create(self, validated_data):
        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredients', None)
        recipe = Recipe.objects.create(**validated_data)
        self.set_tags_and_ingredients(recipe, tags, ingredients)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredients', None)
        instance = super().update(instance, validated_data)
        self.set_tags_and_ingredients(instance, tags, ingredients)
        return instance

    def validate(self, attrs):
        ingredients = attrs.get('ingredients')
        if not ingredients:
            raise ValidationError('Нужен хотя бы один ингредиент')
        ingredient_ids = [ingredient['id'] for ingredient in ingredients]
        if len(ingredient_ids) != len(set(ingredient_ids)):
            raise ValidationError('Ингредиенты не должны повторяться')
        for ingredient in ingredients:
            if ingredient['amount'] <= 0:
                raise ValidationError(
                    'Количество ингредиента должно быть больше 0'
                )
            if not Ingredient.objects.filter(pk=ingredient['id']).exists():
                raise ValidationError('Такого ингредиента не существует')

        tags = attrs.get('tags')
        if not tags:
            raise ValidationError('Нужен хотя бы один тег')
        tag_ids = [tag.id for tag in tags]
        if len(tag_ids) != len(set(tag_ids)):
            raise ValidationError('Теги не должны повторяться')

        image = attrs.get('image')
        if not image:
            raise ValidationError('Изображение не выбрано')
        return attrs

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeSerializer(instance, context=context).data


class RecipeInSubscriptionSerializer(serializers.ModelSerializer):
    """
    Сериализатор рецептов в подписках.
    """

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Сериализатор подписок.
    Используется только для просмотра своих подписок.
    """

    id = serializers.ReadOnlyField(source='user.id')
    username = serializers.ReadOnlyField(source='user.username')
    email = serializers.ReadOnlyField(source='user.email')
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_is_subscribed(self, obj):
        """
        Всегда будет True
        """
        return True

    def get_recipes_count(self, obj):
        """
        Количество рецептов пользователя
        """
        return obj.user.recipes.count()

    def get_recipes(self, obj):
        """
        Список рецептов пользователя
        """
        request = self.context.get('request')
        recipes_limit = request.GET.get('recipes_limit')
        recipes = obj.user.recipes.all()
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        return RecipeInSubscriptionSerializer(recipes, many=True).data