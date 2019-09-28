import json

from django.utils.translation import gettext_lazy as _
from pathlib import Path
from rest_framework import serializers
from rest_framework.reverse import reverse
from template_model.models import Template

from geostore.serializers import LayerSerializer, FeatureSerializer
from . import models


class LayerViewSerializer(LayerSerializer):
    schema = None
    layer_groups = None
    routing_url = None

    class Meta(LayerSerializer.Meta):
        fields = None
        exclude = ('schema',)


class CrudViewSerializer(serializers.ModelSerializer):
    layer = LayerViewSerializer()
    feature_endpoint = serializers.SerializerMethodField(
        help_text=_("Url endpoint for view's features")
    )
    feature_list_properties = serializers.SerializerMethodField(
        help_text=_("Available properties for feature datatable")
    )
    feature_list_default_properties = serializers.SerializerMethodField(
        help_text=_("Properties selected by default in datatable")
    )

    def get_feature_list_default_properties(self, obj):
        return obj.default_list_properties or obj.properties[:8]

    def get_feature_list_properties(self, obj):
        # TODO: override complete list with defined list
        return obj.properties

    def get_feature_endpoint(self, obj):
        return reverse('terra_geocrud:feature-list', args=(obj.layer_id,))

    class Meta:
        model = models.CrudView
        fields = (
            'id', 'name', 'pictogram', 'order', 'map_style',
            'form_schema', 'ui_schema', 'settings', 'layer',
            'feature_endpoint', 'feature_list_properties', 'feature_list_default_properties'
        )


class CrudGroupSerializer(serializers.ModelSerializer):
    crud_views = CrudViewSerializer(many=True, read_only=True)

    class Meta:
        model = models.CrudGroupView
        fields = '__all__'


class FeatureDisplayPropertyGroup(serializers.Serializer):
    title = serializers.CharField()
    order = serializers.IntegerField()
    pictogram = serializers.ImageField()
    properties = serializers.JSONField()


class CrudFeatureListSerializer(FeatureSerializer):
    detail_url = serializers.SerializerMethodField()
    extent = serializers.SerializerMethodField()

    def get_extent(self, obj):
        geom = obj.geom.transform(4326, clone=True)
        return geom.extent

    def get_detail_url(self, obj):
        return reverse('terra_geocrud:feature-detail', args=(obj.layer_id, obj.identifier))

    class Meta(FeatureSerializer.Meta):
        exclude = ('source', 'target', 'layer',)
        fields = None


class DocumentFeatureSerializer(serializers.ModelSerializer):
    extension = serializers.SerializerMethodField()
    template_name = serializers.CharField(source='name')
    template_file = serializers.SerializerMethodField()
    download_url = serializers.SerializerMethodField()

    def get_extension(self, obj):
        return Path(obj.template_file.name).suffix

    def get_template_file(self, obj):
        return Path(obj.template_file.name).name

    def get_download_url(self, obj):
        return reverse('terra_geocrud:render-template', args=(obj.pk,
                                                              self.context.get('feature').pk))

    class Meta:
        fields = ('extension', 'template_name', 'template_file', 'download_url')
        model = Template


class CrudFeatureDetailSerializer(FeatureSerializer):
    geom = serializers.SerializerMethodField()
    documents = serializers.SerializerMethodField()
    display_properties = serializers.SerializerMethodField()
    properties = serializers.SerializerMethodField()

    def get_geom(self, obj):
        geom = obj.geom.transform(4326, clone=True)
        return json.loads(geom.geojson)

    def get_properties(self, obj):
        results = {}
        crud_view = obj.layer.crud_view
        groups = crud_view.feature_display_groups.all()
        original_properties = obj.properties.copy()

        # get ordered groups filled
        for group in groups:
            results[group.slug] = {}
            for prop in group.properties:
                results[group.slug][prop] = original_properties.pop(prop, None)

        return {**results, **original_properties}

    def get_display_properties(self, obj):
        processed_properties = []
        results = {}
        crud_view = obj.layer.crud_view
        groups = crud_view.feature_display_groups.all()

        # get ordered groups filled
        for group in groups:
            serializer = FeatureDisplayPropertyGroup({
                "title": group.label,
                "pictogram": group.pictogram,
                "order": group.order,
                "properties": {
                    obj.layer.get_property_title(prop):
                        obj.properties.get(prop)
                    for prop in list(group.properties)
                }
            }, context={'request': self.context.get('request')})
            results[group.slug] = serializer.data
            processed_properties += list(group.properties)
        # add default other properties
        remained_properties = list(set(crud_view.properties) - set(processed_properties))
        if remained_properties:
            serializer = FeatureDisplayPropertyGroup({
                "title": "",
                "pictogram": None,
                "order": 9999,
                "properties": {
                    obj.layer.get_property_title(prop):
                        obj.properties.get(prop)
                    for prop in list(remained_properties)
                }
            })
            results['__default__'] = serializer.data
        return results

    def get_documents(self, obj):
        serializer = DocumentFeatureSerializer(obj.layer.crud_view.templates.all(),
                                               many=True,
                                               context={'request': self.context.get('request'),
                                                        'feature': obj})
        return serializer.data

    class Meta(FeatureSerializer.Meta):
        exclude = ('source', 'target', 'layer',)
        fields = None
