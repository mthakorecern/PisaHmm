from nail.nail import *
import ROOT
import sys

def getFlow(year):
    FSR=True
    FSRnew=False
    FSRnew=True
    #flow=SampleProcessing("VBF Hmumu Analysis","/scratch/arizzi/Hmm/nail/samples/6B8A2AC8-35E6-1146-B8A8-B1BA90E3F3AA.root"
    flow=SampleProcessing("VBF Hmumu Analysis","/scratchssd/thakore/PROD_2_0/vbfHmm_powheg_merged.root")
    
#    ##FIXME## SD
    #variables that we will add file by file before passing the RNode to the event processor
    
    flow.AddExpectedInput("year","int")
    flow.AddExpectedInput("TriggerSel","bool")
    
    #Higgs to mumu reconstruction
    #flow.DefaultConfig(muIsoCut=0.25,muIdCut=2,muPtCut=20, dzCut=1e99,dxyCut=1e99) #cuts value should not be hardcoded below but rather being declared here so that scans and optimizations are possible
    flow.Define("Muon_mass","0.f*Muon_pt")
    flow.Define("Muon_iso","Muon_isolationvarrhocorr") ## Delphes variables: Muon_sumptneutral, Muon_sumpt, Muon_sumptchargedpu, Muon_sumptcharged, Muon_isolationvarrhocorr, Muon_isolationvar. No Muon ID variables available!
    flow.Define("Muon_p4","vector_map_t<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> >        >(Muon_pt , Muon_eta, Muon_phi, Muon_mass)")
    
    ##Jet Selection. FIXME: Missing Muon ID, Muon Isolation
    flow.SubCollection("SelectedMuon","Muon",sel="abs(Muon_eta) < 2.4") ### I've put a simple selection as example
    
    flow.Selection("twoUnpreselMuons","nMuon>=2")
    flow.Selection("twoMuons","nSelectedMuon==2")
    
    ## Get the pair of opposite side muons, 
    flow.Distinct("MuMu","SelectedMuon")
    flow.Define("OppositeSignMuMu","Nonzero(MuMu0_charge != MuMu1_charge)",requires=["twoMuons"])
    flow.Selection("twoOppositeSignMuons","OppositeSignMuMu.size() > 0")
    flow.TakePair("Mu","SelectedMuon","MuMu","At(OppositeSignMuMu,0,-200)",requires=["twoOppositeSignMuons"])
    flow.Define("Higgs","Mu0_p4+Mu1_p4")
    
    flow.Define("Jet_p4","vector_map_t<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> >        >(Jet_pt , Jet_eta, Jet_phi, Jet_mass)")
    
    #VBF Jets kinematics
    flow.DefaultConfig(jetPtCut=25)
    
    ##Jet Selection. FIXME: Missing Jet ID, JetPU ID
    flow.SubCollection("SelectedJet","Jet",'''
    Jet_pt > jetPtCut && abs(Jet_eta) < 4.7
    ''')
    
    flow.Selection("twoJets","nSelectedJet>=2")
    
    flow.Distinct("JetPair","SelectedJet")
    flow.Define("SortedSelectedJetIndices","Argsort(-SelectedJet_pt)")
    flow.ObjectAt("QJet0","SelectedJet",'At(SortedSelectedJetIndices,0)',requires=["twoJets"])
    flow.ObjectAt("QJet1","SelectedJet",'At(SortedSelectedJetIndices,1)',requires=["twoJets"])

    #compute number of softjets removing signal footprint
    flow.Define("SoftActivityJet_mass","SoftActivityJet_pt*0")
    flow.Define("SoftActivityJet_p4","@p4v(SoftActivityJet)")
    flow.Match("SelectedJet","SoftActivityJet") #associate signal jets
    flow.Match("SelectedMuon","SoftActivityJet") #associate signal muons
    
    flow.Define("qq","QJet0_p4+QJet1_p4")
    flow.Define("Mqq","qq.M()")
    flow.Define("qq_pt","qq.Pt()")
    flow.Define("qqDeltaEta","abs(QJet0_eta-QJet1_eta)")
    flow.Define("qqDeltaPhi","abs(ROOT::Math::VectorUtil::DeltaPhi(QJet0_p4,QJet1_p4))")

    #QQ vs ll kinematic
    flow.Define("ll_ystar","Higgs.Rapidity() - (QJet0_p4.Rapidity() + QJet1_p4.Rapidity())/2.f")
    flow.Define("ll_zstar"," abs( ll_ystar/ (QJet0_p4.Rapidity()-QJet1_p4.Rapidity() )) ")
    flow.Define("ll_zstar_log"," log(ll_zstar) ")
    flow.Define("ll_zstarbug_log","log(abs( (  Higgs.Rapidity() - (QJet0_p4.Rapidity() + QJet1_p4.Rapidity())  )/ (QJet0_p4.Rapidity()-QJet1_p4.Rapidity() )))")
    flow.Define("DeltaEtaQQSum","abs(QJet0_eta) +  abs(QJet1_eta)")
    flow.Define("PhiHQ1","abs(ROOT::Math::VectorUtil::DeltaPhi(Higgs,QJet0_p4))")
    flow.Define("PhiHQ2","abs(ROOT::Math::VectorUtil::DeltaPhi(Higgs,QJet1_p4))")
    flow.Define("EtaHQ1","abs(Higgs.Eta() - QJet0_eta)")
    flow.Define("EtaHQ2","abs(Higgs.Eta() - QJet1_eta)")
    flow.Define("DeltaRelQQ","(QJet0_p4+QJet1_p4).Pt()/( QJet0_p4.Pt()+QJet1_p4.Pt())")
    flow.Define("Rpt","(QJet0_p4+QJet1_p4+ Higgs).Pt()/( QJet0_p4.Pt()+QJet1_p4.Pt() + Higgs.Pt())")
    #flow.Define("mmjj","Higgs+qq")
    flow.Define("theta2","Higgs.Vect().Dot(QJet1_p4.Vect())/QJet1_p4.Vect().R()/Higgs.Vect().R()")
    flow.ObjectAt("LeadMuon","SelectedMuon","0",requires=["twoMuons"])
    flow.ObjectAt("SubMuon","SelectedMuon","1",requires=["twoMuons"])
    flow.Define("Higgs_pt","Higgs.Pt()")
    flow.Define("Higgs_rapidity","Higgs.Rapidity()")

    flow.Define("pTbalanceLead","QJet0_pt/Higgs_pt")
    #flow.Define("pTbalance","qq.Pt()/Higgs_pt")
    flow.Define("pTbalanceAll","SumDef(SelectedJet_p4).pt()/Higgs_pt")
    flow.Define("pTbalanceAllLog","log(pTbalanceAll)")
    flow.Define("pTbalanceLog","log(pTbalance)")
    flow.Define("pTbalanceLeadLog","log(pTbalanceLead)")
    flow.Define("Higgs_m","Higgs.M()")
    flow.Define("Higgs_eta","Higgs.Eta()")
    flow.Define("Higgs_m_uncalib","HiggsUncalib.M()")
    flow.Define("Mqq_log","log(Mqq)")
    flow.Define("Mqq_over400_log","log(Mqq/400)")
    flow.Define("mmjj_pt","mmjj.Pt()")
    flow.Define("mmjj_pt_log","log(mmjj_pt)")
    flow.Define("mmjj_pz","mmjj.Pz()")
    flow.Define("mmjj_pz_logabs","log(abs(mmjj_pz))")
    flow.Define("MaxJetAbsEta","std::max(std::abs(QJet0_eta), std::abs(QJet1_eta))")
    flow.Define("minEtaHQ","std::min(abs(EtaHQ1),(EtaHQ2))")
    flow.Define("minPhiHQ","std::min(abs(PhiHQ1),abs(PhiHQ2))")


    flow.AddCppCode('\n#include "boost_to_CS.h"\n')
    flow.Define("CS_theta","boost_to_CS(LeadMuon_p4, SubMuon_p4,  SubMuon_charge).first",requires=["twoOppositeSignMuons"])
    flow.Define("CS_phi","boost_to_CS(LeadMuon_p4, SubMuon_p4, SubMuon_charge).second",requires=["twoOppositeSignMuons"])

    flow.DefaultConfig(higgsMassWindowWidth=10,mQQcut=400,nominalHMass=125.03) #,btagCut=0.8)
    ## no b-tag discriminant in delphes, just 0 or 1
    flow.Define("SelectedJet_btagDeepB","0") ##FIXME: use actual b-tagging
    flow.Define("btagCut","0.5")
    flow.Define("btagCutL","0.5")
    #adding for sync
    flow.Define("nbtagged","int(Nonzero(SelectedJet_btagDeepB > btagCut && abs(SelectedJet_eta)< 2.5).size())")
    flow.Define("nbtaggedL","int(Nonzero(SelectedJet_btagDeepB > btagCutL && abs(SelectedJet_eta)< 2.5).size())")
    flow.Define("nelectrons","int(Nonzero(Electron_pt > 20 && abs(Electron_eta) < 2.5 ).size())")


    #flow.Selection("MassWindow","Higgs.M()")
    flow.Selection("MassWindowZ","abs(Higgs.M()-91)<15")
    flow.Selection("VBFRegion","Mqq > mQQcut && QJet0_pt> 35 && QJet1_pt > 25")
    flow.Selection("PreSel","nelectrons==0 && nbtaggedL < 2 && VBFRegion && twoOppositeSignMuons && nbtagged < 1 && (( year == 2016 && LeadMuon_pt > 26 ) || ( year == 2017 && LeadMuon_pt > 29 ) || ( (year == 2018||year==2026) && LeadMuon_pt > 26 )) && SubMuon_pt > 20 && TriggerSel && abs(SubMuon_eta) <2.4 && abs(LeadMuon_eta) < 2.4",requires=["VBFRegion","twoOppositeSignMuons"])
    #flow.Selection("SideBand","Higgs_m < 150 && Higgs_m > 110 && ! MassWindow && VBFRegion &&  qqDeltaEta > 2.5",requires=["VBFRegion","PreSel"])
    flow.Selection("SignalRegion","VBFRegion &&  (1 || qqDeltaEta > 2.5)", requires=["VBFRegion","PreSel"]) ##FIXME qqDeltaEta > 2.5
    flow.Selection("InclusiveRegion","1")    #flow.Selection("ZRegion","VBFRegion && MassWindowZ  && qqDeltaEta > 2.5", requires=["VBFRegion","MassWindowZ","PreSel"])
#    flow.Selection("SelectionTest1","VBFRegion &&  qqDeltaEta > 2.5", requires=["VBFRegion","PreSel"])
#    flow.Selection("SelectionTest2","VBFRegion ", requires=["VBFRegion","PreSel"])
#    flow.Selection("SelectionTest3","qqDeltaEta > 2.5", requires=["VBFRegion","PreSel"])
#    flow.Selection("SelectionTest4","1", requires=["VBFRegion","PreSel"])
#    flow.Selection("SelectionTest5","VBFRegion &&  qqDeltaEta > 2.5")
#    flow.Selection("SelectionTest6","qqDeltaEta > 2.5", requires=["PreSel"])

    #flow.Selection("ZRegionSMP","Mqq > 250 && MassWindowZ && QJet0_pt> 50 && QJet1_pt > 30 && twoOppositeSignMuons && twoJets && TriggerSel&& abs(SubMuon_eta) <2.4 && abs(LeadMuon_eta) < 2.4 ", requires=["twoOppositeSignMuons","twoJets"])
    flow.Selection("TwoJetsTwoMu","twoJets && twoOppositeSignMuons", requires=["twoJets","twoOppositeSignMuons"])
    #flow.Selection("SignalRegionT","SignalRegion && QJet0_pt>45 && QJet1_pt > 27",requires=["SignalRegion"])
    flow.Selection("ZRegionT","ZRegion && QJet0_pt>45 && QJet1_pt > 27",requires=["ZRegion"])
    flow.Selection("SideBandT","SideBand && QJet0_pt>45 && QJet1_pt > 27",requires=["SideBand"])
        #with bug

    return flow
