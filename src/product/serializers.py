import json
from rest_framework import serializers
from .models import Product, Variant, ProductVariant, ProductVariantPrice, ProductImage


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = (
            'id',
            'title',
            'description'
        )


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = (
            'id',
            'variant_title',
            'variant',
            'product'
        )
        read_only_fields = (
            'id',
            'created_at',
            'updated_at',
            'product'
        )


class VariantsSerializer(serializers.Serializer):
    option = serializers.CharField()
    tags = serializers.ListField(
        child=serializers.CharField()
    )


class VariantField(serializers.Field):

    def to_internal_value(self, data):
        data = json.loads(data)
        instance = getattr(self, 'instance', None)
        ser = VariantsSerializer(
            instance=instance,
            data=data,
            partial=bool(instance)
        )
        ser.is_valid(raise_exception=True)
        return ser.validated_data

    def to_representation(self, value):
        return VariantsSerializer(value).data


class PriceVariantSerializer(serializers.Serializer):
    title = serializers.CharField()
    price = serializers.FloatField()
    stock = serializers.IntegerField()


class PriceVariantField(serializers.Field):

    def to_internal_value(self, data):
        data = json.loads(data)
        instance = getattr(self, 'instance', None)
        ser = PriceVariantSerializer(
            instance=instance,
            data=data,
            partial=bool(instance)
        )
        ser.is_valid(raise_exception=True)
        return ser.validated_data

    def to_representation(self, value):
        return PriceVariantSerializer(value).data


class ProductSerializer(serializers.ModelSerializer):
    product_image = serializers.ListField(
        child=serializers.URLField(
        ), write_only=True, required=False
    )
    product_variant = serializers.ListField(
        child=VariantField(), write_only=True
    )
    product_variant_prices = serializers.ListField(
        child=PriceVariantField(), write_only=True
    )

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = (
            'id',
            'created_at',
            'updated_at'
        )

    def create(self, validated_data):
        images = validated_data.pop('product_image', [])
        variants = validated_data.pop('product_variant', [])
        variants_prices = validated_data.pop('product_variant_prices', [])
        # print(validated_data, flush=True)
        product = super(ProductSerializer, self).create(validated_data)
        for image in images:
            ProductImage.objects.create(
                product=product,
                file_path=image
            )
        for variant in variants:
            v_id = Variant.objects.get(id=variant['option'])
            for tag in variant['tags']:
                ProductVariant.objects.create(
                    product=product,
                    variant=v_id,
                    variant_title=tag
                )
        for variants_price in variants_prices:
            title = variants_price['title'][:-1]
            titles = title.split("/")
            print(titles, flush=True)
            pd = {}
            variant_list = ['product_variant_one', 'product_variant_two', 'product_variant_three']
            for index, value in enumerate(titles):
                id = ProductVariant.objects.get(
                   product=product,
                   variant_title=value
                )
                pd[variant_list[index]] = id
                print(index, pd, flush=True)

            print(pd, flush=True)
            ProductVariantPrice.objects.create(
                product=product,
                price=variants_price['price'],
                stock=variants_price['stock'],
                **pd
            )
        return product
        

class ProductVariantPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariantPrice
        fields = (
            'id',
            'product_variant_one',
            'product_variant_two',
            'product_variant_three',
            'price',
            'stock',
            'product'
        )