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

def eval_binary_expr(op1, oper, op2) -> bool:
    op1, op2 = float(op1), float(op2)
    return ops[oper](op1, op2)

def check_against_criteria(series, optim_criterion) -> bool:
    return eval_binary_expr(*(f"{create_eval_phrase(series, optim_criterion)}".split()))

def optim_func(series):
    for optim_criterion in optim_criteria:
        if check_against_criteria(series, optim_criterion):
            return -1
    return series[final_field]

dispatcher = {} 
dispatcher['range'] = range
dispatcher['lambda param'] = lambda param: None

def call_func(func, *args, **kwargs):
    try:
        return dispatcher[func](*args, **kwargs)
    except:
        return "Invalid function"

def get_kwargs(qualname, module):
    k = conf.kwargs
    # value = tuple(int(num) for num in x["value"].replace('(', '').replace(')', '').replace('...', '').split(', '))
    # if dispatcher:
        # value = call_func(dispatcher, value)
    value = call_func("range", 10, 70, 5)
    k["n1"] = value
    k["n2"] = value
    k["maximize"] = optim_func
    a = "n1"
    b = "n2"
    oper = "<"
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

def create_eval_phrase(series, optim_criterion) -> str:
    field_name = optim_criterion["field_name"]
    op2 = optim_criterion["op2"]
    operator__ = optim_criterion["operator"]
    return f"{series[field_name]} {operator__} {op2}"

@configure_args
def opto(bt, **kwargs):
    return bt.optimize(**kwargs)

def determine_optimized_strategy_indicator_values(strat_name, bt) -> Backtest|None:
    constraint = get_constraint(strat_name)
    if constraint == None:
        return None
    return opto(bt)