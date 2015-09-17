{{ node.name }}
{{ '=' * node.name|length }}

::

    {{ node.tree() }}


.. automodule:: {{ node.name }}
   :show-inheritance:

   .. contents::
      :local:
{##}
{%- block modules -%}
{%- if node.subnodes %}

Modules
-------

.. autosummary::
{% for item in node.subnodes %}
   {{ item.name }}
{%- endfor %}
{##}
{%- endif -%}
{%- endblock -%}
{##}
.. currentmodule:: {{ node.name }}
{##}
{%- block functions -%}
{%- if node.functions %}

Functions
---------

.. autosummary::
{% for item in node.functions %}
   {{ item }}
{%- endfor %}

{% for item in node.functions %}
.. autofunction:: {{ item }}
{##}
{%- endfor -%}
{%- endif -%}
{%- endblock -%}

{%- block classes -%}
{%- if node.classes %}

Classes
-------

.. autosummary::
{% for item in node.classes %}
   {{ item }}
{%- endfor %}

{% for item in node.classes %}
.. autoclass:: {{ item }}
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: {{ item }}
{##}
{%- endfor -%}
{%- endif -%}
{%- endblock -%}

{%- block exceptions -%}
{%- if node.exceptions %}

Exceptions
----------

.. autosummary::
{% for item in node.exceptions %}
   {{ item }}
{%- endfor %}

{% for item in node.exceptions %}
.. autoexception:: {{ item }}

   .. rubric:: Inheritance
   .. inheritance-diagram:: {{ item }}
{##}
{%- endfor -%}
{%- endif -%}
{%- endblock -%}
