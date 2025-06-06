import ROOT
import numpy as np
import os
ROOT.gROOT.SetBatch(True)
dir_str = "syst_ratioplots/"
if not os.path.exists(dir_str):
    os.makedirs(dir_str)

pts = [['200','300'],['300','800']]
wps = ['0.637','0.845','0.910','0.642','0.842','0.907',
       '0.579','0.810','0.891','0.59','0.82','0.90']
wp_years = ['2016','2016','2016','2016','2016','2016',
            '2017','2017','2017','2018','2018','2018']
eras = [' pre VFP',' pre VFP',' pre VFP',' post VFP',' post VFP',' post VFP',
        '','','','','','']

sf_str = ['tp3','tp2','tp1','other']
systs = ['jes','pu','met','jer','jms','jmr']

c1 = ROOT.TCanvas("c1", "Canvas with 4 Quadrants", 1200, 1200)

title_pad = ROOT.TPad("title_pad", "title_pad", 0.0, 0.93, 1.0, 1.0)
title_pad.SetFillColor(0)
title_pad.SetBorderSize(0)
title_pad.SetMargin(0, 0, 0.1, 0.3)
title_pad.Draw()

# Define quadrant coordinates
quad_coords = [
    (0.0, 0.49, 0.5, 0.95),
    (0.5, 0.49, 1.0, 0.95),
    (0.0, 0.02, 0.5, 0.48),
    (0.5, 0.02, 1.0, 0.48)
]
ratio_hists_up = []
ratio_hists_down = []

# Create and draw the quadrants
pads = []
for i, coords in enumerate(quad_coords):
    quad_name = "quad_" + str(i)
    c1.cd()
    quad = ROOT.TPad(quad_name, "", *coords)
    quad.Draw()
    pads.append(quad)

# Create sub-pads for each quadrant
subpads = []
for i in range(4):
    pads[i].cd()
    top_name = "top_" + str(i)
    bot_name = "bot_" + str(i)
    pad_top = ROOT.TPad(top_name, "", 0.0, 0.31, 1.0, 1.0)
    pad_bot = ROOT.TPad(bot_name, "", 0.0, 0.0, 1.0, 0.3)
    pad_top.SetBottomMargin(0.1)
    pad_top.SetTopMargin(0.08)
    pad_top.SetLeftMargin(0.15)
    pad_bot.SetTopMargin(0)
    pad_bot.SetBottomMargin(0.3)
    pad_bot.SetLeftMargin(0.15)
    pad_top.Draw()
    pad_bot.Draw()
    subpads.append((pad_top, pad_bot))


def get_hists(f0,wp,year,ptbin,pf, sf, syst):
    nom_hist = f0.Get(sf)
    print("got nominal hist",nom_hist)
    nom_hist.Sumw2()
    if (syst == 'jms' or syst == 'jmr'):
        syst_str = sf+syst
    else: 
        syst_str = syst
    sys_up_h = f0.Get(sf+"_"+syst_str+"Up")
    sys_up_h.Sumw2()
    sys_down_h = f0.Get(sf+"_"+syst_str+"Down")
    sys_down_h.Sumw2()
    return nom_hist,sys_up_h,sys_down_h


def makeplots_4panel(c1,quadrant_pads, subpads, hist_sets, sf_list, syst, pf,plotdir,wp,era,year,pt1,pt2, title_pad):
    sf_names= ['Top-Merged','W-merged','Non-Merged','Other']
    ptbin = pt1+"to"+pt2
    for i in range(4):
        sf = sf_list[i]
        sfname = sf_names[i]
        hists = hist_sets[i]
       
        quadrant_pads[i].cd() 
        subpads[i][0].cd()
        
        # Main plot:
        hists[0].SetTitle(sfname)
        hists[0].GetYaxis().SetTitle("Events/Bin")
        hists[0].SetLineColor(ROOT.kBlack)
        hists[0].SetMarkerStyle(21)
        hists[0].Draw()
        

        hists[1].SetLineColor(ROOT.kRed)
        hists[1].SetMarkerStyle(21)
        hists[1].Draw("SAME")
        
        if (syst != 'jmr'):
            hists[2].SetLineColor(ROOT.kBlue)
            hists[2].SetMarkerStyle(21)
            hists[2].Draw("SAME")

        if (i==0):
            legend = ROOT.TLegend(0.2, 0.7, 0.5, 0.88)
            legend.AddEntry(hists[0], "Nominal", "l")
            legend.AddEntry(hists[1], syst + " Up", "l")
            if (syst != 'jmr'):
                legend.AddEntry(hists[2], syst + " Down", "l")
            legend.Draw()
        subpads[i][0].Update()

        # ratio plot 
        quadrant_pads[i].cd()
        subpads[i][1].cd()
        rat1 = hists[1].Clone("rat1_" + pf + "_" + str(i))
        rat1.Divide(hists[0])
        rat1.SetLineColor(ROOT.kRed)
        rat1.SetMarkerStyle(20)
        rat1.SetMarkerSize(0.6)
        rat1.SetMarkerStyle(20)
        rat1.SetMarkerSize(0.6)
        rat1.SetTitle("")
        rat1.GetYaxis().SetTitle("Ratio")
        rat1.GetYaxis().SetTitleSize(0.12)
        rat1.GetYaxis().SetTitleOffset(0.5)
        rat1.GetYaxis().SetLabelSize(0.10)
        rat1.GetYaxis().SetNdivisions(505)
        rat1.GetXaxis().SetTitle("m_{SD}(GeV)")
        rat1.GetXaxis().SetTitleSize(0.12)
        rat1.GetXaxis().SetLabelSize(0.10)
        ymin = max(0.01, rat1.GetMinimum(1e-5))  # Avoid zero, handle underflow
        ymax = min(2.0, rat1.GetMaximum())      # Optional: clamp to avoid wild spikes
        rat1.SetMinimum(0.8 * ymin)
        rat1.SetMaximum(1.2 * ymax)

        rat1.Draw("E")
        ratio_hists_up.append(rat1)
        
        if (syst != 'jmr'):
            rat2 = hists[2].Clone("rat2_"+str(i))
            rat2.Divide(hists[0])
            rat2.SetLineColor(ROOT.kBlue)
            rat2.SetMarkerStyle(21)
            rat2.SetMarkerSize(0.6)
            rat2.Draw("E SAME")
            ratio_hists_down.append(rat2)
        
        subpads[i][1].cd()
        subpads[i][1].Modified()
        subpads[i][1].Update()
        ROOT.gSystem.ProcessEvents()
        c1.Update()
    
    c1.cd()
    title_pad.cd()
    title_pad.Clear()
    title_latex = ROOT.TLatex()
    title_latex.SetNDC()
    title_latex.SetTextAlign(22)
    title_latex.SetTextFont(42)
    title_latex.SetTextSize(0.5)
    if (pf == 'p'):
        pf_str = 'Pass'
    elif (pf == 'f'):
        pf_str = 'Fail'
    title_latex.DrawLatex(0.5, 0.6, "{} {}, W -> cc score = {} ({}), pT [{}, {}]".format(year, era, wp, pf_str, pt1, pt2))
    title_pad.Update()
#    c1.Update()
    c1.SaveAs(plotdir+"/"+syst+"_"+pf+".png")


def run_plots(file_str,wp,year,pt1,pt2,era,pf,plotdir):
    ptbin = pt1+"to"+pt2
    f0 = ROOT.TFile.Open(file_str)
    for syst in systs:
        hist_sets = []
        open_files = []
        for sf in sf_str:
            print(year+" "+wp+" "+ptbin+" "+sf+" "+syst+" "+pf)
            hists= get_hists(f0,wp,year,ptbin,pf, sf, syst)
            open_files.append(f0)
            cloned=[]
            for h_i, h in enumerate(hists):
                newname = "{}_{}_{}_{}_{}_{}".format(sf, syst, pf, wp, year, h_i)
                cloned_hist = h.Clone(newname)
                cloned_hist.SetDirectory(0)
                cloned.append(cloned_hist)
            if len(cloned) == 3:
                hist_sets.append(cloned)
            else:
                print("skipping plot for sf={} due to missing hists.".format(sf))
        
        makeplots_4panel(c1, pads, subpads, hist_sets, sf_str, syst, pf, plotdir,wp,era,year,pt1,pt2,title_pad)
    f0.Close()


# Run all plots for all files:
for p in pts:
    pt1=p[0]
    pt2=p[1]
    ptbin = pt1+"to"+pt2
    for wp,yr,era in zip(wps,wp_years,eras):
        if ("pre" in era):
            eratag = "preVFP"
        elif ("post" in era):
            eratag = "postVFP"
        else:
            eratag=""
        p_plot_dir_str = dir_str+yr+"_"+eratag+"_"+wp+"_"+ptbin+"_p"
        f_plot_dir_str = dir_str+yr+"_"+eratag+"_"+wp+"_"+ptbin+"_f"
        if not os.path.exists(p_plot_dir_str):
            os.makedirs(p_plot_dir_str)
        if not os.path.exists(f_plot_dir_str):
            os.makedirs(f_plot_dir_str)
        p_str="particlenetmd_tt1l_w_{}to1.00_{}_pt{}_templates_p.root".format(wp,yr,ptbin)
        f_str="particlenetmd_tt1l_w_{}to1.00_{}_pt{}_templates_f.root".format(wp,yr,ptbin)
        run_plots(p_str,wp,yr,pt1,pt2,era,'p',p_plot_dir_str)
        run_plots(f_str,wp,yr,pt1,pt2,era,'f',f_plot_dir_str)
        
