from ...mixin import TemplateRendererMixin
from ...__version__ import get_version
from argparse import ArgumentParser
from pathlib import Path


class SnapMin(TemplateRendererMixin):
    """
    for snapshots minimization
    """
    @classmethod
    def template(cls) -> str:
        return f"# Generated by fmojinja version {get_version()}" + """
MD_ENGINE = sander # e.g. sander, pmemd, pmemd.cuda, mpi -n 8 pmemd.MPI
PREFIX := {{ prefix }}
PRMTOP := {{ prmtop }}
TRAJIN :={% for path in trajin %} {{ path }}{% endfor %}
RESTRT := $(addsuffix .restrt, $(addprefix $(PREFIX), $(basename $(notdir $(TRAJIN)))))


.PHONY: gen
gen: $(PREFIX) $(PREFIX)mdin

$(PREFIX)mdin:
\tpython -m fmojinja.sander min \\
\t-rm "{{ restraint_mask if restraint_mask else "" }}" \\
\t-rw {{ restraint_wt }} \\
\t-drms {{ drms }} \\
\t-mc {{ maxcyc }} \\
\t-cut {{ cut_off }} \\
\t-ig {{ seed }} > $@

$(PREFIX):
\tmkdir $(PREFIX)

.PHONY: run
run: gen $(PREFIX)prmtop $(RESTRT)

$(PREFIX)prmtop:
\tcp $(PRMTOP) $@

define expr
$(PREFIX)$(basename $(notdir $(1))).restrt: $(1)
\t$(MD_ENGINE) -O \\
\t-i $(PREFIX)mdin \\
\t-o $(PREFIX)$(basename $(notdir $(1))).mdout \\
\t-p $(PREFIX)prmtop \\
\t-c $(1) \\
\t-ref $(1) \\
\t-r $(PREFIX)$(basename $(notdir $(1))).restrt
endef
$(foreach i, $(TRAJIN), $(eval $(call expr, $(i))))


.PHONY: clean
clean:
\trm $(PREFIX)* 


"""

    @classmethod
    def set_arguments(cls, p: ArgumentParser) -> ArgumentParser:
        p = super(SnapMin, cls).set_arguments(p)
        p.add_argument("-P", "--prefix", default="snapmin/")
        p.add_argument("-p", "--prmtop", type=Path, required=True)
        p.add_argument("-y", "--trajin", type=Path, nargs="+", required=True)
        p.add_argument("-rm", "--restraint-mask", help="restraint mask. e.g. '!@H=' ")
        p.add_argument("-rw", "--restraint-wt", default=10, help="the weight (kcal/mol angstrom)")
        p.add_argument("-mc", "--maxcyc", default=10000)
        p.add_argument("-drms", default=1e-4)
        p.add_argument("-cut", "--cut-off",default=12.0)
        p.add_argument("-ig", "--seed", default=-1)
        return p
