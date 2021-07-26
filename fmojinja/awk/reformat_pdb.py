from ..mixin import TemplateRendererMixin
from ..__version__ import get_version
from argparse import ArgumentParser


class ReformatPdb(TemplateRendererMixin):
    @classmethod
    def template(cls) -> str:
        return f"# Generated by fmojinja version {get_version()}" + """
function chain_tag(i, d) { d[1] = "A"; d[2] = "B"; d[3] = "C"; d[4] = "D"; d[5] = "E"; d[6] = "F"; return d[i] }
BEGIN { i = 1 }
# Left-justification
/^ATOM|^HETATM/ && substr($0, 18, 2) == "  " { $0 = substr($0, 0, 17) substr($0, 20, 1) "  "  substr($0, 21) }
/^ATOM|^HETATM/ && substr($0, 18, 1) == " " { $0 = substr($0, 0, 17) substr($0, 19, 2) " "  substr($0, 21) }
# Reformat chain names
{% for seq_id in chain_starts -%}
!start_{{ seq_id }} && int(substr($0, 23, 4)) == {{ seq_id }} { start_{{ seq_id }} = 1; i = i + 1 }
{% endfor %}
{ print substr($0, 0, 21) chain_tag(i) substr($0, 23) }
"""

    @classmethod
    def set_arguments(cls, p: ArgumentParser) -> ArgumentParser:
        p = super(ReformatPdb, cls).set_arguments(p)
        p.add_argument("-c", "--chain-starts", nargs="+")
        return p