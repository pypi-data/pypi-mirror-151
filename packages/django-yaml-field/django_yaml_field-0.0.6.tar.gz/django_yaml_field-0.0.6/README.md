# django-yaml-field
Same as Django JSONField but represent it as YAML (internally stores as JSON)

### Pip install

```bash
pip install django-yaml-field
```

### Example


```python

from django.db import models
from django_yaml_field import YAMLField


class ModelName(models.Model):
	yaml = YAMLField()
```

Allows querying 

https://docs.djangoproject.com/en/4.0/topics/db/queries/#querying-jsonfield


### Syntax Highlight

If you want a nice syntax highlight in form, you can use with [django-ace](https://github.com/django-ace/django-ace)

```python
from django_ace import AceWidget

@admin.register(ModelName)
class ModelName(admin.ModelAdmin):

	formfield_overrides = {YAMLField: {"widget": AceWidget(mode="yaml")}}
```

### License

MIT