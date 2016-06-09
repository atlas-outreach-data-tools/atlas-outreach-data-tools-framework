config = {
"Luminosity": 1000,
"InputDirectory": "results",

"Histograms" : {
    "invMass1"        : {"rebin" : 3},
    "invMass2"        : {"rebin" : 3},
    "lep_n"           : {"y_margin" : 0.4},
    "lep_pt"          : {"y_margin" : 0.4, "rebin" : 4},
    "lep_eta"         : {"y_margin" : 0.5, "rebin" : 3},
    "lep_E"           : {"rebin" : 3},
    "lep_phi"         : {"y_margin" : 0.6, "rebin" : 4,},
    "lep_charge"      : {"y_margin" : 0.6},
    "lep_type"        : {"y_margin" : 0.5,},
    "lep_ptconerel30" : {"y_margin" : 0.3, "rebin" : 4},
    "lep_etconerel20" : {"y_margin" : 0.3, "rebin" : 4},
    "lep_d0"          : {"y_margin" : 0.5, "rebin" : 2}, 
    "lep_z0"          : {"y_margin" : 0.5, "rebin" : 2}, 
    "vxp_z"           : {"y_margin" : 0.5, "rebin" : 4},
    "pvxp_n"          : {"y_margin" : 0.5, "rebin" : 3},
},

"Paintables": {
    "Stack": {
        "Order": ["ZZ", "Diboson", "DrellYan", "W", "stop", "ttbar"],
        "Processes" : {                
            "ZZ" : {
                "Color"         : "#fa7921",
                "Contributions" : ["ZZ"]},

            "Diboson" : {
                "Color"         : "#086788",
                "Contributions" : ["WW", "WZ"]},
                                
            "DrellYan": {       
                "Color"         : "#5bc0eb",
                "Contributions" : ["DYeeM08to15", "DYeeM15to40", "DYmumuM08to15", "DYmumuM15to40", "DYtautauM08to15", "DYtautauM15to40", "Zee", "Zmumu", "Ztautau"]},
            
            "W": {              
                "Color"         : "#e55934",
                "Contributions" : ["WenuJetsBVeto", "WenuWithB", "WenuNoJetsBVeto", "WmunuJetsBVeto", "WmunuWithB", "WmunuNoJetsBVeto", "WtaunuJetsBVeto", "WtaunuWithB", "WtaunuNoJetsBVeto"]},
                  
            "stop": {
                "Color"         : "#fde74c",
                "Contributions" : ["stop_tchan_top", "stop_tchan_antitop", "stop_schan", "stop_wtchan"]},
            
            "ttbar": {
                "Color"         : "#9bc53d",
                "Contributions" : ["ttbar_lep", "ttbar_had"]}
        }
    },

    "data" : {
        "Contributions": ["data_Egamma", "data_Muons"]}
},

"Depictions": {
    "Order": ["Main", "Data/MC"],
    "Definitions" : {
        "Data/MC": {
            "type"       : "Agreement",
            "Paintables" : ["data", "Stack"]
        },
        
        "Main": {
            "type"      : "Main",
            "Paintables": ["Stack", "data"]
        },
    }
},
}