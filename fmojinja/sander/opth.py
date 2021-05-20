from ..mixin import SubCommandMixin
from ..__version__ import get_version


class OptH(SubCommandMixin):
    """
    e.g. python -m fmojinja.sander.opth > $*.in; sander -O -i $*.in -o $*.mdout -r $*.rst_opt -p $*.parm -c $< -ref $<
    """

    template = f"# Generated by fmojinja version {get_version()}" + """ 
OptH
&cntrl
  imin=1, 
  maxcyc=100000, 
  ncyc=3000, 
  drms=0.1,
  ibelly=1
  bellymask='!@H='
  ig=-1,
  vlimit=-1,
  iwrap=1,
/

"""

    @classmethod
    def set_arguments(cls, p):
        return super(cls, cls).set_arguments(p)
