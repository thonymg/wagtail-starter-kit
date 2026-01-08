from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from django.db.models import Model, QuerySet
from django.forms.models import model_to_dict
import pprint
import json

register = template.Library()

@register.filter
def pprint_context(value):
    """Pretty print context with clean formatting"""
    if not settings.DEBUG:
        return ""

    try:
        data = _extract_data(value)
        formatted = pprint.pformat(data, indent=2, width=80, depth=4)
        return mark_safe(formatted)
    except Exception as e:
        return f"Debug Error: {str(e)}"

@register.filter
def json_context(value):
    """JSON format for context"""
    if not settings.DEBUG:
        return ""

    try:
        data = _extract_data(value)
        formatted = json.dumps(data, indent=2, ensure_ascii=False, default=str)
        return mark_safe(formatted)
    except Exception as e:
        return f"JSON Error: {str(e)}"

@register.filter
def context_keys(value):
    """Show available keys only"""
    if not settings.DEBUG:
        return ""

    try:
        if hasattr(value, '__dict__'):
            keys = [k for k in value.__dict__.keys() if not k.startswith('_')]
        elif hasattr(value, '_meta'):
            keys = [field.name for field in value._meta.fields]
        else:
            keys = list(value.keys()) if hasattr(value, 'keys') else []

        return mark_safe('\n'.join(sorted(keys)))
    except Exception as e:
        return f"Keys Error: {str(e)}"

def _extract_data(value):
    if isinstance(value, QuerySet):
        return [ _extract_data(obj) for obj in value ]
    if isinstance(value, Model):
        try:
            return model_to_dict(value)
        except Exception:
            data = {}
            for field in value._meta.fields:
                try:
                    data[field.name] = getattr(value, field.name)
                except Exception:
                    data[field.name] = 'ERROR'
            return data
    if isinstance(value, (list, tuple, set)):
        return list(value)
    if isinstance(value, dict):
        return value
    if hasattr(value, '__dict__'):
        return {k: v for k, v in value.__dict__.items() if not k.startswith('_')}
    return value

# <!-- Debug basique -->
# <pre class="debug-pre">{{ page|pprint_context }}</pre>

# <!-- Avec panel élégant -->
# <div class="debug-panel">
#     <div class="debug-header">Context Debug</div>
#     <div class="debug-content">
#         {{ page|pprint_context }}
#     </div>
# </div>

# <!-- Clés disponibles -->
# <pre class="debug-keys">{{ page|context_keys }}</pre>

# <!-- Format JSON -->
# <pre class="debug-json">{{ page|json_context }}</pre>
