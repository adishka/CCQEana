
import sys; sys.path.insert(0, '../../'); sys.path.insert(0,'../mupClassification/')
from ccqe_notebook_tools import *
import matplotlib.patches as patches


debug = 0
Nevents=dict()
Nevents['OffBeam sof.trig. efficiency'] = 0.04462
Nevents['OnBeam sof.trig. efficiency'] = 0.05135


Nevents['v04 after sof.trig.'] = 378787 # from python scripts/count_events.py on <prod_reco2_extbnb_v8_mcc8_v04_26_04_05_v04>
Nevents['v05 after sof.trig.'] = 1815 # from python scripts/count_events.py on <prod_reco2_extbnb_v8_mcc8_v04_26_04_05_v05>
Nevents['OffBeam after sof.trig.'] = Nevents['v04 after sof.trig.'] + Nevents['v05 after sof.trig.']
Nevents['OffBeam before sof.trig.'] = Nevents['OffBeam after sof.trig.']/Nevents['OffBeam sof.trig. efficiency']


Nevents['OnBeam after sof.trig.'] = 544114 # from python scripts/count_events.py on <prod_reco2_bnb_v8_mcc8>
Nevents['OnBeam before sof.trig.'] = Nevents['OnBeam after sof.trig.']/Nevents['OnBeam sof.trig. efficiency']
Nevents['OnBeam POT'] = 4.93e19

OffBeam_scaling = Nevents['OnBeam before sof.trig.']/Nevents['OffBeam before sof.trig.']
print "OffBeam_scaling:",OffBeam_scaling,"= N(on beam)/N(off beam) before sof. trig."


Nevents['MC-BNB/Cosmic-DATA overlay'] = 96350 # from python scripts/count_events.py on <prodgenie_bnb_nu_uboone_overlay_mcc8_reco2>
Nevents['MC-BNB/Cosmic-DATA overlay POT'] = 9.773e19
MC_scaling_DATAcosmic = Nevents['OnBeam POT']/Nevents['MC-BNB/Cosmic-DATA overlay POT']
print "MC_scaling_DATAcosmic:",MC_scaling_DATAcosmic,"= N(POT on beam)/N(POT MC)"

Nevents['MC-BNB/Cosmic-MC overlay'] = 358800 # from python scripts/count_events.py on <prodgenie_bnb_nu_cosmic_uboone_mcc8.2_reco2>
Nevents['MC-BNB/Cosmic-MC overlay POT'] = 3.61901e20
MC_scaling_MCcosmic = Nevents['OnBeam POT']/Nevents['MC-BNB/Cosmic-MC overlay POT']
print "MC_scaling_MCcosmic:",MC_scaling_MCcosmic,"= N(POT on beam)/N(POT MC)"

# -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- -
# Dec-4,2017
def draw_var(cut_name=None,var=None,x_label=None,bins=None,debug=0
             ,do_cosmic_only=True,chi2_xrange=None,chi2_xy=None
             ,reduced_OnBeam=None,reduced_OffBeam=None,MCbnbDATAcosmicSamples=None):
    fig = plt.figure(figsize=(16,12))
    if do_cosmic_only:
        ax = fig.add_subplot(2,1,1)
        ax,leg=extBNBvsCosmicOverlay(OffBeamSample=reduced_OffBeam[cut_name]
                                     ,OffBeamFV=OffBeamFV,MCbnbDATAcosmicSamples=MCbnbDATAcosmicSamples
                          ,cosmic_overlay_sample = reduced_MCbnbDATAcosmicSamples[cut_name]['cosmic']
                          ,var=var , color='black' ,x_label=x_label, bins=bins , ax=ax, legend_loc='bbox')
    ax = fig.add_subplot(2,1,2)
    ax,leg=OnBeam_minus_OffBeam_1d(debug=debug
                                   ,OnBeamSample=reduced_OnBeam[cut_name] 
                                   ,OffBeamSample=reduced_OffBeam[cut_name] 
                                   ,MCsamples=reduced_MCbnbDATAcosmicSamples[cut_name]
                                   ,MCbnbDATAcosmicSamples=MCbnbDATAcosmicSamples
                                   ,var=var
                                   ,x_label=x_label 
                                   ,bins=bins 
                                   ,ax=ax
                                   ,legend_loc='bbox'                                       
                                   ,do_add_chi2_MC_data=True , chi2_xrange=chi2_xrange, chi2_xy=chi2_xy)
    plt.savefig(figures_path+var+'_'+'after_cut_'+cut_name+'.pdf', bbox_inches='tight')    
# -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- -




# -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- -
# Nov-9,2017
def extBNBvsCosmicOverlay(OffBeamSample=None,OffBeamFV=None
                            , var='PIDa_assigned_proton' , x_label='$PID_a^p$' 
                            , bins=np.linspace(0,30,31) 
                            , ax=None, figsize=(14,6),fontsize=25
                            , color='purple'
                            , do_add_cosmic_overlay=True , cosmic_overlay_sample=None, MCbnbDATAcosmicSamples=None
                            , do_add_legend=True , legend_loc='best', overlay_alpha=0.5):
    bin_width = bins[1]-bins[0]
    if ax is None: fig,ax=plt.subplots(figsize=figsize)
    x = OffBeamSample[var]
    h_OffBeam,edges = np.histogram( x , bins=bins )
    h_OffBeam_err = np.sqrt(h_OffBeam)
    Int_OffBeam = np.sum([h_OffBeam[i]*bin_width for i in range(len(h_OffBeam))])
    
    plt.errorbar( x = bins[:-1], xerr=bin_width/2.
                 , y=h_OffBeam , yerr=h_OffBeam_err
                 , fmt='o', color=color , ecolor='black'
                 , label='extBNB (%d=%.1f'%(len(OffBeamSample),100*float(len(OffBeamSample))/len(OffBeamFV))+'%)'
                )
    plt.plot([0,0],[0,0],'--',color='black',linewidth=2)
    
    if do_add_cosmic_overlay:        
        plot_cosmic_overlay( ax=ax                               
                            , cosmic_overlay_sample = cosmic_overlay_sample , var=var, bins=bins 
                            , Int_OffBeam = Int_OffBeam
                            , alpha=overlay_alpha,MCbnbDATAcosmicSamples=MCbnbDATAcosmicSamples)
    set_axes(ax,x_label=x_label,y_label='counts',do_add_grid=True,fontsize=fontsize
             ,xlim=(np.min(bins)-bin_width,np.max(bins)+bin_width)
    #              ,ylim=(0,1.05*np.max(h_OffBeam))
            )
    if do_add_legend: 
        if legend_loc=='bbox':
            leg=plt.legend(bbox_to_anchor=(1.,1.05),fontsize=fontsize,loc=2)
        else:
            leg=plt.legend(fontsize=fontsize,loc=legend_loc)
    plt.tight_layout()
    return ax,leg
# -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- -


# -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- -
# Nov-9,2017
def plot_cosmic_overlay( ax=None, cosmic_overlay_sample=None, var=None, bins=None
                        , alpha=0.5, Int_OffBeam=1,MCbnbDATAcosmicSamples=None):
    x = cosmic_overlay_sample[var]
    bin_width = bins[1]-bins[0]
        
    h_overlay,edges = np.histogram( x , bins=bins )
    Int_overlay = np.sum([h_overlay[i]*bin_width for i in range(len(h_overlay))])
    SUMoverlay = np.sum(h_overlay)    

    cosmic_overlay_scaling = Int_OffBeam/Int_overlay    
    ax.hist( x , weights=cosmic_overlay_scaling*np.ones(len(x))
                     , bins=bins-0.5*bin_width, width=bin_width
                     , color=MCcolors[2]
                     , label='cosmic overlay (%d=%.1f'%(len(cosmic_overlay_sample),100*float(len(cosmic_overlay_sample))/len(MCbnbDATAcosmicSamples['cosmic']))+'%)'
                     , alpha=alpha)       
# -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- -        



# -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- -
# Nov-20,2017
def plot_stacked_MCsamples( ax=None, MCsamples = None , MC_scaling=MC_scaling_DATAcosmic, MCbnbDATAcosmicSamples=None
                           , var=None, bins=None , N_OnBeam_minus_OffBeam=1, alpha=0.8):
    '''
    return: h, bins
            stacked histogram values and bins,
            of the samples from the overlay: 
            (cosmic, other-pairs) + 1mu 1p pairs
    '''
    Nall_pairs = len(MCsamples['1mu-1p']+MCsamples['cosmic']+MCsamples['other pairs'])

    x_array, weights_array = [] , []
    label_array , color_array = [] , []
    # stack background (cosmic, other-pairs) + 1mu1p pairs
    for i_pair_type in [2,1,0]:
        pair_type=pair_types[i_pair_type]
        sample = MCsamples[pair_type]; 
        label = MClabels[i_pair_type]+' (%.1f'%(100*float(len(sample))/len(MCbnbDATAcosmicSamples[pair_type]))+'%)'
        label_array.append(label); 
        color_array.append(MCcolors[i_pair_type]);
        x = sample[var]
        x_array.append(x)
        # normalize the MC to have the same number of events as the total On-Off beam sample
        weights_array.append (MC_scaling * np.ones(len(x)) )
        # -- - - - --------- - - -- ---- -  - --- -- -- -- --
    bin_width = bins[1]-bins[0]
    h,bins_arr,_=ax.hist( x_array , weights=weights_array
                     , bins=bins-0.5*bin_width, width=bin_width
                     , stacked=True 
                     , color=color_array
                     , label=label_array
                     , alpha=alpha)            
    h_stack = h[0]+h[1]+h[2]
    if np.max(h[2])>np.max(ax.get_ylim()):
        ax.set_ylim(np.min(ax.get_ylim()),1.05*np.max(h[2]))
        
    # add CC1p0pi as a box inside the 1mu1p 
    sample = MCsamples[pair_types[3]]
    hCC1p0pi,edges = np.histogram( sample[var] , weights=MC_scaling*np.ones(len(sample)) , bins=bins )
    for bin in range(len(bins[:-2])):
        x, dx = bins[bin+1] - 0.4*bin_width, bin_width 
        y, dy = 0.99*h[2][bin+1] - hCC1p0pi[bin], hCC1p0pi[bin]
        label=MClabels[3]+' (%.1f'%(100*float(len(sample))/len(MCbnbDATAcosmicSamples['CC 1p 0pi']))+'%)'
        ax.add_patch( patches.Rectangle( (x, y),dx,dy, facecolor=MCcolors[3],alpha=0.8*alpha,label=label if bin==0 else None))
        
    return h_stack , bins
# -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- -


# -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- -
# written Nov-9,2017  (last edit Dec-6)
def OnBeam_minus_OffBeam_1d( OnBeamSample=None , OffBeamSample=None , debug=0
                            , var='PIDa_assigned_proton' , x_label='$PID_a^p$' 
                            , bins=np.linspace(0,30,31) 
                            , ax=None, figsize=(14,6),fontsize=25
                            , color='purple'
                            , do_add_MCoverlay=True , MCsamples=None, MCbnbDATAcosmicSamples=None
                            , MC_scaling=MC_scaling_DATAcosmic
                            , do_add_legend=True , legend_loc='best', MCalpha=0.5
                            , do_add_chi2_MC_data=False , chi2_xrange=None, chi2_xy=(0,0)
                            , OriginalOnBeamSample=None , OriginalOffBeamSample=None):
    bin_width = bins[1]-bins[0]
    if ax is None: fig,ax=plt.subplots(figsize=figsize)
    h_OnBeam,edges = np.histogram( OnBeamSample[var] , bins=bins )
    h_OnBeam_err = np.sqrt(h_OnBeam)
    h_OffBeam,edges = np.histogram( OffBeamSample[var] , bins=bins )
    h_OffBeam_err = np.sqrt(h_OffBeam)
    
    h_OnBeam_minus_OffBeam = h_OnBeam - OffBeam_scaling*h_OffBeam
    h_OnBeam_minus_OffBeam_err = np.sqrt( np.square(h_OnBeam_err) + np.square(OffBeam_scaling*h_OffBeam_err)  )
    Integral = len(OnBeamSample) - OffBeam_scaling*len(OffBeamSample)
    Integral_Original = len(OriginalOnBeamSample) - OffBeam_scaling*len(OriginalOffBeamSample)

    
    plt.errorbar( x = bins[:-1], xerr=bin_width/2.
                 , y=h_OnBeam_minus_OffBeam , yerr=h_OnBeam_minus_OffBeam_err
                 , fmt='o', color=color , ecolor='black', label=r'(On-Off) Beam ($\int=$%.1f=%.1f'%(Integral,100*Integral/Integral_Original)+'%)'
                )
    ax.set_xlim(np.min(bins)-bin_width,np.max(bins)+bin_width);
    ax.set_ylim(np.min([0,np.min(h_OnBeam_minus_OffBeam-1.1*h_OnBeam_minus_OffBeam_err)])
                ,np.max(h_OnBeam_minus_OffBeam+1.1*h_OnBeam_minus_OffBeam_err));

    plt.plot([np.min(ax.get_xlim()),np.min(ax.get_xlim())],[0,0],'--',color='black',linewidth=2)
    set_axes(ax,x_label=x_label,y_label='counts',do_add_grid=True,fontsize=fontsize)
    
    if do_add_MCoverlay:        
        N_OnBeam_minus_OffBeam = len(OnBeamSample) - OffBeam_scaling*len(OffBeamSample)
        if debug>1: print 'Number of On-Off:',N_OnBeam_minus_OffBeam

        h_MC, bins_MC = plot_stacked_MCsamples( ax=ax
                               , MCsamples = MCsamples , MCbnbDATAcosmicSamples=MCbnbDATAcosmicSamples
                               , var=var, bins=bins , MC_scaling=MC_scaling
                               , N_OnBeam_minus_OffBeam=N_OnBeam_minus_OffBeam , alpha=MCalpha)
    if do_add_chi2_MC_data:
        chi2 , ndf = chi2_two_histograms( bins=bins, chi2_xrange=chi2_xrange
                                         , h1=h_MC , h2=h_OnBeam_minus_OffBeam 
                                         , h1err=np.sqrt(h_MC), h2err=h_OnBeam_minus_OffBeam_err
                                         , debug=debug )
        plt.text(chi2_xy[0],chi2_xy[1],r'$\chi^2/ndf=%.1f/%d$'%(chi2,ndf),fontsize=fontsize)
        if chi2_xrange is not None:
            plt.plot([chi2_xrange[0],chi2_xrange[0]],ax.get_ylim(),'-',alpha=0.3)
            plt.plot([chi2_xrange[1],chi2_xrange[1]],ax.get_ylim(),'-',alpha=0.3)

    if do_add_legend: 
        if legend_loc=='bbox':
            leg=plt.legend(bbox_to_anchor=(1.,1.05),fontsize=fontsize,loc=2)
        else:
            leg=plt.legend(fontsize=fontsize,loc=legend_loc)
    plt.tight_layout()
    return ax,leg
# -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- -

# -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- -
# Dec-3, 2017 (last edit Dec-9)
def chi2_two_histograms( bins=None, chi2_xrange=None
                        , h1=None , h2=None 
                        , h1err=None, h2err=None 
                        , debug=0):
    '''
    compare the two histograms using a chi2 test.
    return: chi2, ndf
    '''
    chi2 = 0
    Nbins_compares = 0
    for i_bin in range(len(bins)-1):
        if chi2_xrange is None or (bins[i_bin]>=chi2_xrange[0] and bins[i_bin]<=chi2_xrange[1]):
            if debug: 
                print 'comparing in bin:',bins[i_bin],'h1:',h1[i_bin],'+/-',h1err[i_bin],'h2:',h2[i_bin],'+/-',h2err[i_bin]
                print 'chi2+=',(np.square( h1[i_bin] - h2[i_bin] ) / np.max([( np.square(h1err[i_bin]) + np.square(h2err[i_bin]) ),1]))
            chi2 += np.square( h1[i_bin] - h2[i_bin] ) / np.max([( np.square(h1err[i_bin]) + np.square(h2err[i_bin]) ),1])
            Nbins_compares += 1
    ndf = Nbins_compares - 1
    if debug: print 'chi2,ndf:',chi2,ndf
    return chi2,ndf
# -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- -







# -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- -
# Sep-3,2017
def OnBeam_minus_OffBeam_2d( OnBeamSample=None , OffBeamSample=None
                            , varx='l_assigned_proton' , x_label='$l^{\\mu}$'
                            , vary='l_assigned_muon' , y_label='$l^p$'
                            , bins=(np.linspace(0,100,51),np.linspace(0,150,51))
                            , ax=None, figsize=(12,8),fontsize=25
                            , cmap='hot_r'):
    global debug
    if ax is None: fig,ax=plt.subplots(figsize=figsize)
    h_OnBeam_T,xedges, yedges = np.histogram2d( OnBeamSample[varx] , OnBeamSample[vary] , bins=bins )
    h_OffBeam_T,xedges, yedges = np.histogram2d( OffBeamSample[varx] , OffBeamSample[vary] , bins=bins )
    
    h_OnBeam_minus_OffBeam_T = h_OnBeam_T - OffBeam_scaling*h_OffBeam_T
    h_OnBeam_minus_OffBeam = h_OnBeam_minus_OffBeam_T.T
    
    X, Y = np.meshgrid(xedges, yedges)
    pcmesh = ax.pcolormesh(X, Y, h_OnBeam_minus_OffBeam ,cmap=cmap)
    cbar = plt.colorbar(pcmesh,label='(On-Off) Beam [cts]')
    cbar.ax.yaxis.label.set_font_properties(matplotlib.font_manager.FontProperties(size=fontsize))
    cbar.ax.tick_params(labelsize=fontsize)
    
    bin_width = [bins[0][1]-bins[0][0],bins[1][1]-bins[1][0]]
    ax.set_xlim(np.min(bins[0])-bin_width[0],np.max(bins[0])+bin_width[0]);
    ax.set_ylim(np.min(bins[1])-bin_width[1],np.max(bins[1])+bin_width[1]);
    set_axes(ax,x_label=x_label,y_label=y_label,do_add_grid=True,fontsize=fontsize)
# -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- - -- - - -- -- - -- -
