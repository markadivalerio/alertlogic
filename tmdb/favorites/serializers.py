from rest_framework import serializers
from favorites.models import Favorites

class FavoritesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Favorites
		fields = ('title', 'person')