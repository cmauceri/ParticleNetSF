import os, argparse, json


parser=argparse.ArgumentParser(description="Extracting jms and jmr scale factors from ParticleNet output root file")

parser.add_argument("--wp", help = "Working Point: low_high",type=str,default = "0.82to1.00")

parser.add_argument("--tagger", help = "Tagger type", type=str,default="cc")

parser.add_argument("--year", help = "Run year", type=str,default = "2018")

parser.add_argument("--jettype", help = "jet type (width), ex: ak8",type=str, default = "ak8")

args = vars(parser.parse_args())

wp=args["wp"]
tagger=args["tagger"]
year=args["year"]
jettype=args["jettype"]

filestring = f"impacts_particlenetmd_tt1l_w_{wp}_{year}_pt200to800.json"
with open(filestring, 'r') as f:
    obj=json.load(f)

parameters = obj['params']
names=['tp3jms','tp2jms','tp1jms','otherjms','tp3jmr','tp2jmr','tp1jmr','otherjmr']

outfileStr=f"wp_{wp}_{tagger}_{year}_{jettype}_jms_jmr.txt"
txtout=open(outfileStr,"w")
for param in parameters:
    name = param['name']
    if name in names:
        txtout.write(f"{name}:")
        txtout.write("\n Central Value: ")
        txtout.write(f"{param['fit'][1]}")
        txtout.write("\n Lower Bound: ")
        txtout.write(f"{param['fit'][0]}")
        txtout.write("\n Upper Bound: ")
        txtout.write(f"{param['fit'][2]}")
        txtout.write("\n")

txtout.close()
