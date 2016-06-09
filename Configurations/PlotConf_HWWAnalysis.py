config = {
'InputDirectory': 'results',
'Luminosity': 1000,

'Histograms': {
    'leadlep_E'             : {"rebin" : 2, "y_margin" : 0.3},
    'leadlep_charge'        : {"y_margin" : 0.7},
    'leadlep_eta'           : {"rebin" : 3, "y_margin" : 0.6},
    'leadlep_phi'           : {"rebin" : 4, "y_margin" : 0.6},
    'leadlep_pt'            : {},
    'leadlep_etconerel20'   : {"rebin" : 2, "y_margin" : 0.3},
    'leadlep_ptconerel30'   : {"rebin" : 2, "y_margin" : 0.3},
    'leadlep_type'          : {"y_margin" : 0.5},
    'leadlep_d0'            : {"y_margin" : 0.3},
    'leadlep_z0'            : {"y_margin" : 0.3},
    'traillep_E'            : {"rebin" : 2, "y_margin" : 0.3},
    'traillep_charge'       : {"y_margin" : 0.7},
    'traillep_eta'          : {"rebin" : 3, "y_margin" : 0.6},
    'traillep_phi'          : {"rebin" : 4, "y_margin" : 0.6},
    'traillep_pt'           : {},
    'traillep_etconerel20'  : {},
    'traillep_ptconerel30'  : {},
    'traillep_type'         : {},
    'traillep_d0'           : {},
    'traillep_z0'           : {},
    'vismass'               : {"rebin" : 2, "y_margin" : 0.3},
    'ptll'                  : {"rebin" : 2, "y_margin" : 0.3},
    'deltaphill'            : {"rebin" : 2},
    'etmiss'                : {"rebin" : 2, "y_margin" : 0.3},
    'pvxp_n'                : {"rebin" : 2, "y_margin" : 0.3},
    'vxp_z'                 : {"rebin" : 4, "y_margin" : 0.3},
},

'Paintables': {
    'Stack': {
        "Order"     : ["Diboson", "DrellYan", "W", "Z", "stop", "ttbar"],
        "Processes" : {
            'Diboson': {
                'Color'         : '#fa7921',
                'Contributions' : ['WW', 'WZ', 'ZZ']},
                                
            'DrellYan': {       
                'Color'         : '#5bc0eb',
                'Contributions' : ['DYeeM08to15', 'DYeeM15to40', 'DYmumuM08to15', 'DYmumuM15to40', 'DYtautauM08to15', 'DYtautauM15to40']},
            
            'W': {              
                'Color'         : '#e55934',
                'Contributions' : ['WenuJetsBVeto', 'WenuWithB', 'WenuNoJetsBVeto', 'WmunuJetsBVeto', 'WmunuWithB', 'WmunuNoJetsBVeto', 'WtaunuJetsBVeto', 'WtaunuWithB', 'WtaunuNoJetsBVeto']},
                                
            'Z': {              
                'Color'         : '#086788',
                'Contributions' : ['Zee', 'Zmumu', 'Ztautau']},
                  
            'stop': {
                'Color'         : '#fde74c',
                'Contributions' : ['stop_tchan_top', 'stop_tchan_antitop', 'stop_schan', 'stop_wtchan']},
            
            'ttbar': {
                'Color'         : '#9bc53d',
                'Contributions' : ['ttbar_lep', 'ttbar_had']}
            }
    },
                    
    'Higgs': {
        'Color': '#0000ff', 
        'Contributions': ['ggH125_WW2lep']},
                    
    'data' : {
        'Contributions': ['data_Egamma', 'data_Muons']}
},

'Depictions': {
    "Order"       : ["Main", "Data/MC", "S/B"],
    "Definitions" : {
      'Data/MC': {
          'type'       : 'Agreement',
          'Paintables' : ['data', 'Stack']},
      
      'Main': {
          'type'      : 'Main',
          'Paintables': ['Stack', 'data', 'Higgs']},
      
      'S/B': {
          'type'       : 'Ratio',
          'Paintables' : ['Higgs', 'Stack']},
      }
}
}