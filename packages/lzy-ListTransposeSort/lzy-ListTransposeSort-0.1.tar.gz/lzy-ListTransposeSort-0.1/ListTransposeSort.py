def ListTransposeSort(*args,T = True,v=0,reverse=False):
    if T:
        return list(map(list, zip(*args)))
    else:
        return sorted(args, key=lambda kv: kv[v],reverse=reverse)