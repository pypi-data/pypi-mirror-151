import numpy as np
import os.path as osp
import copy
import os
import matplotlib.pyplot as plt
import cv2
from skimage.morphology import opening, disk
from skimage.measure import perimeter
from matplotlib import cm
from scipy import stats
import seaborn as sns
from torch import clamp_min
from NaroNet.utils.parallel_process import parallel_process
from tifffile.tifffile import imwrite
import pandas as pd
import gc
import itertools
from skimage import filters
import time 
from openTSNE import TSNE
from sklearn.preprocessing import StandardScaler
from torch_geometric.data.makedirs import makedirs


def visualize_tsne_phenotypes(dataset, IndexAndClass,clusters):

    def load_embeddings(patch_dir):
        
        # Initialize features    
        features = []
        features_idx = []

        # Extract patches and save it into a graph
        for subject in IndexAndClass:                                    
            
            # Load image 
            subject_feats = np.load(patch_dir + subject[0] + '.npy')

            # Store feats
            features.append(subject_feats)
            
            # Store subject idx
            features_idx.append([subject[1]]*subject_feats.shape[0])

        # Store in one file all features
        features = np.concatenate(features,axis=0)
        features_idx = np.concatenate(features_idx,axis=0)    
        return features, features_idx
    
    def tsne_with_pheno_thrshold(dataset,features_idx,features,pheno_assignmnents):
        
        # Select number of patches
        num_val =min(10000000,features_idx.shape[0])     
        features_idx = features_idx[::int(features_idx.shape[0]/num_val)]
        features = features[::int(features.shape[0]/num_val),:]
        pheno_assignmnents = pheno_assignmnents[::int(features.shape[0]/num_val),:]
        
        # Reorder samples
        sel_vals = np.random.randint(0,high=features.shape[0],size=features.shape[0])
        features = features[sel_vals,:]
        features_idx = features_idx[sel_vals]
        pheno_assignmnents = pheno_assignmnents[sel_vals,:]
        
        # Normalize features
        scaled_features = StandardScaler().fit_transform(features[:,2:])

        # Create UMAP
        embedding = TSNE(n_jobs=8,random_state=3, verbose=True).fit(scaled_features)

        # Show each phenotype
        for ph in range(pheno_assignmnents.shape[1]):

            # Create and save scatter plot figure
            plt.close('all')
            fig, ax = plt.subplots()   
            scatter = ax.scatter(embedding[:, 0],embedding[:, 1],s=0.5,c=pheno_assignmnents[:,ph],vmin=0,vmax=1,cmap='jet',edgecolors='none')        
            plt.title('TSNE of the dataset Phenoptype - '+str(ph+1), fontsize=24)    
            plt.colorbar(scatter)
            plt.savefig(dataset.bioInsights_dir_cell_types_Pheno+'tSNE/'+'Ph_'+str(ph+1)+'.png',dpi=600)

        pheno_assignmnents_75 = np.zeros(pheno_assignmnents.shape[0])
        for ph in range(pheno_assignmnents.shape[1]):
            thr = np.percentile(pheno_assignmnents[pheno_assignmnents.argmax(1)==ph,ph],90)
            pheno_assignmnents_75[np.logical_and(pheno_assignmnents.argmax(1)==ph,pheno_assignmnents[:,ph]>=thr)] = ph+1
        plt.close('all')
        fig, ax = plt.subplots()   
        scatter = ax.scatter(embedding[:, 0],embedding[:, 1],s=0.5,c=pheno_assignmnents_75,cmap='jet',edgecolors='none')        
        plt.title('TSNE of the dataset ALL_Phenotypes D1', fontsize=24)    
        plt.colorbar(scatter)
        plt.savefig(dataset.bioInsights_dir_cell_types_Pheno+'tSNE/'+'ALL_Phenotypes_D1.png',dpi=600)        


    pat_num = int(len(IndexAndClass)*dataset.args['TSNE_Perc_Pat'])
    IndexAndClass = IndexAndClass[:pat_num]

    # Directory to load
    patch_dir = dataset.root+'Patch_Contrastive_Learning/Image_Patch_Representation/'       

    # Load data
    features, features_idx = load_embeddings(patch_dir)

    # Load pheno assignments
    pheno_assignmnents = []
    for subject_idx, subject_info in enumerate(IndexAndClass):              
        _, cell_type_assignment = load_cell_types_assignments(dataset, 0, subject_info, 0, clusters[0], [])
        pheno_assignmnents.append(cell_type_assignment[:(features_idx==subject_info[1]).sum(),:])
    pheno_assignmnents = np.concatenate(pheno_assignmnents,axis=0)   
        
    # Create Tsne 
    makedirs(dataset.bioInsights_dir_cell_types_Pheno+'tSNE/')
    embedding = tsne_with_pheno_thrshold(dataset,features_idx,features,pheno_assignmnents)


def load_cell_types_assignments(dataset, cell_type_idx, subject_info,subgraph_idx,n_cell_types, prev_cell_type_assignment):
    """
    Obtain matrix that assigns patches to cell types (phenotypes and neighborhoods)
    dataset: (object)
    cell_type_idx: (int) cell_type_idx==0 is phenotype, cell_type_idx==1 is neihborhood, cell_type_idx==2 is neihborhood interaction
    subject_info: (list of str and int)
    subgraph_idx: (int) specifying the index of the subgraph.
    n_cell_types: (int) number of cell types (phenotypes or neighborhoods)
    prev_cell_type_assignment: (array of int) specifying assignments
    """

    # If phenotype or neighborhood load matrix assignment.
    if cell_type_idx<2:
        cell_type_assignment = np.load(osp.join(dataset.processed_dir_cell_types,
                    'cluster_assignmentPerPatch_Index_{}_{}_ClustLvl_{}.npy'.format(subject_info[1], subgraph_idx, n_cell_types)))                        

    # if neighborhood interaction the matrix assigns neighbors to neighborhood interactions.
    else:        
        # Load neighborhood interactions
        secondorder_assignment = np.load(osp.join(dataset.processed_dir_cell_types,
                                'cluster_assignment_Index_{}_ClustLvl_{}.npy'.format(subject_info[1], n_cell_types)))                    
        
        # Obtain assignment of patches to neighborhood interactions
        cell_type_assignment = np.matmul(prev_cell_type_assignment,secondorder_assignment)
    prev_cell_type_assignment = copy.deepcopy(cell_type_assignment)
    
    return prev_cell_type_assignment, cell_type_assignment

def load_patch_image(dataset,imList):
    '''
    Load patch image
    # Create label map. 
    labels = []
    last_patch = 0
    for im_i in imList:
        num_patches = int(im_i.shape[0]/dataset.patch_size)*int(im_i.shape[1]/dataset.patch_size)
        labels.append(np.reshape(np.array(range(last_patch,last_patch+num_patches)),(int(im_i.shape[0]/dataset.patch_size),int(im_i.shape[1]/dataset.patch_size))))
        last_patch = last_patch+num_patches
    labels = np.concatenate(labels,1)
    '''             

    labels = []
    last_patch = 0
    x_y_shape = [0,0]
    for im_i in imList:

        # Create label image
        num_patches = int(im_i.shape[0]/dataset.patch_size)*int(im_i.shape[1]/dataset.patch_size)
        labels.append(np.transpose(np.reshape(np.array(range(last_patch,last_patch+num_patches)),(int(im_i.shape[1]/dataset.patch_size),int(im_i.shape[0]/dataset.patch_size)))))
        last_patch = last_patch+num_patches

        # Update shape of mosaic
        x_y_shape[0], x_y_shape[1] = max(labels[-1].shape[0],x_y_shape[0]), labels[-1].shape[1]+x_y_shape[1]
            
    # Create mosaic
    mosaic = np.zeros(x_y_shape,dtype=np.uint32)+4294967295

    # Concatenate images
    col=0
    for lab in labels:
        mosaic[0:lab.shape[0],col:col+lab.shape[1]] = lab
        col += lab.shape[1]

    return mosaic, labels

def select_patches_from_cohort_(clusters,dataset,subject_info,count):

    # Crops,Confidence,and Phenotype Vector.
    CropConfPheno = []
    CropConfTissueComm = []
    TissueArea_Conf = []
    for c in range(clusters[0]):
        CropConfPheno.append([])
            
    for c in range(clusters[1]):
        CropConfTissueComm.append([])  
    
    for c in range(clusters[2]):
        TissueArea_Conf.append([]) 

    # Crops,Confidence,and Phenotype Vector.    
    prev_cell_type_assignment=[]
        
    # Apply mask to patch
    for subgraph_idx in range(dataset.findLastIndex(subject_info[1])+1):                
        
        # Open Raw Image.        
        im, imList = dataset.open_Raw_Image(subject_info,1)                

        for cell_type_idx, n_cell_types in enumerate(clusters):    
            # load cell_types_assignments
            prev_cell_type_assignment, cell_type_assignment = load_cell_types_assignments(
                                                                    dataset,cell_type_idx,subject_info,subgraph_idx,
                                                                    n_cell_types,prev_cell_type_assignment)                               
            # Open Single-Cell Contrastive Learning Information
            PCL_reprsntions = np.load(dataset.raw_dir+'/{}.npy'.format(subject_info[0]))                     

            # Phenotypes and neighborhoods, or areas
            if cell_type_idx<2:             
                # Select patches with most confidence
                CropConfPheno,CropConfTissueComm = topk_confident_patches(dataset,n_cell_types,
                                                                            cell_type_assignment,cell_type_idx,CropConfPheno,
                                                                            CropConfTissueComm,im,imList,PCL_reprsntions,count)  
            else:
                # Save subject index and max cell type
                for c_type in range(n_cell_types):
                    TissueArea_Conf[c_type].append(cell_type_assignment[:,c_type])

    del im, imList, PCL_reprsntions
    gc.collect(0)
    gc.collect(1)
    gc.collect(2)
    time.sleep(3)

    return CropConfPheno,CropConfTissueComm,TissueArea_Conf


def select_patches_from_cohort(dataset,IndexAndClass,clusters):
    '''
    '''
     
    # Prepare parallel process
    dict_subjects = []
    for count, subject_info in enumerate(IndexAndClass):
        if subject_info[2][0]!='None':
            dict_subjects.append({'clusters':clusters,'dataset':dataset,'subject_info':subject_info,'count':count})
    
    # select_patches_from_cohort
    result_images = parallel_process(dict_subjects,select_patches_from_cohort_,use_kwargs=True,front_num=1,desc='BioInsights: Get relevant examples of cell types') 

    # Crops,Confidence,and Phenotype Vector.
    CropConfPheno = []
    CropConfTissueComm = []
    TissueArea_Conf = []
    for c in range(clusters[0]):
        CropConfPheno.append([])
            
    for c in range(clusters[1]):
        CropConfTissueComm.append([])  
    
    for c in range(clusters[2]):
        TissueArea_Conf.append([])  

    # Get lists of patches
    for cluster_level in result_images:  
        for clust_idx, cluster in enumerate(cluster_level[0]):
            for patch in cluster:  
                CropConfPheno[clust_idx].append(patch)
        for clust_idx, cluster in enumerate(cluster_level[1]):
            for patch in cluster:  
                CropConfTissueComm[clust_idx].append(patch)
        for r_i, r in enumerate(cluster_level[2]):
            TissueArea_Conf[r_i].append(r)
            
    return CropConfPheno,CropConfTissueComm, TissueArea_Conf

def topk_confident_patches(dataset,n_cell_types,
                            cell_type_assignment,cell_type_idx,CropConfPheno,
                            CropConfTissueComm,im,imList,PCL_reprsntions,count):
    '''
    '''
    K = int(np.ceil(10/dataset.processed_file_names*100))

    # Create label map. 
    labels,labels_list = load_patch_image(dataset,imList)
    # for ll in range(len(labels_list)):
    #     labels_list[ll] = np.transpose(labels_list[ll])
    # labels = np.concatenate(labels_list,axis=1)

            
    for c in range(n_cell_types):
                                                                        
        # Obtain patch info of the K with most certainty
        highest_ent_patches = cell_type_assignment[:PCL_reprsntions.shape[0],c].argsort()[-K:]
        for patch_idx in highest_ent_patches:                  
                    
            # Select the patch from the patch_image            
            mask = labels==patch_idx

            if cell_type_idx==0:
                mx_val = mask.argmax(0).max()*dataset.patch_size
                mxx_val = mask.argmax(1).max()*dataset.patch_size
                CropConfPheno[c].append([im[mx_val:mx_val+dataset.patch_size,mxx_val:mxx_val+dataset.patch_size].copy(), # The original Image
                                            cell_type_assignment[patch_idx,c], # The cell type certainty
                                            [], # The parameters obtained from contrastive learning
                                            [100000*count+patch_idx]]) # Number of the image, and patch identificator
            elif cell_type_idx==1:
                mx_val = mask.argmax(0).max()*dataset.patch_size
                mxx_val = mask.argmax(1).max()*dataset.patch_size
                minIdx = mx_val-dataset.patch_size*2
                maxIdx = mx_val+dataset.patch_size*3
                minIdy = mxx_val-dataset.patch_size*2
                maxIdy = mxx_val+dataset.patch_size*3
                if maxIdx>im.shape[0] or maxIdy>im.shape[1] or minIdx<0 or minIdy<0:
                    continue
                CropConfTissueComm[c].append([im[minIdx:maxIdx,minIdy:maxIdy].copy(), # The original Image
                                            cell_type_assignment[patch_idx,c], # The cell type certainty
                                            [100000*count+patch_idx]]) # Patch identificator 
    
    return CropConfPheno,CropConfTissueComm

def save_2Dmatrix_in_excel_with_names(filename,matrix,Names):
    dict_ = {}
    for n, name in enumerate(Names):
        dict_[name] = matrix[:,n]
    dict_ = pd.DataFrame.from_dict(dict_)      
    dict_.to_excel(filename) 

def save_heatmap_with_names(filename,matrix,Names):   
    import sys
    sys.setrecursionlimit(1000000) 
    if matrix.shape[0]>2:
        plt.close('all')
        plt.figure()
        sns.set(font_scale=1.1)
        scaler = StandardScaler()
        scaler.fit(matrix)        
        h_E_Fig = sns.clustermap(scaler.transform(matrix)*25+128, row_cluster=True, xticklabels=Names, linewidths=0,vmin=-2, vmax=2, cmap="bwr")                
        h_E_Fig.savefig(filename,dpi=600) 

def calculate_pearson_correlation(matrix_0,matrix_1):
    cor_val = stats.spearmanr(matrix_0.flatten(),matrix_1.flatten()).correlation
    cor_val = 0 if np.isnan(cor_val) else cor_val
    return cor_val

def calculate_marker_colocalization(matrix,MarkerNames):
    # matrix: contains (number of patches, x_dimension, y_dimension, number of markers)
    Marker_Colocalization =  np.ones((len(MarkerNames),len(MarkerNames)))
    for n_comb, pair_of_markers in enumerate(itertools.combinations(MarkerNames,2)):
        id_0 = MarkerNames.index(pair_of_markers[0])
        id_1 = MarkerNames.index(pair_of_markers[1])
        matrix_0 = matrix[:,:,:,[id_0]]
        matrix_1 = matrix[:,:,:,[id_1]]
        # for n_patch in range(matrix.shape[0]):            
        Marker_Colocalization[id_0,id_1] = calculate_pearson_correlation(matrix_0,matrix_1)
        Marker_Colocalization[id_1,id_0] = Marker_Colocalization[id_0,id_1]
    return Marker_Colocalization

def calculate_Cell_Size_circularity(filename, matrix):
    # matrix: contains (number of patches, x_dimension, y_dimension)         
    # selem = disk(2)
    Size = np.zeros((matrix.shape[3]))
    Eccentricity = np.zeros((matrix.shape[3]))
    Granularity = np.zeros((matrix.shape[3]))
    for mk in range(matrix.shape[3]):

        # Calculate global threshold
        thr = filters.threshold_otsu(matrix[:,:,:,mk])

        # Initialize count
        count = 0 

        for patch in range(matrix.shape[0]):
            
            if matrix[patch,:,:].sum()>0 and (matrix[patch,:,:].max()-matrix[patch,:,:].min())>0:
                logical = matrix[patch,:,:,mk]>thr
                output = cv2.connectedComponentsWithStats(np.array(logical,dtype=np.uint8), 4, cv2.CV_32S)

                if output[0]>1: # at least one component
                    Size[mk] += output[2][1:,4].mean()                    
                    Eccentricity[mk] += min((4*3.14159*(output[1]==1).sum())/(perimeter((output[1]==1),neighbourhood=4)**2),1) # Eccentricity
                    Granularity[mk] += output[0]-1

                    count += 1
        if count>0:
            Size[mk] /= count
            Eccentricity[mk] /= count
            Granularity[mk] /= count
        else:
            Size[mk] = 0
            Eccentricity[mk] = 0
            Granularity[mk] = 0

    return Size, Eccentricity, Granularity

def extract_topk_patches_from_cohort(dataset, CropConf, Marker_Names,cell_type,Thresholds):
    '''
    docstring
    '''

    thisfolder = dataset.bioInsights_dir_cell_types + cell_type+'/'

    if cell_type=='Phenotypes':
        mult_1 = 1 
        mult_2 = 2
    else:
        mult_1 = 5 
        mult_2 = 4

    ## Iterate through Phenotypes to extract topk patches
    k=100
    topkPatches=[]
    # Create a heatmap marker using topk patches
    heatmapMarkerExpression = np.zeros((len(CropConf),len(Marker_Names))) # Number of TMEs x number of markers
    heatmap_Colocalization = np.zeros((len(CropConf),len(Marker_Names),len(Marker_Names))) # Number of TMEs x Number of Markers x Number of Markers
    heatmap_Size = np.zeros((len(CropConf),len(Marker_Names))) # size and circularity of markers
    heatmap_Eccentricity = np.zeros((len(CropConf),len(Marker_Names))) # size and circularity of markers
    heatmap_Granularity = np.zeros((len(CropConf),len(Marker_Names))) # size and circularity of markers

    # Make directory
    makedirs(thisfolder+'Prototypes/')

    # Use CropCOnf, that saves a lot of patches...
    for n_cell_type ,CropConf_i in enumerate(CropConf):
        
        if len(CropConf_i)==0: # Let te heatmap be zero in case no cells were assigned to this TME.
            continue
        
        # Choose patches with most confidence
        topkPheno = np.array([CCP[1] for CCP in CropConf_i]).argsort()[-k:]               
        
        heatmap_Colocalization[n_cell_type,:,:] = calculate_marker_colocalization(np.array([CropConf_i[t][0] for t in topkPheno]),Marker_Names)    
        heatmap_Size[n_cell_type,:], heatmap_Eccentricity[n_cell_type,:], heatmap_Granularity[n_cell_type,:] = calculate_Cell_Size_circularity(thisfolder,np.array([CropConf_i[t][0] for t in topkPheno]))

        # Save topkPheno to heatMarkerMap. Mean
        MarkerExpression = np.array([CropConf_i[t][0].mean((0,1)) for t in topkPheno])
              
        heatmapMarkerExpression[n_cell_type,:] = np.mean(MarkerExpression,axis=0)                    
      
        # Save Image in RGB
        ImwithKPatches = np.zeros((dataset.patch_size*mult_1*int(np.sqrt(k))+mult_2*int(np.sqrt(k)),dataset.patch_size*mult_1*int(np.sqrt(k))+mult_2*int(np.sqrt(k)),CropConf_i[0][0].shape[2]))
        for t_n, t in enumerate(topkPheno):
            row = np.floor(t_n/int(k**0.5))
            col = np.mod(t_n,int(k**0.5))
       
            # Assign patch to Image
            ImwithKPatches[int(row*mult_1*dataset.patch_size+row*mult_2):int((row+1)*mult_1*dataset.patch_size+row*mult_2),int(col*mult_1*dataset.patch_size+col*mult_2):int((col+1)*mult_1*dataset.patch_size+col*mult_2),:] = CropConf_i[t][0]
        
        # Fill unassigned patches with zeroes.
        for t_n in range(len(topkPheno),k):
            row = np.floor(t_n/int(k**0.5))
            col = np.mod(t_n,int(k**0.5))
            # Assign patch to Image
            ImwithKPatches[int(row*mult_1*dataset.patch_size+row*mult_2):int((row+1)*mult_1*dataset.patch_size+row*mult_2),int(col*mult_1*dataset.patch_size+col*mult_2):int((col+1)*mult_1*dataset.patch_size+col*mult_2),:] = 0.0
                        
        # RGBImwithKPatches = dataset.nPlex2RGB(ImwithKPatches)
        imwrite(thisfolder+'Prototypes/Cell_type_{}_Raw.tiff'.format(n_cell_type+1),np.moveaxis(ImwithKPatches,2,0), photometric='minisblack')
        
        # Save Certainty of this Phenotype
        plt.close('all')
        plt.figure()
        n, bins, patches = plt.hist(np.array([i[1] for i in CropConf_i]),range=(0, 1), color=cm.jet_r(int(n_cell_type*(255/int(len(CropConf))))), alpha=1)            
        plt.ylabel('Number of Patches',fontsize=16)            
        plt.xlabel('Level of TME certainty',fontsize=16)
        plt.title('Histogram of TME ' + str(n_cell_type+1) + ' certainty',fontsize=16)
        plt.savefig(thisfolder+'Prototypes/ConfidenceHistogram_{}.png'.format(n_cell_type+1), format="PNG",dpi=600)                                         

        # Assign topkPheno Patches
        topkPatches+=[CropConf_i[t] for t in topkPheno]     

    return heatmapMarkerExpression, heatmap_Colocalization, heatmap_Size, heatmap_Eccentricity, heatmap_Granularity

def save_heatmap_raw_and_normalized(filename, heatmap, TME_names,Colormap,Marker_Names):    
    y_ticklabels = TME_names[heatmap.sum(1)!=0]
    c_map = Colormap[:heatmap.shape[0]][heatmap.sum(1)!=0]
    # Figure Heatmap Raw Values
    plt.close('all')
    plt.figure()
    sns.set(font_scale=0.9)
    cluster=True if (heatmap.sum(1)!=0).sum()>1 else False
    h_E_Fig = sns.clustermap(heatmap[heatmap.sum(1)!=0,:],col_cluster=cluster, row_cluster=cluster, row_colors=c_map,xticklabels=Marker_Names,yticklabels=y_ticklabels,vmin=-1,vmax=1, linewidths=0.5, cmap="bwr")            
    h_E_Fig.savefig(filename+'_Raw.png',dpi=600) 

    # Save Excel.
    df = pd.DataFrame(heatmap[heatmap.sum(1)!=0,:], columns = Marker_Names)
    df.index = y_ticklabels
    df.to_excel(filename+'_Raw.xlsx')  

    # Figure Heatmap Min is 0 and max is 1 Values    
    h_E_COL_MinMax = heatmap[heatmap.sum(1)!=0,:] - heatmap[heatmap.sum(1)!=0,:].min(0,keepdims=True)
    h_E_COL_MinMax = h_E_COL_MinMax/h_E_COL_MinMax.max(0,keepdims=True)
    h_E_COL_MinMax[np.isnan(h_E_COL_MinMax)] = 0 
    plt.close('all')
    plt.figure()
    sns.set(font_scale=0.9)
    if (h_E_COL_MinMax.sum(1)!=0).sum()==1: # One column heatmap
        h_E_Fig = sns.clustermap(h_E_COL_MinMax[h_E_COL_MinMax.sum(1)!=0,:],col_cluster=False, 
            row_cluster=False, row_colors=c_map,xticklabels=Marker_Names,yticklabels=y_ticklabels, linewidths=0.5,vmin=-1,vmax=1, cmap="bwr")            
        h_E_Fig.savefig(filename+'_MinMax.png',dpi=600) 
    elif (h_E_COL_MinMax.sum(1)!=0).sum()>1: # Normal heatmap.    
        h_E_Fig = sns.clustermap(h_E_COL_MinMax[h_E_COL_MinMax.sum(1)!=0,:],col_cluster=True, 
            row_cluster=True, row_colors=c_map,xticklabels=Marker_Names,yticklabels=y_ticklabels, linewidths=0.5,vmin=-1,vmax=1, cmap="bwr")            
        h_E_Fig.savefig(filename+'_MinMax.png',dpi=600)  
    
    # Figure Heatmap z-scored values
    h_E_COL_Norm = stats.zscore(heatmap[heatmap.sum(1)!=0,:],axis=0)  
    h_E_COL_Norm[np.isnan(h_E_COL_Norm)] = 0              
    plt.close('all')
    plt.figure()
    sns.set(font_scale=0.9)    
    if (h_E_COL_Norm.sum(1)!=0).sum()==1: # One column heatmap
        h_E_Fig = sns.clustermap(h_E_COL_Norm,col_cluster=False, vmin=-1, vmax=1, row_cluster=False, row_colors=c_map,xticklabels=Marker_Names,yticklabels=y_ticklabels, linewidths=0.5, cmap="bwr")            
        h_E_Fig.savefig(filename+'_Norm.png',dpi=600) 
    elif (h_E_COL_Norm.sum(1)!=0).sum()>1: # Normal heatmap
        h_E_Fig = sns.clustermap(h_E_COL_Norm,col_cluster=True, vmin=-1, vmax=1, row_cluster=True, row_colors=c_map,xticklabels=Marker_Names,yticklabels=y_ticklabels, linewidths=0.5, cmap="bwr")            
        h_E_Fig.savefig(filename+'_Norm.png',dpi=600) 

    # Figure Heatmap z-scored values
    h_E_COL_Norm = stats.zscore(h_E_COL_Norm[heatmap.sum(1)!=0,:],axis=1)  
    h_E_COL_Norm[np.isnan(h_E_COL_Norm)] = 0              
    plt.close('all')
    plt.figure()
    sns.set(font_scale=0.9)    
    if (h_E_COL_Norm.sum(1)!=0).sum()==1: # One column heatmap
        h_E_Fig = sns.clustermap(h_E_COL_Norm,col_cluster=False, vmin=-1, vmax=1, row_cluster=False, row_colors=c_map,xticklabels=Marker_Names,yticklabels=y_ticklabels, linewidths=0.5, cmap="bwr")            
        h_E_Fig.savefig(filename+'_Norm_rows.png',dpi=600) 
    elif (h_E_COL_Norm.sum(1)!=0).sum()>1: # Normal heatmap
        h_E_Fig = sns.clustermap(h_E_COL_Norm,col_cluster=True, vmin=-1, vmax=1, row_cluster=True, row_colors=c_map,xticklabels=Marker_Names,yticklabels=y_ticklabels, linewidths=0.5, cmap="bwr")            
        h_E_Fig.savefig(filename+'_Norm_rows.png',dpi=600) 

def save_heatMapMarker_and_barplot(dataset, heatmapMarkerExpression, heatmap_Colocalization, heatmap_Size, heatmap_Eccentricity, heatmap_Granularity, CropConf,Marker_Names,cell_type,Thresholds):
    '''
    '''
    if cell_type=='Phenotypes':
        abrev = 'P'
        names = np.array([abrev+str(i+1) for i in range(len(CropConf))])

        # Exclude phenotypes from the analysis
        phnos = np.array(range(heatmapMarkerExpression.shape[0]))
        for excluded in dataset.args['Pheno_Excluded_from_analysis']:            
            phnos = phnos[phnos!=excluded-1]
        heatmapMarkerExpression = heatmapMarkerExpression[phnos,:]
        heatmap_Size = heatmap_Size[phnos,:]
        heatmap_Eccentricity = heatmap_Eccentricity[phnos,:]
        heatmap_Granularity = heatmap_Granularity[phnos,:]
        names = names[phnos]
        
    else:
        abrev = 'N'
        names = np.array([abrev+str(i+1) for i in range(len(CropConf))])

        # Exclude phenotypes from the analysis
        neighs = np.array(range(heatmapMarkerExpression.shape[0]))
        for excluded in dataset.args['Neigh_Excluded_from_analysis']:            
            neighs = neighs[neighs!=excluded-1]
        heatmapMarkerExpression = heatmapMarkerExpression[neighs,:]
        heatmap_Size = heatmap_Size[neighs,:]
        heatmap_Eccentricity = heatmap_Eccentricity[neighs,:]
        heatmap_Granularity = heatmap_Granularity[neighs,:]
        names = names[neighs]

    Colormap=cm.jet(range(0,255,int(255/heatmapMarkerExpression.shape[0])))[:,:3]

    # Save heatmapmarker to disk    
    makedirs(dataset.bioInsights_dir_cell_types+cell_type+'/Marker_Expression/')
    save_heatmap_raw_and_normalized(dataset.bioInsights_dir_cell_types+cell_type+'/Marker_Expression/heatmap', 
                                        heatmapMarkerExpression, names,
                                        Colormap,Marker_Names)

    makedirs(dataset.bioInsights_dir_cell_types+cell_type+'/Morphology/')
    save_heatmap_raw_and_normalized(dataset.bioInsights_dir_cell_types+cell_type+'/Morphology/Heatmap_Size', 
                                        heatmap_Size, names,
                                        Colormap,Marker_Names)            

    save_heatmap_raw_and_normalized(dataset.bioInsights_dir_cell_types+cell_type+'/Morphology/heatmap_Eccentricity', 
                                        heatmap_Eccentricity, names,
                                        Colormap,Marker_Names)         

    save_heatmap_raw_and_normalized(dataset.bioInsights_dir_cell_types+cell_type+'/Morphology/heatmap_Granularity', 
                                        heatmap_Granularity, names,
                                        Colormap,Marker_Names)     

    # Correlation matrix
    makedirs(dataset.bioInsights_dir_cell_types+cell_type+'/Marker_Colocalization/')
    mask = np.triu(np.ones_like(heatmap_Colocalization[0,:,:], dtype=np.bool))
    sns.set(font_scale=0.5)    
    for TME in range(len(heatmap_Colocalization)):
        plt.close('all')
        plt.figure()
        heatmap = sns.heatmap(heatmap_Colocalization[TME,:,:], mask=mask, vmin=heatmap_Colocalization.min(), vmax=heatmap_Colocalization.max(),xticklabels=Marker_Names,yticklabels=Marker_Names, cmap='BrBG')
        heamap = heatmap.get_figure()
        heamap.savefig(dataset.bioInsights_dir_cell_types+cell_type+'/Marker_Colocalization/heatmap_Colocalization_'+abrev+str(TME+1)+'.png',dpi=600) 
        df = pd.DataFrame(heatmap_Colocalization[TME,:,:], columns = Marker_Names)
        df.index = Marker_Names
        df.to_excel(dataset.bioInsights_dir_cell_types+cell_type+'/Marker_Colocalization/heatmap_Colocalization_'+abrev+str(TME+1)+'.xlsx')  

       

def neigh_comp(TC,phenoInd):
    InteractivityVect = np.zeros(len(phenoInd))
    for n_Phen, PH in enumerate(phenoInd):
        PH = [p[0] for p in PH]
        if len(PH)>0:
            for t in TC:
                if t[2] in PH:
                    InteractivityVect[n_Phen]+=1     
    return InteractivityVect

def obtain_neighborhood_composition(dataset,CropConfPheno,CropConfTissueComm):
    '''
    '''

    # Find indices of phenotypes
    phenoInd = []
    for c in CropConfPheno:
        # Find all indices
        phenoInd.append([c_n[3] for c_n in c])        

    # Generate Interactivity matrix
    dict_neigh = []
    for n_Neighbor, TC in enumerate(CropConfTissueComm):
        dict_neigh.append({'TC':TC,'phenoInd':phenoInd})
    result = parallel_process(dict_neigh,neigh_comp,use_kwargs=True,front_num=1,desc='BioInsights: Calculate phenotype abundance whithin neighborhoods') 
    InteractivityMatrix = np.stack(result)

    # Input
    Colormap_Pheno=cm.jet_r(range(0,255,int(255/len(CropConfPheno))))[:,:3]
    Colormap_Neigh=cm.jet_r(range(0,255,int(255/len(CropConfTissueComm))))[:,:3]

    # Save interactivity matrix
    sns.set(font_scale=1.5)
    plt.close('all')
    heatmapInteractivityMatrix_Fig = sns.clustermap(InteractivityMatrix,col_cluster=False, row_cluster=False, row_colors=Colormap_Neigh, col_colors=Colormap_Pheno,xticklabels=['P'+str(i+1) for i in range(len(CropConfPheno))],yticklabels=['N'+str(i+1) for i in range(len(CropConfTissueComm))], linewidths=0.5, cmap="bwr")            
    plt.xlabel("Phenotypes")
    plt.ylabel("Neighborhoods")
    heatmapInteractivityMatrix_Fig.savefig(dataset.bioInsights_dir_cell_types+'Neighborhoods/heatmap_InteractivityMat_Raw.png',dpi=600) 
    plt.close('all')
    InteractivityMatrix[InteractivityMatrix==0]=1e-3
    heatmapInteractivityMatrix_Fig = sns.clustermap(stats.zscore(InteractivityMatrix,axis=1),col_cluster=False, row_cluster=False, row_colors=Colormap_Neigh, col_colors=Colormap_Pheno,xticklabels=['P'+str(i+1) for i in range(len(CropConfPheno))],yticklabels=['N'+str(i+1) for i in range(len(CropConfTissueComm))], linewidths=0.5, cmap="bwr")            
    plt.xlabel("Phenotypes")
    plt.ylabel("Neighborhoods")
    heatmapInteractivityMatrix_Fig.savefig(dataset.bioInsights_dir_cell_types+'Neighborhoods/heatmap_InteractivityMat_Norm.png',dpi=600) 

def Area_to_Neighborhood_to_Phenotype(dataset,clusters,IndexAndClass, ClusteringThreshold):
    
    # Initialize variables
    neigh_to_area = []
    patch_to_pheno = []
    patch_to_neigh = []

    # Obtain clusters per Slide
    for count, idxclster in enumerate(IndexAndClass):           
        try:

            # Load assignment
            neigh_to_area_assignment = np.load(osp.join(dataset.processed_dir_cell_types,'cluster_assignment_Index_{}_ClustLvl_{}.npy'.format(idxclster[1], clusters[-1])))                
            patch_to_neigh_assignment = np.load(osp.join(dataset.processed_dir_cell_types,'cluster_assignmentPerPatch_Index_{}_0_ClustLvl_{}.npy'.format(idxclster[1], clusters[-2])))        
            patch_to_pheno_assignment = np.load(osp.join(dataset.processed_dir_cell_types,'cluster_assignmentPerPatch_Index_{}_0_ClustLvl_{}.npy'.format(idxclster[1], clusters[-3])))                             
            data = dataset.get(idxclster[1],0)

            # Save assignments
            neigh_to_area.append(neigh_to_area_assignment)
            patch_to_neigh.append(patch_to_neigh_assignment[:data.num_nodes,:])            
            patch_to_pheno.append(patch_to_pheno_assignment[:data.num_nodes,:])                        
        except:
            continue

    # Calculate Neighborhoods to areas
    neigh_to_area = np.stack(neigh_to_area) # pat x neigh x areas
    PercTHrsl_area = np.percentile(neigh_to_area,axis=(0,1),q=ClusteringThreshold)
    Area_to_Neigh = np.zeros((clusters[-1],clusters[-2])) 
    for area in range(clusters[-1]):
        Area_to_Neigh[area,:] = np.sum(neigh_to_area[:,:,area]*np.array(neigh_to_area[:,:,area]>PercTHrsl_area[area]),0)

    # Save Neighborhoods to areas heatmap
    plt.close('all')
    plt.figure()
    sns.set(font_scale=1.1)
    row_colors_Area=cm.jet_r(range(0,255,int(255/clusters[2])))[:,:3]
    yticklabels_Area = ['A'+str(i+1) for i in range(clusters[2])]
    col_colors_Neigh=cm.jet_r(range(0,255,int(255/clusters[1])))[:,:3]
    xticklabels_Neigh = ['N'+str(i+1) for i in range(clusters[1])]
    Area_to_Neigh = Area_to_Neigh/Area_to_Neigh.sum(1,keepdims=True)*100    
    Area_to_Neigh[np.isnan(Area_to_Neigh)] = 0
    h_E_Fig = sns.clustermap(Area_to_Neigh.transpose(),col_cluster=True, row_cluster=True, col_colors=row_colors_Area,
                                row_colors=col_colors_Neigh,yticklabels=xticklabels_Neigh,xticklabels=yticklabels_Area, linewidths=0.5, cmap="bwr")            
    h_E_Fig.savefig(dataset.bioInsights_dir_cell_types_Areas + 'heatmap_Neighborhood_composition_of_Areas_Perc_'+str(ClusteringThreshold)+'.png',dpi=600) 
    plt.close('all')
    plt.figure()
    h_E_Fig = sns.clustermap(Area_to_Neigh.transpose(),col_cluster=True, row_cluster=True,vmin=-1, vmax=1, col_colors=row_colors_Area, z_score=1,
                                row_colors=col_colors_Neigh,yticklabels=xticklabels_Neigh,xticklabels=yticklabels_Area, linewidths=0.5, cmap="bwr")            
    h_E_Fig.savefig(dataset.bioInsights_dir_cell_types_Areas + 'heatmap_Neighborhood_composition_of_Areas_Zscore_'+str(ClusteringThreshold)+'.png',dpi=600) 
    df = pd.DataFrame(Area_to_Neigh.transpose(), columns = yticklabels_Area)
    df.index = xticklabels_Neigh
    df.to_excel(dataset.bioInsights_dir_cell_types_Areas + 'heatmap_Neighborhood_composition_of_Areas_Zscore_'+str(ClusteringThreshold)+'.xlsx')  

    # Phenotypes to neighborhoods
    patch_to_neigh = np.concatenate(patch_to_neigh,0) # patches x neigh
    patch_to_pheno = np.concatenate(patch_to_pheno,0) # patches x pheno    
    PercTHrsl_neigh = np.percentile(patch_to_neigh_assignment,axis=0,q=ClusteringThreshold)
    PercTHrsl_pheno = np.percentile(patch_to_pheno,axis=0,q=ClusteringThreshold)        
    for i in range(patch_to_neigh.shape[1]):
        patch_to_neigh[:,i][PercTHrsl_neigh[i]>=patch_to_neigh[:,i]] = 0 
    for i in range(patch_to_pheno.shape[1]):
        patch_to_pheno[:,i][PercTHrsl_pheno[i]>=patch_to_pheno[:,i]] = 0        
    Neigh_to_Pheno = np.matmul(np.transpose(patch_to_neigh),patch_to_pheno)

    # Save heatmap Neigh_to_Pheno
    plt.close('all')
    plt.figure()
    sns.set(font_scale=1.1)
    row_colors_Neigh=cm.jet_r(range(0,255,int(255/clusters[1])))[:,:3]
    yticklabels_Neigh = ['N'+str(i+1) for i in range(clusters[1])]
    col_colors_Pheno=cm.jet_r(range(0,255,int(255/clusters[0])))[:,:3]
    xticklabels_Pheno = ['P'+str(i+1) for i in range(clusters[0])]
    Neigh_to_Pheno = Neigh_to_Pheno/Neigh_to_Pheno.sum(1,keepdims=True)*100
    Neigh_to_Pheno[np.isnan(Neigh_to_Pheno)] = 0
    h_E_Fig = sns.clustermap(Neigh_to_Pheno.transpose(),col_cluster=True, row_cluster=True, col_colors=row_colors_Neigh,
                                row_colors=col_colors_Pheno,yticklabels=xticklabels_Pheno,xticklabels=yticklabels_Neigh, linewidths=0.5, cmap="bwr")            
    h_E_Fig.savefig(dataset.bioInsights_dir_cell_types + 'Neighborhoods/heatmap_Phenotype_composition_of_neighborhoods_Perc_Thrs{}.png'.format(str(ClusteringThreshold)),dpi=600) 
    plt.close('all')
    plt.figure()
    Neigh_to_Pheno[Neigh_to_Pheno==0] = np.random.rand()*1e-3
    h_E_Fig = sns.clustermap(Neigh_to_Pheno.transpose(),col_cluster=True, row_cluster=True,vmin=-1, vmax=1, col_colors=row_colors_Neigh, z_score=1,
                                row_colors=col_colors_Pheno,yticklabels=xticklabels_Pheno,xticklabels=yticklabels_Neigh, linewidths=0.5, cmap="bwr")            
    h_E_Fig.savefig(dataset.bioInsights_dir_cell_types + 'Neighborhoods/heatmap_Phenotype_composition_of_neighborhoods_Zscore_Thrs{}.png'.format(str(ClusteringThreshold)),dpi=600) 
    df = pd.DataFrame(Neigh_to_Pheno.transpose(), columns = yticklabels_Neigh)
    df.index = xticklabels_Pheno
    df.to_excel(dataset.bioInsights_dir_cell_types + 'Neighborhoods/heatmap_Phenotype_composition_of_neighborhoods_Perc_Thrs{}.xlsx'.format(str(ClusteringThreshold)))  


    
