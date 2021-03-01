#define hist mapping

genericHistos=["Higgs_m","pTbalanceAll","LeadMuon_pt","LeadMuon_eta","SubMuon_pt","SubMuon_eta","QJet0_eta","QJet1_eta","QJet0_pt","QJet1_pt", "CS_theta", "CS_phi"]
bdtInputHistos=["Mqq_over400_log","Rpt","mmjj_pt","qqDeltaEta","NSoft5","ll_zstar","Higgs_pt","theta2","mmjj_pz","MaxJetAbsEta","Higgs_m_uncalib","NSoft5New","ll_zstar_log", "Higgs_mReso","QJet0_qgl","QJet1_qgl","Jet_jetId","Jet_puId"]


histosPerSelection={
#"PreSel" : ["Higgs_m"],
#"SignalRegionDNNWeighted" : ["Higgs_m"],
#"SRplusSBDNNWeighted" : ["Higgs_m","Higgs_m38"],
#"TightMassRegion" : ["DNN18AtanNoMass"],
"SignalRegion": ["MET_met", "QJet0_pt", "qq_pt", "qqDeltaEta", "qqDeltaPhi"]+genericHistos,
"InclusiveRegion": ["MET_met"],
"VBFRegion": ["MET_met"],
"MassWindowZ": ["MET_met"],
"PreSel": ["MET_met"],
#"SelectionTest1": ["MET_met"],
#"SelectionTest2": ["MET_met"],
#"SelectionTest3": ["MET_met"],
#"SelectionTest4": ["MET_met"],
#"SelectionTest5": ["MET_met"],
#"SelectionTest6": ["MET_met"],
#"SignalRegion": signalHistos+signalHistosVariations+signalHistosMassScan, #+bdtInputHistos+ genericHistos,
#"ZRegion": signalHistosVariations+balance,#+genericHistos +bdtInputHistos,
#"SideBand" : signalHistosVariations, #+ ["DNN18AtanMassSpread","DNN18AtanMassSpread2"],#+genericHistos+bdtInputHistos,
#"SignalRegionT": signalHistos+signalHistosVariations+signalHistosMassScan, #+bdtInputHistos+ genericHistos,
#"ZRegionT": signalHistosVariations+balance,#+genericHistos +bdtInputHistos,
#"SideBandT" : signalHistosVariations, #+ ["DNN18AtanMassSpread","DNN18AtanMassSpread2"],#+genericHistos+bdtInputHistos,
#"ZRegionSMP": signalHistosVariations+["pTbalanceAll"]+bdtInputHistos,
#"BDT1p1" : bdtInputHistos+genericHistos,
#"BDT1p2" : bdtInputHistos+genericHistos,
}

 
#manyZregions={
#"ZRegionSLJeta0pt0":signalHistosVariations+balance,
#"ZRegionSLJeta1pt0":signalHistosVariations+balance,
#"ZRegionSLJeta2pt0":signalHistosVariations+balance,
#"ZRegionSLJeta2pt1":signalHistosVariations+balance,
#"ZRegionSLJeta3pt0":signalHistosVariations+balance,
#"ZRegionSLJeta3pt1":signalHistosVariations+balance,
#}
#histosPerSelection.update(manyZregions)


#histosPerSelectionFullJecs={
#"SignalRegionDNNWeighted" : ["Higgs_m"],
#"SignalRegionDNNWeighted" : ["Higgs_m"],
#"SRplusSBDNNWeighted" : ["Higgs_m"],
#"SignalRegion":signalHistos+signalHistosMassScan,
#"SideBand":signalHistosVariations, #+["DNN18AtanMassSpread","DNN18AtanMassSpread2"],
#"ZRegion":signalHistosVariations+balance,
#"SignalRegionT":signalHistos+signalHistosMassScan,
#"SideBandT":signalHistosVariations, #+["DNN18AtanMassSpread","DNN18AtanMassSpread2"],
#"ZRegionT":signalHistosVariations+balance,
#"ZRegionSMP":["pTbalanceAll","DNN18AtanNoMass"],
#"SignalRegion":["BDTAtan","DNNAtan","DNN18Atan"],#,"DNN18AtanNoQGL"],
#"SideBand":["BDTAtanNoMass","DNNAtanNoMass","DNN18AtanNoMass"],
#"ZRegion":["BDTAtanNoMass","pTbalanceAll","DNNAtanNoMass","DNN18AtanNoMass"],
#ZRegionSMP":["BDTAtanNoMass","pTbalanceAll","DNNAtanNoMass"],
#}
#histosPerSelectionFullJecs.update(manyZregions)

#quick override for missing plots
if False:
#    histosPerSelectionFullJecs={
 # }
    histosPerSelection={
      "SignalRegion":      ["MET_pt"],
  }    
      #ericHistos+bdtInputHistos,
#      "SideBand":      ["Higgs_m_noGF","Mqq_over400_log","DNN18Atan"],#ericHistos+bdtInputHistos,
  #}

#'''
#genericHistos=["Higgs_m",]
  
