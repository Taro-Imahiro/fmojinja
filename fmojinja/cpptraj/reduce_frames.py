from ..__version__ import get_version
from ..mixin import CpptrajMixin


class ReduceFrames(CpptrajMixin):

    @classmethod
    def template(cls) -> str:
        return f"# Generated by fmojinja version {get_version()}" + """
parm {{ parm }}
{%- for path in trajin %}
trajin {{ path }} {{ offset }} last {{ offset }}
trajout {{ prefix ~ path.stem  }}.crd 
run
clear trajin{% endfor %}

"""

    @classmethod
    def set_arguments(self, p):
        super(ReduceFrames, self).set_arguments(p)
        p.add_argument("-P", "--prefix", default="reduced/")
        p.add_argument("--offset", default=10)
        return p