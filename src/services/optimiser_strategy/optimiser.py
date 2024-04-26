def optimise(bt, factor):
    if factor == "return":
        f='Return [%]'
    optim = bt.optimze(
        n1=range(50,160,10),
        n1=range(50,160,10),
        constraint=lambda x: x.n2 - x.n1 > 20,
        maximize=f
    )
    return optim