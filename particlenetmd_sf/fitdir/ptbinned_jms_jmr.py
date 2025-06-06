import matplotlib
matplotlib.use('Agg')
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = (6, 4)
#ptbins = ['200to300','300to400','400to800']
ptbins = ['200to300','300to800']
wps = ['0.637','0.845','0.910','0.642','0.842','0.907',
       '0.579','0.810','0.891','0.59','0.82','0.90']
wp_years = ['2016','2016','2016','2016','2016','2016',
            '2017','2017','2017','2018','2018','2018']
eras = [' pre VFP',' pre VFP',' pre VFP',' post VFP',' post VFP',' post VFP',
        '','','','','','']
plot_idx = [yr + " " + wp + era for wp, yr, era in zip(wps, wp_years ,eras)]
#jet_merge = ['other','tp1','tp2','tp3']
jet_merge = ['tp2','tp3']
data_types = ['SF_down_err','SF','SF_up_err']
cols = pd.MultiIndex.from_product([plot_idx, jet_merge, data_types])
jms_df = pd.DataFrame(np.nan, index=range(2), columns=cols)
jmr_df = pd.DataFrame(np.nan, index=range(2), columns=cols)

for wp, yr, era in zip(wps, wp_years ,eras):
    plot_idx = yr + " " + wp + era
    print(plot_idx)
    names = jet_merge
    if ("pre" in era):
            eratag = "preVFP"
        elif ("post" in era):
            eratag = "postVFP"
        else:
            eratag=""
    for pt in range(len(ptbins)):
        ptbin = ptbins[pt]
        filestring=f"impacts_particlenetmd_tt1l_w_{wp}to1.00_{yr}_pt{ptbin}.json"
        print(filestring)
        with open(filestring, 'r') as f:
            obj=json.load(f)
            params_dict = {param["name"]: param["fit"]
                           for param in obj["params"]}
            for name in names:
                jmsname = name + 'jms'
                jmrname = name + 'jmr'
                print(jmsname)
                print (data_types)
                if (jmsname == 'tp3jms' and wp == '0.642' and pt == 0):
                    jms_df.at[pt,(plot_idx, name,data_types[0])] = 0
                    jms_df.at[pt,(plot_idx, name,data_types[1])] = 0
                    jms_df.at[pt,(plot_idx, name,data_types[2])] = 0

                else:
                    jms_df.at[pt,(plot_idx, name,data_types[0])] = np.abs(params_dict.get(jmsname)[1]-params_dict.get(jmsname)[0])
                    print( np.abs(params_dict.get(jmsname)[1]-params_dict.get(jmsname)[0]))
                    jms_df.at[pt,(plot_idx, name,data_types[1])] = params_dict.get(jmsname)[1]
                    jms_df.at[pt,(plot_idx, name,data_types[2])] = np.abs(params_dict.get(jmsname)[1]-params_dict.get(jmsname)[2])
                    jmr_df.at[pt,(plot_idx, name,data_types[1])] = params_dict.get(jmrname)[1]
                    jmr_df.at[pt,(plot_idx, name,data_types[0])] = np.abs(params_dict.get(jmrname)[1]-params_dict.get(jmrname)[0])
                    jmr_df.at[pt,(plot_idx, name,data_types[2])] = np.abs(params_dict.get(jmrname)[1]-params_dict.get(jmrname)[2])
            f.close()
    fig, ax = plt.subplots()
    ax.margins(x=0.1, y=0.1)
    plt.tight_layout()
    plt.grid(True)
#    tmp_x = [250,350,600]
    tmp_x = [250,550]
    #jettypes=['Other','Non-merged','W-merged','Top-merged']
    jettypes=['W-merged','Top-merged']
    for m,j in zip(jet_merge,jettypes):
        if(plot_idx == '2016 0.642 post VFP' and j == 'Top-merged'):
            ax.errorbar(tmp_x,jms_df[plot_idx][m]['SF'][1],xerr = [250], yerr = [jms_df[plot_idx][m]['SF_down_err'],jms_df[plot_idx][m]['SF_up_\
            err']],fmt='o', linestyle='none', capsize=5, label=j )
        else:
                ax.errorbar(tmp_x,jms_df[plot_idx][m]['SF'],xerr = [50,250], yerr = [jms_df[plot_idx][m]['SF_down_err'],jms_df[plot_idx][m]['SF_up_err']],fmt='o', linestyle='none', capsize=5, label=j )
    ax.legend(fontsize=10,markerscale=0.6,labelspacing=0.4,handlelength=1.25,handletextpad=0.4,borderpad=0.3,loc='best')
    plt.xticks([0,100,200,300,400,500,600,700,800,900,1000])
    plt.xlabel("pT")
    plt.ylabel("jms SF")
    plt.title("jms SF: "+plot_idx)
    if not os.path.exists("jms_sf_plots/"):
        os.makedirs("jms_sf_plots/")
    plt.savefig("jms_sf_plots/"+yr+"_"+eratag+"_"+wp+"_jms_sf.png",dpi=150,bbox_inches='tight')
    plt.close()

    fig, ax = plt.subplots()
    ax.margins(x=0.1, y=0.1)
    plt.tight_layout()
    plt.grid(True)
    #tmp_x = [250,350,600]
    for m,j in zip(jet_merge,jettypes):
        ax.errorbar(tmp_x,jmr_df[plot_idx][m]['SF'],xerr = [50,250], yerr = [jmr_df[plot_idx][m]['SF_down_err'],jmr_df[plot_idx][m]['SF_up_err']],fmt='o', linestyle='none', capsize=5, label=j )
    ax.legend(fontsize=10,markerscale=0.6,labelspacing=0.4,handlelength=1.25,handletextpad=0.4,borderpad=0.3,loc='best')
    plt.xticks([0,100,200,300,400,500,600,700,800,900,1000])
    plt.xlabel("pT")
    plt.ylabel("jmr SF")
    plt.title("jmr SF: "+plot_idx)
    if not os.path.exists("jmr_sf_plots/"):
        os.makedirs("jmr_sf_plots/")
    plt.savefig("jmr_sf_plots/"+yr+"_"+eratag+"_"+wp+"_jmr_sf.png",dpi=150,bbox_inches='tight')
    plt.close()



