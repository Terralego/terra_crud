from copy import deepcopy

from django.utils.functional import cached_property


class FormSchemaMixin:
    @cached_property
    def grouped_form_schema(self):
        original_schema = deepcopy(self.layer.schema)
        generated_schema = deepcopy(original_schema)
        groups = self.feature_display_groups.all()
        generated_schema['properties'] = {}

        for group in groups:
            # group properties by sub object, then add other properties
            generated_schema['properties'][group.slug] = group.form_schema
            for prop in group.group_properties.all():
                try:
                    generated_schema.get('required', []).remove(prop.key)
                except ValueError:
                    pass
        # add default other properties
        remained_properties = list(self.properties.filter(group__isnull=True).values_list('key', flat=True))
        for prop in remained_properties:
            generated_schema['properties'][prop] = original_schema['properties'][prop]

        return generated_schema

    @cached_property
    def grouped_ui_schema(self):
        """
        Original ui_schema is recomposed with grouped properties
        """
        ui_schema = deepcopy(self.ui_schema)

        groups = self.feature_display_groups.all()
        for group in groups:
            # each field defined in ui schema should be placed in group key
            ui_schema[group.slug] = {'ui:order': []}

            for prop in group.group_properties.all():
                # get original definition
                original_def = ui_schema.pop(prop.key, None)
                if original_def:
                    ui_schema[group.slug][prop.key] = original_def

                # if original prop in ui:order
                if prop.key in ui_schema.get('ui:order', []):
                    ui_schema.get('ui:order').remove(prop.key)
                    ui_schema[group.slug]['ui:order'] += [prop.key]
            # finish by adding '*' in all cases (security)
            ui_schema[group.slug]['ui:order'] += ['*']
        if groups:
            ui_schema['ui:order'] = list(groups.values_list('slug', flat=True)) + ['*']
        return ui_schema


def sync_layer_schema(crud_view):
    """ sync layer schema with properties defined by crud view properties """
    properties = crud_view.properties.all()
    crud_view.layer.schema = {"properties": {
        prop.key: prop.json_schema for prop in properties
    }, 'required': list(properties.filter(required=True).values_list('key', flat=True))}
    # required fields
    crud_view.layer.save()


def sync_ui_schema(crud_view):
    """ sync ui schema with properties defined by crud view properties """
    crud_view.ui_schema = {
        prop.key: prop.ui_schema
        for prop in crud_view.properties.exclude(ui_schema={})
    }
    crud_view.save()


def clean_properties_not_in_schema_or_null(crud_view):
    """ Clean properties not in layer schema to avoid schema validation """
    layer = crud_view.layer
    features = layer.features.all()
    if layer.schema:
        schema_properties = layer.schema.get('properties').keys()
        for feat in features:
            props_not_in_schema = feat.properties.keys() - schema_properties
            for prop in feat.properties.keys():
                if prop in props_not_in_schema or feat.properties.get(prop) is None:
                    feat.properties.pop(prop, 0)
            feat.save()
