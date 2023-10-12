from rest_framework import serializers


class BaseSerializer(serializers.ModelSerializer):
    def get_validated_data(self, **kwargs):
        validated_data = dict(list(self.validated_data.items()) + list(kwargs.items()))
        return validated_data

    def get_validators(self):
        validators = getattr(getattr(self, "Meta", None), "validators", [])
        return (
                self.get_unique_together_validators()
                + self.get_unique_for_date_validators()
                + validators
        )

    def get_extra_kwargs(self):
        extra_kwargs = super(BaseSerializer, self).get_extra_kwargs()
        write_only_fields = getattr(self.Meta, "write_only_fields", None)
        if write_only_fields is not None:
            if not isinstance(write_only_fields, (list, tuple)):
                raise TypeError(
                    "The `write_only_fields` option must be a list or tuple. "
                    "Got %s." % type(write_only_fields).__name__
                )
            for field_name in write_only_fields:
                kwargs = extra_kwargs.get(field_name, {})
                kwargs["write_only"] = True
                extra_kwargs[field_name] = kwargs

        return extra_kwargs
