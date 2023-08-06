from .util import *
from .db import Database
from .optimizer import *
from .ops import Print, Yield
from .parseops import *
from .udfs import *
from .parse_sql import parse
from .tuples import *
from .tables import *
from .schema import Schema
from .exprs import Attr
from .compile import *
from .context import *


def sql2pandas(sql):
  opt = Optimizer()

  plan = Collect(opt(parse(sql).to_plan()))
  q = PandasCompiledQuery(plan)
  return q

