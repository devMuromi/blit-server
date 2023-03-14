from rest_framework import serilaizers

# class ImageSerializer(serializers.ModelSerializer):
#     image = serializers.ImageField(max_length=None, use_url=True)
#     title = serializers.CharField(max_length=100)
#     uploaded_at = serializers.DateTimeField(auto_now_add=True)
#     uploaded_by = serializers.ForeignKey("", verbose_name=_(""), on_delete=models.CASCADE)

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'image', 'title', 'uploaded_at', 'uploaded_by')