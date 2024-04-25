from django.apps import apps
from extras.scripts import Script, StringVar, ChoiceVar


class FindRelatedFieldsScript(Script):
    class Meta:
        name = "Find Related Fields"
        description = "Find all possible related fields for a NetBox model"
        field_order = ["app_name", "model_name"]

    app_name = ChoiceVar(
        label="App Name",
        choices=sorted([(app.label, app.verbose_name) for app in apps.get_app_configs()]),
    )

    model_name = StringVar(
        label="Model Name", description="Name of the NetBox model to find related fields for"
    )

    def run(self, data, commit):
        app_label = data["app_name"]
        model_name = data["model_name"]
        model = apps.get_model(app_label, model_name)

        self.log_success(f"Model {model_name} in app {app_label} has the following related fields:")
        for field in model._meta.get_fields(include_hidden=True):
            if field.is_relation:
                self.log_success(f"- {field.name} (model: {field.related_model.__name__})")
