from pprint import pprint
import operator
from backtesting import Backtest
from pandas import Series
from functools import wraps
from src.services.config_service.config import Configuration
from src.services.strategy_service.constraints import get_constraint
conf = Configuration.load_json('strategies_config.json')
optim_criteria = conf.optim_criteria
final_field = conf.optim_criteria_final_field
ops = {
    '+' : operator.add,
    '-' : operator.sub,
    '*' : operator.mul,
    '/' : operator.truediv,
    '%' : operator.mod,
    '^' : operator.xor,
    '<' : operator.lt,
    '>' : operator.gt,
}
dispatcher = {} 
dispatcher['range'] = range

def eval_binary_expr(op1, oper, op2) -> bool:
    op1, op2 = float(op1), float(op2)
    return ops[oper](op1, op2)

def create_eval_phrase(series, optim_criterion) -> str:
    field_name = optim_criterion["field_name"]
    op2 = optim_criterion["op2"]
    operator__ = optim_criterion["operator"]
    return f"{series[field_name]} {operator__} {op2}"

def check_against_criteria(series, optim_criterion) -> bool:
    return eval_binary_expr(*(f"{create_eval_phrase(series, optim_criterion)}".split()))

def optim_func(series):
    for optim_criterion in optim_criteria:
        if check_against_criteria(series, optim_criterion):
            return -1
    return series[final_field]

def call_func(func, *args, **kwargs):
    try:
        return dispatcher[func](*args, **kwargs)
    except:
        return "Invalid function"

def get_kwargs(qualname, module):
    conf_kwargs = conf.kwargs
    k = {}
    for p in conf_kwargs.params:
        if p.is_func:
            value = p.value
            value = tuple(int(num) for num in value.replace('(', '').replace(')', '').replace('...', '').split(', '))
            value = call_func(p.func, *value)
        k[p.name] = value
    k["maximize"] = optim_func
    a = conf_kwargs.constraint.op1
    b = conf_kwargs.constraint.op2
    oper = conf_kwargs.constraint.operator
    k["constraint"] = lambda param: {eval_binary_expr(*(f"{param[a]} {oper} {param[b]}".split()))}
    return k

def configure_args(f):
    qualname = f.__qualname__
    module = f.__module__
    default_kwargs = get_kwargs(qualname, module)
    @wraps(f)
    def wrapper(*args, **kwargs):
        new_kwargs = {**default_kwargs , **kwargs}
        return f(*args, **new_kwargs)
    return wrapper

@configure_args
def opto(bt, **kwargs):
    return bt.optimize(**kwargs)

def determine_optimized_strategy_indicator_values(strat_name, bt) -> Backtest|None:
    constraint = get_constraint(strat_name)
    if constraint == None:
        return None
    return opto(bt)