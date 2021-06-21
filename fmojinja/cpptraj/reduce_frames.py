from ..__version__ import get_version
from ..mixin import CpptrajMixin


class ReduceFrames(CpptrajMixin):
    template = f"# Generated by fmojinja version {get_version()}" + """
parm {{ parm }}
{%- for path in trajin %}
trajin {{ path }}
trajout {{ prefix ~ path.stem  }}.crd offset {{ offset }}
run
clear trajin{% endfor %}

"""

    @classmethod
    def set_arguments(self, p):
        super(ReduceFrames, self).set_arguments(p)
        p.add_argument("--offset", default=10)
        return p