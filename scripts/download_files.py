'''
    usage:
    -----
    python scripts/download_files.py --name=ecohen_physical_files_adi_prodgenie_bnb_nu_uboone_overlay_cosmic_data_100K_reco2
    python scripts/download_files.py --name=adi_prodgenie_bnb_nu_uboone_overlay_cosmic_data_100K_reco2
    python scripts/download_files.py --name=ccqe_ana_MCBNBCosmicDATA --option=makeup --continue_makeup=3215875_826 --ctr=2397
'''

import sys, os, time, argparse
time_name = "%4d_%02d_%02d" % time.localtime()[0:3]


parser = argparse.ArgumentParser()
parser.add_argument('-n','--name', default='ccqe_ana_MCBNBCosmicDATA', type=str )
parser.add_argument('-o','--option', default='download', type=str )
parser.add_argument('--continue_makeup', default='3215875_563', type=str )
parser.add_argument('--ctr', default=0, type=int )
name = parser.parse_args().name
option = parser.parse_args().option
continue_makeup = parser.parse_args().continue_makeup
ctr = parser.parse_args().ctr


uboone = 'ecohen@uboonegpvm04.fnal.gov'
csv_path = '/Users/erezcohen/Desktop/uBoone/CCQEanalysis/csvFiles/'

# for the new overlay: AdiReco27List_18Jan2018
if name=="ccqe_ana_MCBNBCosmicDATA":
    default_pnfsjob = "/pnfs/uboone/scratch/users/ecohen/mcc8/06_26_01_09/ccqe_ana/"+name
    default_outdirname = csv_path+"ccqe_candidates/"

# new overlay using SAM definition
if "prodgenie_bnb_nu_uboone_overlay_cosmic_data" in name:
    default_pnfsjob = "/pnfs/uboone/scratch/users/ecohen/mcc8/06_26_01_09/ccqe_ana/"+name+"_CCQE"
    default_outdirname = csv_path+"ccqe_candidates/"


# pandora pairs
elif name=="prodcosmics_corsika_cmc_uboone_mcc8.4":
    default_pnfsjob = "/pnfs/uboone/scratch/users/ecohen/mcc8/v06_42_00/cosmic_pairs_rejection_pandoraCosmic/prodcosmics_corsika_cmc_uboone_mcc8.4_reco2_cosmic_pairs_rejection_pandoraCosmic/"
    default_outdirname = csv_path+"pandora_pairs/"

default_indirname = csv_path+"from_grid/"+name+"/"



pnfsjob = raw_input("enter pnfs:...<"+default_pnfsjob+">") or default_pnfsjob
print 'pnfsjob: ',pnfsjob
indirname = raw_input("enter indir:...<"+default_indirname+">") or default_indirname
print 'indirname: ',indirname
outdirname = raw_input("enter outdir:...<"+default_outdirname+">") or default_outdirname
print 'outdirname: ',outdirname
print

# step 0: create the indirname directory
os.system("mkdir "+indirname)
print 'step 0: created the indirname directory'
print

# step 1: create a list of files to download
do_step_1 = raw_input("# step 1: create a list of files to download?:...<False>") or False
if do_step_1:#{
    print 'creating a list of files to download from',pnfsjob
    print 'into '+indirname+'/files_to_download.list'
    os.system("ssh "+uboone+" ls "+pnfsjob+"/*/*.csv > "+indirname+"/files_to_download.list")
#}
print
# step 2: grab this list
do_step_2 = raw_input("# step 2: grab this list?:...<False>") or False
if do_step_2:#{
    files_to_download_name = "files_to_download"
    if option=="makeup": files_to_download_name = files_to_download_name + "_since_" + continue_makeup
    with open(indirname+'/'+files_to_download_name+".list") as f:
        files = f.read().splitlines()
#}
print
# step 3: iterate over the list and download the files
do_step_3 = raw_input("# step 3: iterate over the list and download the files?:...<False>") or False
if do_step_3:
    for file in files:#{
        try:
            print 'downloading',file
            destination = file.rsplit('/', 1)[1] + '_%d.csv'%ctr
            print 'into destination',destination
            os.system('scp '+uboone+':'+file+' '+indirname+'/'+destination)
            ctr = ctr + 1
        except IOError:
            pass
    #}
#}
print

# step 4: merge the csv files into a large dataframe
print '# step 4: merge the csv files into a large dataframe'
print 'creating ',name+'_vertices.csv file'
import os, pandas as pd
list_files = os.listdir(indirname)
print "list of files to combine from:",list_files
print
summary_df_array,vertices_df_array,tracks_df_array ,genie_df_array = [],[],[],[]
list_files = os.listdir(indirname)
for file in list_files:#{
    if os.stat(indirname+'/'+file).st_size == 0: continue
    try:
        if "vertices.csv" in file:#{
            print 'adding ',indirname+'/'+file
            vertices_df_array.append(pd.read_csv( ( indirname+'/'+file )))
        #}
        if "summary.csv" in file:#{
            print 'adding ',indirname+'/'+file
            summary_df_array.append(pd.read_csv( ( indirname+'/'+file )))
        #}
        if "tracks.csv" in file:#{
            print 'adding ',indirname+'/'+file
            tracks_df_array.append(pd.read_csv( ( indirname+'/'+file )))
        #}
        if "genie.csv" in file:#{
            print 'adding ',indirname+'/'+file
            genie_df_array.append(pd.read_csv( ( indirname+'/'+file )))
        #}
    except IOError:
        pass
#}
vertices_all = pd.concat(vertices_df_array)
print len(vertices_all),'total pair-vertices'
outfilename = outdirname+'/'+name+'_'+time_name+'_vertices.csv'
vertices_all.to_csv(outfilename)
print 'concatenated %d'%len(vertices_all),'vertices to\n',outfilename,'\ndone.'
print
summary_all = pd.concat(summary_df_array)
print len(summary_all),'is the length summary of all events'
outfilename = outdirname+'/'+name+'_'+time_name+'_summary.csv'
summary_all.to_csv(outfilename)
print 'concatenated %d'%len(summary_all),'summary files to\n',outfilename,'\ndone.'
print
if (len(tracks_df_array)>0):#{
    tracks_all = pd.concat(tracks_df_array)
    print len(tracks_all),'total tracks'
    outfilename = outdirname+'/'+name+'_'+time_name+'_tracks.csv'
    tracks_all.to_csv(outfilename)
    print 'concatenated %d'%len(tracks_all),'tracks to\n',outfilename,'\ndone.'
#}
print
if (len(genie_df_array)>0):#{
    genie_all = pd.concat(genie_df_array)
    print len(vertices_all),'total genie'
    outfilename = outdirname+'/'+name+'_'+time_name+'_genie.csv'
    genie_all.to_csv(outfilename)
    print 'concatenated %d'%len(genie_all),'genie to\n',outfilename,'\ndone.'
#}
print
