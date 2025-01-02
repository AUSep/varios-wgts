d1={'gat':56,'hy':543,'hdak':64}
d2={'gat':345,'hy':5165,'hdak':5}
d3={'gat':5245,'hy':89,'hdak':6}
d_tupl=(d1,d2,d3)
def get_gat(*d_tupl:dict) -> None:
    gat = [d['gat'] for d in d_tupl]
    return gat

print(get_gat(d1,d2,d3))