import os, argparse, json


parser=argparse.ArgumentParser(description="Extracting jms and jmr scale factors from ParticleNet output json file")

parser.add_argument("--wp", help = "Working Point: lowtohigh",type=str,default = "0.82to1.00")

parser.add_argument("--tagger", help = "Tagger type", type=str,default="cc")

parser.add_argument("--year", help = "Run year", type=str,default = "2018")

parser.add_argument("--jettype", help = "jet type (width), ex: ak8",type=str, default = "ak15")

args = vars(parser.parse_args())

wp=args["wp"]
tagger=args["tagger"]
year=args["year"]
jettype=args["jettype"]

filestring = f"impacts_particlenetmd_tt1l_w_{wp}_{year}_pt200to800.json"
with open(filestring, 'r') as f:
    obj=json.load(f)

outfileStr=f"wp_{wp}_{tagger}_{year}_{jettype}_jms_jmr.txt"
txtout=open(outfileStr,"w")
txtout.write(f"{year} {wp} {tagger} {jettype}")
txtout.write("\n")

params_dict = {param["name"]: param["fit"]
               for param in obj["params"]}
names = ['tp3','tp2','tp1','other']

for name in names:
    jmsname = name + 'jms'
    jmrname = name + 'jmr' 
    # write jms
    txtout.write(f"{jmsname}:")
    txtout.write("\n SF: ")
    txtout.write(f"{1+params_dict.get(jmsname)[1]}")
    txtout.write("\n Down Uncertainty: ")
    txtout.write(f"{params_dict.get(jmsname)[0]-params_dict.get(jmsname)[1]}")
    txtout.write("\n Up Uncertainty: ")
    txtout.write(f"{params_dict.get(jmsname)[2]-params_dict.get(jmsname)[1]}")
    txtout.write("\n")
    txtout.write("\n")
    # write jmr
    txtout.write(f"{jmrname}:")
    txtout.write("\n SF: ")
    txtout.write(f"{1+params_dict.get(jmrname)[1]}")
    txtout.write("\n Down Uncertainty: ")
    txtout.write(f"{params_dict.get(jmrname)[0]-params_dict.get(jmrname)[1]}")
    txtout.write("\n Up Uncertainty: ")
    txtout.write(f"{params_dict.get(jmrname)[2]-params_dict.get(jmrname)[1]}")
    txtout.write("\n")
    txtout.write("\n")
    

txtout.close()
