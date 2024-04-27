from pprint import pprint
import operator
from backtesting import Backtest
from pandas import Series
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

def create_eval_phrase(series, optim_criterion) -> str:
    field_name = optim_criterion["field_name"]
    op2 = optim_criterion["op2"]
    operator__ = optim_criterion["operator"]
    return f"{series[field_name]} {operator__} {op2}"

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

def determine_optimized_strategy_indicator_values(strat_name, bt) -> Backtest|None:
    constraint = get_constraint(strat_name)
    if constraint == None:
        return None
    return bt.optimize(
        n1=range(5, 30, 5),
        n2=range(10, 70, 5),
        maximize=optim_func,
        constraint=constraint
    )