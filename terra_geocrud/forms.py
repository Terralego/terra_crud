import tempfile

from django import forms
from django.contrib.gis.gdal import DataSource
from geostore.models import FeatureExtraGeom

from . import models


def parse_geometry_file(geom_file):
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.write(geom_file.read())
    temp.close()
    ds = DataSource(temp.name)

    if len(ds) == 0:
        return
    layer = ds[0]
    if len(layer) == 0:
        return
    geom = layer[0].geom.clone()
    geom.coord_dim = 2
    return geom.geos


class ExtraLayerStyleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # limit choices to available (linked by crud view / layer
            self.fields['layer_extra_geom'].queryset = self.instance.crud_view.layer.extra_geometries.all()

    class Meta:
        model = models.ExtraLayerStyle
        fields = "__all__"


class CrudPropertyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # limit choices to available (linked by crud view)
            self.fields['group'].queryset = self.instance.view.feature_display_groups.all()
            # unable to change property key after creation
            self.fields['key'].widget = forms.TextInput(attrs={'readonly': "readonly"})

    class Meta:
        model = models.CrudViewProperty
        fields = "__all__"


class CrudViewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # limit choices to available (linked by crud view)
            self.fields['default_list_properties'].queryset = self.instance.list_available_properties.all()
            self.fields['feature_title_property'].queryset = self.instance.list_available_properties.all()

    class Meta:
        model = models.CrudView
        fields = "__all__"


class FeatureExtraGeomForm(forms.ModelForm):
    geojson_file = forms.FileField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # limit choices to available (linked by crud view)
            self.fields['layer_extra_geom'].queryset = self.instance.feature.layer.extra_geometries.all()

    def save(self, commit=True):
        geometry_file = self.cleaned_data.get('geometry_file', None)

        if geometry_file:
            self.instance.geom = parse_geometry_file(geometry_file)
        return super().save(commit=commit)

    class Meta:
        model = FeatureExtraGeom
        fields = "__all__"
