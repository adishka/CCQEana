# combine *vertices.csv files from a grid job
default_name = "prod_reco2_extbnb_v8_mcc8"
name = raw_input("enter list name:...<"+default_name+">") or default_name

defauld_indirname = "/Users/erezcohen/Desktop/uBoone/CCQEanalysis/csvFiles/"+name+"/"
indirname = raw_input("enter indir:...<"+defauld_indirname+">") or defauld_indirname

defauls_outdirname = "/Users/erezcohen/Desktop/uBoone/CCQEanalysis/csvFiles/ccqe_candidates/"
outdirname = raw_input("enter outdir:...<"+defauls_outdirname+">") or defauls_outdirname


print 'creating ',name+'_vertices.csv file'
import os, pandas as pd
list_files = os.listdir(indirname)
print "list of files to combine from:",list_files

vertices_df_array = []
list_files = os.listdir(indirname)
for file in list_files:#{
    if "vertices.csv" in file:#{
        print 'adding ',indirname+'/'+file
        vertices_df_array.append(pd.read_csv( ( indirname+'/'+file )))
    #}
#}
vertices_all = pd.concat(vertices_df_array)
print len(vertices_all),'total pair-vertices'
outfilename = outdirname+'/'+name+'_vertices.csv'
vertices_all.to_csv(outfilename)
print 'concatenated %d'%len(vertices_all),'vertices to\n',outfilename,'\ndone.'
