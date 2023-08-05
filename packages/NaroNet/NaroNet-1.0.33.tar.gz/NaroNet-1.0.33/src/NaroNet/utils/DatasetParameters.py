
import argparse
import numpy as np
from hyperopt import hp
import torch

def parameters(path, debug):

    # args=DefaultParameters(path)
    args={}
    args['path'] = path

    # Use optimized parameters depending on the experiment.
    if 'STK11' in path:            
        
        # Patch contrastive learning parameters
        args['PCL_CNN_Architecture']='resnet50' # Architecture of the CNN. Choose between resnet50 or resnet18. resnet50 is slow but is capable of learning more complex patterns. resnet18 is faster but learns simpler patterns. So far we have used resnet50.
        args['PCL_Learning_Rate']= 0.0003 # Learning Rate used to train the CNN. Do not change this value.
        args['PCL_Weight_Decay']= 1e-4 # Weight Decay used to train the CNN. Do not change this value.
        args['PCL_Temperature']= 0.07 # Softmax temperature used to train the CNN. Do not change this value.
        args['PCL_GPU_INDEX']= torch.device('cuda:0') # Specify the GPU where the training is carried out.
        args['PCL_Epochs']=400 # Number of epochs to run PCL. Increase the numnber so that PCL achieves at least a 85% of top1 accuracy.
        args['PCL_N_Workers']=1 # Number of workers used to parallelize data loading. A higher number of workers will result in a faster execution but will require more RAM memory usage. 
        args['PCL_N_Crops_per_Image']=300 # Number of image crops used to train the model in each iteration. Higher number of crops will learn more features from patches from one image but requires more RAM and GPU memory usage.
        args['PCL_Patch_Size']=30 # Size of image patch (in pixels). We saw best performance when the patch embeds 1 to 3 cells.
        args['PCL_Stride']=0 # Size of stride between consecutive patches. Do not use it. It is not yet implemented. :(
        args['PCL_Alpha_L']=1.15 # Size ratio between image crop and image patch. Check paper for better explanation.
        args['PCL_Z_Score']= True # Whether to apply z_score per channel/marker. Seen better performance when using it. 
        args['PCL_Batch_Size']= 4 # Number of images used per iteration. A higher batch size results in learning more features and doing it in a more stable way but will require more RAM and GPU memory usage.    
        args['PCL_Out_Dimensions']= 128 # Feature dimensions of the output image patch. A higher value results in more learned features but requires more RAM and GPU memory usage.
        args['PCL_eliminate_Black_Background'] = True # Whether to eliminate from the training the black background. Use it for Multiplex fluorescence images.
        args['PCL_eliminate_White_Background'] = False # Whether to eliminate from the training the whit background. Use it for H&E white-field microscopy images.        
        args['PCL_Color_perturbation_Augmentation'] = False # Whether to use color normalization augmentation in H&E white-field microscopy images. Used to force PCL to learn morphological features and avoid learning color staining features. 

        # Name of the columnn from Image_Labels.xslx used to differentiate subject types.
        args['experiment_Label'] = ['Unsupervised'] 

        # General parameters used for Machine Learning
        args['NaroNet_n_workers'] = 1 # Number of workers used to parallelize data loading. A higher number of workers will result in a faster execution but will require more RAM memory usage. 
        args['epochs'] = 3 # Number of epochs to run PCL. Increase the number so that all function losses find a plateau without overfitting
        args['weight_decay'] = 0 # Weight Decay used to train the CNN. Do not change this value.
        args['batch_size'] = 12 # Number of subjects used per iteration. A higher batch size results in learning more features and doing it in a more stable way but will require more RAM and GPU memory usage.    
        args['lr'] = 0.001 # Learning Rate used to train the CNN. Do not change this value.
        args['dropoutRate'] = 0 # Dropout rate 
        args['training_MODE'] = 'TrainALL' # Train mode selection. 'TrainALL' uses 100% of the data to train (no validation). 'CrossValidation' divides data in k-folds to obtain generability of the model.
        args['folds'] = 1 # Number of folds used in the cross-validation training/testing mode. Check https://machinelearningmastery.com/k-fold-cross-validation/ for more info. 
        args['device'] = 'cuda:0' # Specify the GPU where the training is carried out.
        args['Batch_Normalization'] = True # Whether to apply batch normalization just before patch assignment. Do not change this value. If False it will not work.
        args['dataAugmentationPerc'] = 0 # Artificially augment subjects in each iteration. Value specifies percentage of nodes of the graph changed where 1 stands for 100% and 0 implies no data augmentation used.
            
        # NaroNet specific parameters
        args['N_Phenotypes'] = 8 # Number of local phenotypes. Use low values when you want to find only 2 or 3 relevant phenotypes. Use larger values to find multiple relevant phenotypes.
        args['N_Neighborhoods'] = 12 # Number of cellular neighborhoods. Use low values when you want to find only 2 or 3 relevant neighborhoods. Use larger values to find multiple relevant neighborhoods.
        args['N_Areas'] = 4 # Number of tissue areas. Use low values when you want to find only 2 or 3 ares. Use larger values to find multiple relevant areas.     
        args['n_hops_neighborhoods'] = 1 # Number of hops used to learn neighborhoods using GNNs. Do not change this value.
        args['Phenotype_Learning'] = True # Whether to learn phenotypes or not  
        args['Neighborhood_Learning'] = True # Whether to learn neighborhoods or not
        args['Area_Learning'] = True # Whether to learn areas or not        
        args['attntnThreshold'] = 0 # Attention threshold for patch assignment. Patches with a confidence value below this are not considered for subject prediction
        args['1Patch1Cluster'] = False # Whether to let patches be from several TMEs at the same time or not.
        
        # Losses
        args['ContrastACC_Pheno'] = 1000 # Relevance of contrast accuracy loss for phenotypes
        args['ContrastACC_Neigh'] = 1000 # Relevance of contrast accuracy loss for neighborhoods
        args['ContrastACC_Area'] = 0 # Relevance of contrast accuracy loss for areas
        args['PatchEntropy_Pheno'] = 0 # Relevance of contrast accuracy loss for areas
        args['PatchEntropy_Neigh'] = 0#1 if debug=='Index' else hp.choice("PatchEntropy_Neigh", [1,0.1,0.01,0.001,0.0001,0]) if debug=='Object' else 0.1
        args['PatchEntropy_Area'] = 1#4 if debug=='Index' else hp.choice("PatchEntropy_Area", [1,0.1,0.01,0.001,0.0001,0]) if debug=='Object' else 0.0001                                             

        # Bioinsights parameters
        args['Bio_save_Orig_im'] = False
        args['Perc_high_conf_patches'] = 0.0001 # 1 is 100%. Great values generates phenotypes and neighborhoods with many patches. A low values generates rare populations.                                  
        args['TSNE_Perc_Pat'] = 0.5 # Percentage of patients to use to generate the tsne.     


    elif 'Melanoma_ProgressionvsBaseline' in path:            
        # Patch contrastive learning parameters
        args['PCL_CNN_Architecture']='resnet50' # or resnet18
        args['PCL_N_Workers']=2 # Number of data loading workers 
        args['PCL_Epochs']=300 # Number of total epoch to run
        args['PCL_N_Crops_per_Image']=300 # Number of crops chosen per image
        args['PCL_Patch_Size']=50 # Size of patches in pixels
        args['PCL_Stride']=0 # Size of stride between consecutive patches
        args['PCL_Alpha_L']=1.15 # size ratio between image crop and image patch
        args['PCL_Z_Score']= True # Whether to apply z score per channel/marker 
        args['PCL_Batch_Size']= 6 # Number of images per iteration
        args['PCL_Weight_Decay']= 1e-4 # Weight Decay
        args['PCL_Out_Dimensions']= 128 # Feature dimensions of patch
        args['PCL_Learning_Rate']= 0.0003 # Learning Rate
        args['PCL_Temperature']= 0.07 # Softmax temperature                
        args['PCL_eliminate_Black_Background'] = False
        args['PCL_eliminate_White_Background'] = True   
        args['PCL_GPU_INDEX']= torch.device('cuda:0') # GPU where the training is carried out 
        args['PCL_Color_perturbation_Augmentation'] = True # Color augmentation for H&E tissue staining.

        # Label you want to infer with respect the images.
        args['experiment_Label'] = ['Sample_Type'] 

        # Architecture Search parameters
        args['num_samples_architecture_search'] = 700  

        # Optimization Parameters
        args['NaroNet_n_workers'] = 1 # Number of data loading workers
        args['epochs'] = 400# if debug else hp.quniform('epochs', 5, 25, 1)
        args['lr_decay_factor'] = 0.1# if debug else hp.uniform('lr_decay_factor', 0, 0.75)
        args['lr_decay_step_size'] = 10000#max(int(args['epochs']/3),1)# if debug else hp.quniform('lr_decay_step_size', 2, 20, 1)        
        args['weight_decay'] = 0#3 if debug=='Index' else hp.choice('weight_decay',[0.1,0.01,0.001,0.0001,0]) if debug=='Object' else 0.0001
        args['batch_size'] = 4 if debug=='Index' else hp.choice('batch_size', [2, 4, 8, 16, 32]) if debug=='Object' else 32
        args['lr'] = 2 if debug=='Index' else hp.choice('lr', [1,0.1,0.01,0.001,0.0001]) if debug=='Object' else 0.01

        # General        
        args['training_MODE'] = 'TrainALL' # TrainALL, NestedCrossValidation, CrossValidation # Whether to use nested cross validation or cross validation.            
        args['folds'] = 1
        args['device'] = 'cuda:0'
        args['Batch_Normalization'] = True
        args['dataAugmentationPerc'] = 0 #0 if debug=='Index' else hp.choice("dataAugmentationPerc", [0,0.0001,0.001]) if debug=='Object' else 0  

        # Neural Network
        args['N_Phenotypes'] = 1 if debug=='Index' else hp.choice('clusters1',[5,8,15,20]) if debug=='Object' else 8     
        args['N_Neighborhoods'] = 2 if debug=='Index' else hp.choice('clusters2',[6,11,12,21]) if debug=='Object' else 12
        args['N_Areas'] = 1 if debug=='Index' else hp.choice('clusters3',[2,6,7]) if debug=='Object' else 6      
        args['Phenotype_Learning'] = True  
        args['Neighborhood_Learning'] = True  
        args['Area_Learning'] = True
        args['dropoutRate'] = 0# 1 if debug=='Index' else hp.choice('dropoutRate', [0.1, 0.2, 0.3,0.4]) if debug=='Object' else 0.2        
        args['attntnThreshold'] = 0# if debug=='Index' else hp.choice('attntnThreshold', [0,.2,.4,.6,.8]) if debug=='Object' else 0  
        args['1Patch1Cluster'] = True# if debug=='Index' else hp.choice('attntnThreshold', [0,.2,.4,.6,.8]) if debug=='Object' else 0  

        # Losses 
        args['ContrastACC_Pheno'] = 100#.001#4 if debug=='Index' else hp.choice("orthoColor_Lambda0", [1,0.1,0.01,0.001,0.0001,0.00001]) if debug=='Object' else 0.0001                                
        args['ContrastACC_Neigh'] = 100#.001#4 if debug=='Index' else hp.choice("orthoColor_Lambda1", [1, 0.1,0.01,0.001,0.0001,0.00001]) if debug=='Object' else 0.0001                                              
        args['ContrastACC_Area'] = 100#.0001#4 if debug=='Index' else hp.choice("orthoColor_Lambda1", [1, 0.1,0.01,0.001,0.0001,0.00001]) if debug=='Object' else 0.0001            
        args['Perc_high_conf_patches'] = 0.001 # 1 is 100%. Great values generates phenotypes and neighborhoods with many patches. A low values generates rare populations.                                  
        args['PatchEntropy_Pheno'] = 0#.01#3 if debug=='Index' else hp.choice("min_Cell_entropy_Lambda0", [1,0.1,0.01,0.001,0]) if debug=='Object' else 0.001   
        args['PatchEntropy_Neigh'] = 0#.01#4 if debug=='Index' else hp.choice("min_Cell_entropy_Lambda1", [1,0.1,0.01,0.001,0]) if debug=='Object' else 0
        args['PatchEntropy_Area'] = 0#.0001#1 if debug=='Index' else hp.choice("min_Cell_entropy_Lambda2", [1,0.1,0.01,0.001,0]) if debug=='Object' else 0.1                                  

        # Bioinsights parameters
        args['Bio_save_Orig_im'] = False
        args['TSNE_Perc_Pat'] = 0.33 # Percentage of patients to use to generate the tsne. 


    elif 'LF_Recurrence' in path:            
        # Patch contrastive learning parameters
        args['PCL_CNN_Architecture']='resnet50' # or resnet18
        args['PCL_N_Workers']=8 # Number of data loading workers 
        args['PCL_Epochs']=400 # Number of total epoch to run
        args['PCL_N_Crops_per_Image']=70 # Number of crops chosen per image
        args['PCL_Patch_Size']=30 # Size of patches in pixels
        args['PCL_Stride']=0 # Size of stride between consecutive patches
        args['PCL_Alpha_L']=1.1 # size ratio between image crop and image patch
        args['PCL_Z_Score']= True # Whether to apply z score per channel/marker 
        args['PCL_Batch_Size']= 8 # Number of images per iteration
        args['PCL_Weight_Decay']= 1e-4 # Weight Decay
        args['PCL_Out_Dimensions']= 128 # Feature dimensions of patch
        args['PCL_Learning_Rate']= 0.0003 # Learning Rate
        args['PCL_Temperature']= 0.07 # Softmax temperature    
        args['PCL_eliminate_Black_Background'] = True
        args['PCL_eliminate_White_Background'] = False
        args['PCL_GPU_INDEX']= torch.device('cuda:0') # GPU where the training is carried out 
        args['PCL_Color_perturbation_Augmentation'] = False # Color augmentation for H&E tissue staining.

        # Label you want to infer with respect the images.
        args['experiment_Label'] = ['Relapse'] 

        # Architecture Search parameters
        args['num_samples_architecture_search'] = 700  

        # Optimization Parameters
        args['NaroNet_n_workers'] = 1
        args['epochs'] = 200# if debug else hp.quniform('epochs', 5, 25, 1)
        args['lr_decay_factor'] = 0.1# if debug else hp.uniform('lr_decay_factor', 0, 0.75)
        args['lr_decay_step_size'] = 309#max(int(args['epochs']/3),1)# if debug else hp.quniform('lr_decay_step_size', 2, 20, 1)        
        args['weight_decay'] = 0#3 if debug=='Index' else hp.choice('weight_decay',[0.1,0.01,0.001,0.0001,0]) if debug=='Object' else 0.0001
        args['batch_size'] = 4 if debug=='Index' else hp.choice('batch_size', [2, 4, 8, 12, 28]) if debug=='Object' else 28
        args['lr'] = 1 if debug=='Index' else hp.choice('lr', [1,0.1,0.01,0.001,0.0001]) if debug=='Object' else 0.1

        # General        
        args['training_MODE'] = 'TrainALL' # TrainALL, NestedCrossValidation, CrossValidation # Whether to use nested cross validation or cross validation.            
        args['folds'] = 1
        args['device'] = 'cuda:0'
        args['Batch_Normalization'] = True
        args['dataAugmentationPerc'] = 0 #0 if debug=='Index' else hp.choice("dataAugmentationPerc", [0,0.0001,0.001]) if debug=='Object' else 0  

        # Neural Network
        args['N_Phenotypes'] = 1 if debug=='Index' else hp.choice('clusters1',[5,8,15,20]) if debug=='Object' else 8     
        args['N_Neighborhoods'] = 2 if debug=='Index' else hp.choice('clusters2',[6,11,16,21]) if debug=='Object' else 16 
        args['N_Areas'] = 1 if debug=='Index' else hp.choice('clusters3',[2,4,7]) if debug=='Object' else 4      
        args['Phenotype_Learning'] = True  
        args['Neighborhood_Learning'] = False  
        args['Area_Learning'] = False
        args['dropoutRate'] = 0# 1 if debug=='Index' else hp.choice('dropoutRate', [0.1, 0.2, 0.3,0.4]) if debug=='Object' else 0.2        
        args['attntnThreshold'] = 0# if debug=='Index' else hp.choice('attntnThreshold', [0,.2,.4,.6,.8]) if debug=='Object' else 0  
        args['1Patch1Cluster'] = False# if debug=='Index' else hp.choice('attntnThreshold', [0,.2,.4,.6,.8]) if debug=='Object' else 0  

        # Losses 
        args['ContrastACC_Pheno'] = 1000#.001#4 if debug=='Index' else hp.choice("orthoColor_Lambda0", [1,0.1,0.01,0.001,0.0001,0.00001]) if debug=='Object' else 0.0001                                
        args['ContrastACC_Neigh'] = 0#.001#4 if debug=='Index' else hp.choice("orthoColor_Lambda1", [1, 0.1,0.01,0.001,0.0001,0.00001]) if debug=='Object' else 0.0001                                              
        args['ContrastACC_Area'] = 0#.0001#4 if debug=='Index' else hp.choice("orthoColor_Lambda1", [1, 0.1,0.01,0.001,0.0001,0.00001]) if debug=='Object' else 0.0001                                              
        args['PatchEntropy_Pheno'] = 0#.01#3 if debug=='Index' else hp.choice("min_Cell_entropy_Lambda0", [1,0.1,0.01,0.001,0]) if debug=='Object' else 0.001   
        args['PatchEntropy_Neigh'] = 0#.01#4 if debug=='Index' else hp.choice("min_Cell_entropy_Lambda1", [1,0.1,0.01,0.001,0]) if debug=='Object' else 0
        args['PatchEntropy_Area'] = 0#.0001#1 if debug=='Index' else hp.choice("min_Cell_entropy_Lambda2", [1,0.1,0.01,0.001,0]) if debug=='Object' else 0.1                                  

        # Bioinsights parameters
        args['Bio_save_Orig_im'] = False
        args['TSNE_Perc_Pat'] = 0.5 # Percentage of patients to use to generate the tsne. 


    elif 'LF_19H' in path:            
        # Patch contrastive learning parameters
        args['PCL_CNN_Architecture']='resnet50' # or resnet18
        args['PCL_N_Workers']=0 # Number of data loading workers 
        args['PCL_Epochs']=400 # Number of total epoch to run
        args['PCL_N_Crops_per_Image']=200 # Number of crops chosen per image
        args['PCL_Patch_Size']=30 # Size of patches in pixels
        args['PCL_Stride']=0 # Size of stride between consecutive patches
        args['PCL_Alpha_L']=1.15 # size ratio between image crop and image patch
        args['PCL_Z_Score']= True # Whether to apply z score per channel/marker 
        args['PCL_Batch_Size']= 6 # Number of images per iteration
        args['PCL_Weight_Decay']= 1e-4 # Weight Decay
        args['PCL_Out_Dimensions']= 128 # Feature dimensions of patch
        args['PCL_Learning_Rate']= 0.0003 # Learning Rate
        args['PCL_Temperature']= 0.07 # Softmax temperature         
        args['PCL_eliminate_Black_Background'] = True
        args['PCL_eliminate_White_Background'] = False       
        args['PCL_GPU_INDEX']= torch.device('cuda:0') # GPU where the training is carried out 
        args['PCL_Color_perturbation_Augmentation'] = False # Color augmentation for H&E tissue staining.

        # Label you want to infer with respect the images.
        args['experiment_Label'] = ['Relapse'] 

        # Architecture Search parameters
        args['num_samples_architecture_search'] = 700  

        # Optimization Parameters
        args['epochs'] = 8# if debug else hp.quniform('epochs', 5, 25, 1)
        args['lr_decay_factor'] = 0.1# if debug else hp.uniform('lr_decay_factor', 0, 0.75)
        args['lr_decay_step_size'] = 10000#max(int(args['epochs']/3),1)# if debug else hp.quniform('lr_decay_step_size', 2, 20, 1)        
        args['weight_decay'] = 0#3 if debug=='Index' else hp.choice('weight_decay',[0.1,0.01,0.001,0.0001,0]) if debug=='Object' else 0.0001
        args['batch_size'] = 26# if debug=='Index' else hp.choice('batch_size', [2, 4, 8, 16, 22]) if debug=='Object' else 22
        args['lr'] = 0.1#0 if debug=='Index' else hp.choice('lr', [1,0.1,0.01]) if debug=='Object' else 1

        # General        
        args['training_MODE'] = 'TrainALL' # TrainALL, NestedCrossValidation, CrossValidation # Whether to use nested cross validation or cross validation.            
        args['folds'] = 1
        args['device'] = 'cuda:0'
        args['Batch_Normalization'] = True
        args['dataAugmentationPerc'] = 0 #0 if debug=='Index' else hp.choice("dataAugmentationPerc", [0,0.0001,0.001]) if debug=='Object' else 0  

        # Neural Network
        args['N_Phenotypes'] = 1 if debug=='Index' else hp.choice('clusters1',[5,8,15,20]) if debug=='Object' else 8     
        args['N_Neighborhoods'] = 2 if debug=='Index' else hp.choice('clusters2',[6,11,16,21]) if debug=='Object' else 16 
        args['N_Areas'] = 1 if debug=='Index' else hp.choice('clusters3',[2,4,7]) if debug=='Object' else 4      
        args['Phenotype_Learning'] = True  
        args['Neighborhood_Learning'] = True  
        args['Area_Learning'] = True
        args['dropoutRate'] = 0# 1 if debug=='Index' else hp.choice('dropoutRate', [0.1, 0.2, 0.3,0.4]) if debug=='Object' else 0.2        
        args['attntnThreshold'] = 0# if debug=='Index' else hp.choice('attntnThreshold', [0,.2,.4,.6,.8]) if debug=='Object' else 0  
        args['1Patch1Cluster'] = False# if debug=='Index' else hp.choice('attntnThreshold', [0,.2,.4,.6,.8]) if debug=='Object' else 0  


        # Losses
        args['ContrastACC_Pheno'] = 1#.001#4 if debug=='Index' else hp.choice("orthoColor_Lambda0", [1,0.1,0.01,0.001,0.0001,0.00001]) if debug=='Object' else 0.0001                                
        args['ContrastACC_Neigh'] = 1#.001#4 if debug=='Index' else hp.choice("orthoColor_Lambda1", [1, 0.1,0.01,0.001,0.0001,0.00001]) if debug=='Object' else 0.0001                                              
        args['ContrastACC_Area'] = 1#.0001#4 if debug=='Index' else hp.choice("orthoColor_Lambda1", [1, 0.1,0.01,0.001,0.0001,0.00001]) if debug=='Object' else 0.0001                                              
        args['PatchEntropy_Pheno'] = 0#.01#3 if debug=='Index' else hp.choice("min_Cell_entropy_Lambda0", [1,0.1,0.01,0.001,0]) if debug=='Object' else 0.001   
        args['PatchEntropy_Neigh'] = 0#.01#4 if debug=='Index' else hp.choice("min_Cell_entropy_Lambda1", [1,0.1,0.01,0.001,0]) if debug=='Object' else 0
        args['PatchEntropy_Area'] = 0#.0001#1 if debug=='Index' else hp.choice("min_Cell_entropy_Lambda2", [1,0.1,0.01,0.001,0]) if debug=='Object' else 0.1                                  

        # Bioinsights parameters
        args['Bio_save_Orig_im'] = False

    elif 'Urothelial_ClinBen' in path:            
        
        # Patch contrastive learning parameters
        args['PCL_CNN_Architecture']='resnet50' # or resnet18
        args['PCL_N_Workers']=8 # Number of data loading workers 
        args['PCL_Epochs']=80 # Number of total epoch to run
        args['PCL_N_Crops_per_Image']=40 # Number of crops chosen per image
        args['PCL_Patch_Size']=30 # Size of patches in pixels
        args['PCL_Stride']=0 # Size of stride between consecutive patches
        args['PCL_Alpha_L']=1.15 # size ratio between image crop and image patch
        args['PCL_Z_Score']= True # Whether to apply z score per channel/marker
        args['PCL_Batch_Size']= 8 # Number of images per iteration
        args['PCL_Weight_Decay']= 1e-4 # Weight Decay
        args['PCL_Out_Dimensions']= 128 # Feature dimensions of patch
        args['PCL_Learning_Rate']= 0.0003 # Learning Rate
        args['PCL_Temperature']= 0.07 # Softmax temperature    
        args['PCL_eliminate_Black_Background'] = True 
        args['PCL_eliminate_White_Background'] = False            
        args['PCL_Color_perturbation_Augmentation'] = False # Whether to use color normalization augmentation in H&E white-field microscopy images. Used to force PCL to learn morphological features and avoid learning color staining features. 
        args['PCL_GPU_INDEX']= torch.device('cuda:0') # GPU where the training is carried out 

        # Label you want to infer with respect the images.
        args['experiment_Label'] = ['Clinical_Benefit'] 

        # Architecture Search parameters
        args['num_samples_architecture_search'] = 1500  

        # Optimization Parameters
        args['NaroNet_n_workers'] = 1
        args['epochs'] = 1000# if debug else hp.quniform('epochs', 5, 25, 1)
        args['lr_decay_factor'] = 0.1# if debug else hp.uniform('lr_decay_factor', 0, 0.75)
        args['lr_decay_step_size'] = 10000#max(int(args['epochs']/5),1)# if debug else hp.quniform('lr_decay_step_size', 2, 20, 1)        
        args['weight_decay'] = 4 if debug=='Index' else hp.choice('weight_decay',[0.1,0.01,0.001,0.0001,0]) if debug=='Object' else 0
        args['batch_size'] = 3 if debug=='Index' else hp.choice('batch_size', [2, 4, 8, 24]) if debug=='Object' else 24
        args['lr'] = 3 if debug=='Index' else hp.choice('lr', [1,0.1,0.01,0.001,0.001]) if debug=='Object' else 0.001

        # General
        args['training_MODE'] = 'TrainALL' # TrainALL, NestedCrossValidation, CrossValidation # Whether to use nested cross validation or cross validation.        
        args['folds'] = 1
        args['device'] = 'cuda:0'
        args['Batch_Normalization'] = True
        args['dataAugmentationPerc'] = 0 #0 if debug=='Index' else hp.choice("dataAugmentationPerc", [0,0.0001,0.001]) if debug=='Object' else 0  

        # Neural Network
        args['N_Phenotypes'] = 6#2 if debug=='Index' else hp.choice('clusters1',[5,10,15,20]) if debug=='Object' else 15     
        args['N_Neighborhoods'] = 8#1 if debug=='Index' else hp.choice('clusters2',[6,11,16,21]) if debug=='Object' else 11 
        args['N_Areas'] = 4#0 if debug=='Index' else hp.choice('clusters3',[2,4,7]) if debug=='Object' else 2      
        args['n_hops_neighborhoods'] = 2 
        args['Phenotype_Learning'] = True  
        args['Neighborhood_Learning'] = False
        args['Area_Learning'] = False
        args['dropoutRate'] = 0# 1 if debug=='Index' else hp.choice('dropoutRate', [0.1, 0.2, 0.3,0.4]) if debug=='Object' else 0.2        
        args['attntnThreshold'] = 0# if debug=='Index' else hp.choice('attntnThreshold', [0,.2,.4,.6,.8]) if debug=='Object' else 0  
        args['1Patch1Cluster'] = False# if debug=='Index' else hp.choice('attntnThreshold', [0,.2,.4,.6,.8]) if debug=='Object' else 0  
                
        # Losses
        args['ContrastACC_Pheno'] = 1# 4 if debug=='Index' else hp.choice("orthoColor_Lambda0", [1,0.1,0.01,0.001,0.0001,0.00001]) if debug=='Object' else 0.0001                                
        args['ContrastACC_Neigh'] = 0 # 4 if debug=='Index' else hp.choice("orthoColor_Lambda1", [1, 0.1,0.01,0.001,0.0001,0.00001]) if debug=='Object' else 0.0001                                              
        args['ContrastACC_Area'] = 0#4 if debug=='Index' else hp.choice("orthoColor_Lambda1", [1, 0.1,0.01,0.001,0.0001,0.00001]) if debug=='Object' else 0.0001 
        args['Perc_high_conf_patches'] = 0.1 # 1 is 100%. Great values generates phenotypes and neighborhoods with many patches. Low values generate rare populations.
        args['PatchEntropy_Pheno'] = 0#3 if debug=='Index' else hp.choice("min_Cell_entropy_Lambda0", [1,0.1,0.01,0.001,0]) if debug=='Object' else 0.001   
        args['PatchEntropy_Neigh'] = 0#4 if debug=='Index' else hp.choice("min_Cell_entropy_Lambda1", [1,0.1,0.01,0.001,0]) if debug=='Object' else 0
        args['PatchEntropy_Area'] = 0#1 if debug=='Index' else hp.choice("min_Cell_entropy_Lambda2", [1,0.1,0.01,0.001,0]) if debug=='Object' else 0.1          
        
        # Bioinsights parameters
        args['Bio_save_Orig_im'] = True
        args['TSNE_Perc_Pat'] = 0 # Percentage of patients used to calculate TSNE. 1 is 100% of patients
        args['Pheno_Perc_Pat'] = 1 # Percentage of patients used to calculate TSNE. 1 is 100% of patients
        args['Pheno_Excluded_from_analysis'] = [] # Percentage of patients used to calculate TSNE. 1 is 100% of patients
        args['Neigh_Excluded_from_analysis'] = [] # Percentage of patients used to calculate TSNE. 1 is 100% of patients


    elif 'Endometrial_Survival' in path:            
        
        # Patch contrastive learning parameters
        args['PCL_CNN_Architecture']='resnet50' # or resnet18
        args['PCL_N_Workers']=8 # Number of data loading workers 
        args['PCL_Epochs']=500 # Number of total epoch to run
        args['PCL_N_Crops_per_Image']=30 # Number of crops chosen per image
        args['PCL_Patch_Size']=30 # Size of patches in pixels
        args['PCL_Stride']=0 # Size of stride between consecutive patches
        args['PCL_Alpha_L']=1.15 # size ratio between image crop and image patch
        args['PCL_Z_Score']= True # Whether to apply z score per channel/marker
        args['PCL_Batch_Size']= 40 # Number of images per iteration
        args['PCL_Weight_Decay']= 1e-4 # Weight Decay
        args['PCL_Out_Dimensions']= 128 # Feature dimensions of patch
        args['PCL_Learning_Rate']= 0.0003 # Learning Rate
        args['PCL_Temperature']= 0.07 # Softmax temperature    
        args['PCL_eliminate_Black_Background'] = True 
        args['PCL_eliminate_White_Background'] = False        
        args['PCL_Color_perturbation_Augmentation'] = False # Whether to use color normalization augmentation in H&E white-field microscopy images. Used to force PCL to learn morphological features and avoid learning color staining features. 
        args['PCL_GPU_INDEX']= torch.device('cuda:0') # GPU where the training is carried out 

        # Label you want to infer with respect the images.
        args['experiment_Label'] = ['POLE Mutation'] 

        # Architecture Search parameters
        args['num_samples_architecture_search'] = 1500  

        # Optimization Parameters
        args['NaroNet_n_workers'] = 1
        args['epochs'] = 75# if debug else hp.quniform('epochs', 5, 25, 1)
        args['lr_decay_factor'] = 0.1# if debug else hp.uniform('lr_decay_factor', 0, 0.75)
        args['lr_decay_step_size'] = 10000#max(int(args['epochs']/5),1)# if debug else hp.quniform('lr_decay_step_size', 2, 20, 1)        
        args['weight_decay'] = 4 if debug=='Index' else hp.choice('weight_decay',[0.1,0.01,0.001,0.0001,0]) if debug=='Object' else 0
        args['batch_size'] = 3 if debug=='Index' else hp.choice('batch_size', [2, 4, 8, 64]) if debug=='Object' else 64
        args['lr'] = 1 if debug=='Index' else hp.choice('lr', [1,0.1,0.01,0.001,0.0001]) if debug=='Object' else 0.001

        # General
        args['training_MODE'] = 'CrossValidation' # TrainALL, NestedCrossValidation, CrossValidation # Whether to use nested cross validation or cross validation.        
        args['folds'] = 12
        args['device'] = 'cuda:0'
        args['Batch_Normalization'] = True
        args['dataAugmentationPerc'] = 0 #0 if debug=='Index' else hp.choice("dataAugmentationPerc", [0,0.0001,0.001]) if debug=='Object' else 0  

        # Neural Network
        args['N_Phenotypes'] = 6#2 if debug=='Index' else hp.choice('clusters1',[5,10,15,20]) if debug=='Object' else 15     
        args['N_Neighborhoods'] = 8#1 if debug=='Index' else hp.choice('clusters2',[6,11,16,21]) if debug=='Object' else 11 
        args['N_Areas'] = 4#0 if debug=='Index' else hp.choice('clusters3',[2,4,7]) if debug=='Object' else 2      
        args['n_hops_neighborhoods'] = 3
        args['Phenotype_Learning'] = True  
        args['Neighborhood_Learning'] = True
        args['Area_Learning'] = True
        args['dropoutRate'] = 0# 1 if debug=='Index' else hp.choice('dropoutRate', [0.1, 0.2, 0.3,0.4]) if debug=='Object' else 0.2        
        args['attntnThreshold'] = 0# if debug=='Index' else hp.choice('attntnThreshold', [0,.2,.4,.6,.8]) if debug=='Object' else 0  
        args['1Patch1Cluster'] = False# if debug=='Index' else hp.choice('attntnThreshold', [0,.2,.4,.6,.8]) if debug=='Object' else 0  
                
        # Losses
        args['ContrastACC_Pheno'] = 0#4 if debug=='Index' else hp.choice("orthoColor_Lambda0", [1,0.1,0.01,0.001,0.0001,0.00001]) if debug=='Object' else 0.0001                                
        args['ContrastACC_Neigh'] = 0#4 if debug=='Index' else hp.choice("orthoColor_Lambda1", [1, 0.1,0.01,0.001,0.0001,0.00001]) if debug=='Object' else 0.0001                                              
        args['ContrastACC_Area'] = 0#4 if debug=='Index' else hp.choice("orthoColor_Lambda1", [1, 0.1,0.01,0.001,0.0001,0.00001]) if debug=='Object' else 0.0001 
        args['Perc_high_conf_patches'] = 0.0001 # 1 is 100%. Great values generates phenotypes and neighborhoods with many patches. Low values generate rare populations.
        args['PatchEntropy_Pheno'] = 0.001#3 if debug=='Index' else hp.choice("min_Cell_entropy_Lambda0", [1,0.1,0.01,0.001,0]) if debug=='Object' else 0.001   
        args['PatchEntropy_Neigh'] = 0.001#4 if debug=='Index' else hp.choice("min_Cell_entropy_Lambda1", [1,0.1,0.01,0.001,0]) if debug=='Object' else 0
        args['PatchEntropy_Area'] = 0.001#1 if debug=='Index' else hp.choice("min_Cell_entropy_Lambda2", [1,0.1,0.01,0.001,0]) if debug=='Object' else 0.1          
        
        # Bioinsights parameters
        args['Bio_save_Orig_im'] = True
        args['TSNE_Perc_Pat'] = 1 # Percentage of patients to use to generate the tsne. 

    elif 'Tumor_subtype' in path:            
        
        # Patch contrastive learning parameters
        args['PCL_CNN_Architecture']='resnet50' # or resnet18
        args['PCL_N_Workers']=8 # Number of data loading workers 
        args['PCL_Epochs']=80 # Number of total epoch to run
        args['PCL_N_Crops_per_Image']=40 # Number of crops chosen per image
        args['PCL_Patch_Size']=30 # Size of patches in pixels
        args['PCL_Stride']=0 # Size of stride between consecutive patches
        args['PCL_Alpha_L']=1.15 # size ratio between image crop and image patch
        args['PCL_Z_Score']= True # Whether to apply z score per channel/marker
        args['PCL_Batch_Size']= 8 # Number of images per iteration
        args['PCL_Weight_Decay']= 1e-4 # Weight Decay
        args['PCL_Out_Dimensions']= 128 # Feature dimensions of patch
        args['PCL_Learning_Rate']= 0.003 # Learning Rate
        args['PCL_Temperature']= 0.07 # Softmax temperature                
        args['PCL_eliminate_Black_Background'] = False
        args['PCL_eliminate_White_Background'] = False
        args['PCL_GPU_INDEX']= torch.device('cuda:0') # GPU where the training is carried out 

        # Label you want to infer with respect the images.
        args['experiment_Label'] = ['Clinical_Benefit'] 

        # Architecture Search parameters
        args['num_samples_architecture_search'] = 1500  

        # Optimization Parameters
        args['epochs'] = 500
        args['lr_decay_factor'] = 0.1
        args['lr_decay_step_size'] = 10000
        args['weight_decay'] = 0
        args['batch_size'] = 24
        args['lr'] = 1 

        # General
        args['training_MODE'] = 'TrainALL' # TrainALL, NestedCrossValidation, CrossValidation # Whether to use nested cross validation or cross validation.        
        args['folds'] = 1
        args['device'] = 'cuda:0'
        args['Batch_Normalization'] = True
        args['dataAugmentationPerc'] = 0 #0 if debug=='Index' else hp.choice("dataAugmentationPerc", [0,0.0001,0.001]) if debug=='Object' else 0  

        # Neural Network
        args['N_Phenotypes'] = 8#2 if debug=='Index' else hp.choice('clusters1',[5,10,15,20]) if debug=='Object' else 15     
        args['N_Neighborhoods'] = 16#1 if debug=='Index' else hp.choice('clusters2',[6,11,16,21]) if debug=='Object' else 11 
        args['N_Areas'] = 4#0 if debug=='Index' else hp.choice('clusters3',[2,4,7]) if debug=='Object' else 2      
        args['Phenotype_Learning'] = True  
        args['Neighborhood_Learning'] = True
        args['Area_Learning'] = True
        args['dropoutRate'] = 0# 1 if debug=='Index' else hp.choice('dropoutRate', [0.1, 0.2, 0.3,0.4]) if debug=='Object' else 0.2        
        args['attntnThreshold'] = 0# if debug=='Index' else hp.choice('attntnThreshold', [0,.2,.4,.6,.8]) if debug=='Object' else 0  
                
        # Losses
        args['ContrastACC_Pheno'] = 0#4 if debug=='Index' else hp.choice("orthoColor_Lambda0", [1,0.1,0.01,0.001,0.0001,0.00001]) if debug=='Object' else 0.0001                                
        args['ContrastACC_Neigh'] = 0#4 if debug=='Index' else hp.choice("orthoColor_Lambda1", [1, 0.1,0.01,0.001,0.0001,0.00001]) if debug=='Object' else 0.0001                                              
        args['ContrastACC_Area'] = 0#4 if debug=='Index' else hp.choice("orthoColor_Lambda1", [1, 0.1,0.01,0.001,0.0001,0.00001]) if debug=='Object' else 0.0001                                              
        args['PatchEntropy_Pheno'] = 0#3 if debug=='Index' else hp.choice("min_Cell_entropy_Lambda0", [1,0.1,0.01,0.001,0]) if debug=='Object' else 0.001   
        args['PatchEntropy_Neigh'] = 0#4 if debug=='Index' else hp.choice("min_Cell_entropy_Lambda1", [1,0.1,0.01,0.001,0]) if debug=='Object' else 0
        args['PatchEntropy_Area'] = 0#1 if debug=='Index' else hp.choice("min_Cell_entropy_Lambda2", [1,0.1,0.01,0.001,0]) if debug=='Object' else 0.1          
        
        # Bioinsights parameters
        args['Bio_save_Orig_im'] = False


    elif 'Mary_Helen' in path or 'MH_test' in path:            
        
        # Patch contrastive learning parameters
        args['PCL_CNN_Architecture']='resnet50' # or resnet18
        args['PCL_N_Workers']=8 # Number of data loading workers 
        args['PCL_Epochs']=200 # Number of total epoch to run
        args['PCL_N_Crops_per_Image']=40 # Number of crops chosen per image
        args['PCL_Patch_Size']=40 # Size of patches in pixels
        args['PCL_Stride']=0 # Size of stride between consecutive patches
        args['PCL_Alpha_L']=1.15 # size ratio between image crop and image patch
        args['PCL_Z_Score']= True # Whether to apply z score per channel/marker
        args['PCL_Batch_Size']= 20 # Number of images per iteration
        args['PCL_Weight_Decay']= 1e-4 # Weight Decay
        args['PCL_Out_Dimensions']= 128 # Feature dimensions of patch
        args['PCL_Learning_Rate']= 0.0003 # Learning Rate
        args['PCL_Temperature']= 0.07 # Softmax temperature    
        args['PCL_eliminate_Black_Background'] = True 
        args['PCL_eliminate_White_Background'] = False        
        args['PCL_Color_perturbation_Augmentation'] = False # Whether to use color normalization augmentation in H&E white-field microscopy images. Used to force PCL to learn morphological features and avoid learning color staining features. 
        args['PCL_GPU_INDEX']= torch.device('cuda:0') # GPU where the training is carried out 

        # Label you want to infer with respect the images.
        args['experiment_Label'] = ['Treatment_Administered'] 

        # Architecture Search parameters
        args['num_samples_architecture_search'] = 1500  

        # Optimization Parameters
        args['NaroNet_n_workers'] = 1
        args['epochs'] = 1000# if debug else hp.quniform('epochs', 5, 25, 1)
        args['lr_decay_factor'] = 0.1# if debug else hp.uniform('lr_decay_factor', 0, 0.75)
        args['lr_decay_step_size'] = 10000#max(int(args['epochs']/5),1)# if debug else hp.quniform('lr_decay_step_size', 2, 20, 1)        
        args['weight_decay'] = 0
        args['batch_size'] = 24
        args['lr'] = 0.001

        # General
        args['training_MODE'] = 'TrainALL' # TrainALL, NestedCrossValidation, CrossValidation # Whether to use nested cross validation or cross validation.        
        args['folds'] = 1
        args['device'] = 'cuda:0'
        args['Batch_Normalization'] = True
        args['dataAugmentationPerc'] = 0 #0 if debug=='Index' else hp.choice("dataAugmentationPerc", [0,0.0001,0.001]) if debug=='Object' else 0  

        # Neural Network
        args['N_Phenotypes'] = 8
        args['N_Neighborhoods'] = 12
        args['N_Areas'] = 4
        args['n_hops_neighborhoods'] = 1
        args['Phenotype_Learning'] = True  
        args['Neighborhood_Learning'] = True
        args['Area_Learning'] = False
        args['dropoutRate'] = 0
        args['attntnThreshold'] = 0
        args['1Patch1Cluster'] = False
                
        # Losses
        args['ContrastACC_Pheno'] = 1000#4 if debug=='Index' else hp.choice("orthoColor_Lambda0", [1,0.1,0.01,0.001,0.0001,0.00001]) if debug=='Object' else 0.0001                                
        args['ContrastACC_Neigh'] = 1000#4 if debug=='Index' else hp.choice("orthoColor_Lambda1", [1, 0.1,0.01,0.001,0.0001,0.00001]) if debug=='Object' else 0.0001                                              
        args['ContrastACC_Area'] = 0#4 if debug=='Index' else hp.choice("orthoColor_Lambda1", [1, 0.1,0.01,0.001,0.0001,0.00001]) if debug=='Object' else 0.0001 
        args['Perc_high_conf_patches'] = 0.0001 # 1 is 100%. Great values generates phenotypes and neighborhoods with many patches. Low values generate rare populations.
        args['PatchEntropy_Pheno'] = 0#3 if debug=='Index' else hp.choice("min_Cell_entropy_Lambda0", [1,0.1,0.01,0.001,0]) if debug=='Object' else 0.001   
        args['PatchEntropy_Neigh'] = 0#4 if debug=='Index' else hp.choice("min_Cell_entropy_Lambda1", [1,0.1,0.01,0.001,0]) if debug=='Object' else 0
        args['PatchEntropy_Area'] = 0#1 if debug=='Index' else hp.choice("min_Cell_entropy_Lambda2", [1,0.1,0.01,0.001,0]) if debug=='Object' else 0.1          
        
        # Bioinsights parameters
        args['Bio_save_Orig_im'] = True
        args['TSNE_Perc_Pat'] = 0 # Percentage of patients to use to generate the tsne. 
        args['Pheno_Perc_Pat'] = 0.05 # Percentage of patients to use to generate the tsne. 


    elif 'Melanoma_ProgressionvsBaseline' in path:            
        
        # Patch contrastive learning parameters
        args['PCL_CNN_Architecture']='resnet50' # or resnet18
        args['PCL_N_Workers']=1 # Number of data loading workers 
        args['PCL_Epochs']=300 # Number of total epoch to run
        args['PCL_N_Crops_per_Image']=200 # Number of crops chosen per image
        args['PCL_Patch_Size']=50 # Size of patches in pixels
        args['PCL_Stride']=0 # Size of stride between consecutive patches
        args['PCL_Alpha_L']=1.15 # size ratio between image crop and image patch
        args['PCL_Z_Score']= True # Whether to apply z score per channel/marker
        args['PCL_Batch_Size']= 4 # Number of images per iteration
        args['PCL_Weight_Decay']= 1e-4 # Weight Decay
        args['PCL_Out_Dimensions']= 128 # Feature dimensions of patch
        args['PCL_Learning_Rate']= 0.0003 # Learning Rate
        args['PCL_Temperature']= 0.07 # Softmax temperature                
        args['PCL_eliminate_Black_Background'] = False
        args['PCL_eliminate_White_Background'] = True
        args['PCL_GPU_INDEX']= torch.device('cuda:0') # GPU where the training is carried out 
        args['PCL_Color_perturbation_Augmentation'] = True # Color augmentation for H&E tissue staining.

        # Label you want to infer with respect the images.
        args['experiment_Label'] = ['Sample_Type'] 

        # Architecture Search parameters
        args['num_samples_architecture_search'] = 1500  

        # Optimization Parameters
        args['NaroNet_n_workers'] = 1
        args['epochs'] = 1000
        args['lr_decay_factor'] = 0.1
        args['lr_decay_step_size'] = 10000
        args['weight_decay'] = 0
        args['batch_size'] = 24
        args['lr'] = 0.001 

        # General
        args['training_MODE'] = 'TrainALL' # TrainALL, NestedCrossValidation, CrossValidation # Whether to use nested cross validation or cross validation.        
        args['folds'] = 1
        args['device'] = 'cuda:0'
        args['Batch_Normalization'] = True
        args['dataAugmentationPerc'] = 0 #0 if debug=='Index' else hp.choice("dataAugmentationPerc", [0,0.0001,0.001]) if debug=='Object' else 0  

        # Neural Network
        args['N_Phenotypes'] = 6#2 if debug=='Index' else hp.choice('clusters1',[5,10,15,20]) if debug=='Object' else 15     
        args['N_Neighborhoods'] = 8#1 if debug=='Index' else hp.choice('clusters2',[6,11,16,21]) if debug=='Object' else 11 
        args['N_Areas'] = 4#0 if debug=='Index' else hp.choice('clusters3',[2,4,7]) if debug=='Object' else 2      
        args['Phenotype_Learning'] = True  
        args['Neighborhood_Learning'] = True
        args['Area_Learning'] = True
        args['dropoutRate'] = 0# 1 if debug=='Index' else hp.choice('dropoutRate', [0.1, 0.2, 0.3,0.4]) if debug=='Object' else 0.2        
        args['attntnThreshold'] = 0# if debug=='Index' else hp.choice('attntnThreshold', [0,.2,.4,.6,.8]) if debug=='Object' else 0  
        args['1Patch1Cluster'] = False
                
        # Losses
        args['ContrastACC_Pheno'] = 100#4 if debug=='Index' else hp.choice("orthoColor_Lambda0", [1,0.1,0.01,0.001,0.0001,0.00001]) if debug=='Object' else 0.0001                                
        args['ContrastACC_Neigh'] = 100#4 if debug=='Index' else hp.choice("orthoColor_Lambda1", [1, 0.1,0.01,0.001,0.0001,0.00001]) if debug=='Object' else 0.0001                                              
        args['ContrastACC_Area'] = 0#4 if debug=='Index' else hp.choice("orthoColor_Lambda1", [1, 0.1,0.01,0.001,0.0001,0.00001]) if debug=='Object' else 0.0001                                              
        args['Perc_high_conf_patches'] = 0.001 # 1 is 100%. Great values generates phenotypes and neighborhoods with many patches. Low values generate rare populations.
        args['PatchEntropy_Pheno'] = 0#3 if debug=='Index' else hp.choice("min_Cell_entropy_Lambda0", [1,0.1,0.01,0.001,0]) if debug=='Object' else 0.001   
        args['PatchEntropy_Neigh'] = 0#4 if debug=='Index' else hp.choice("min_Cell_entropy_Lambda1", [1,0.1,0.01,0.001,0]) if debug=='Object' else 0
        args['PatchEntropy_Area'] = 0#1 if debug=='Index' else hp.choice("min_Cell_entropy_Lambda2", [1,0.1,0.01,0.001,0]) if debug=='Object' else 0.1          
        
        # Bioinsights parameters
        args['Bio_save_Orig_im'] = False
        args['TSNE_Perc_Pat'] = 0.5 # Percentage of patients used to calculate TSNE. 1 is 100% of patients


    elif 'AKOYA_Arlene_Tonsil' in path:            
        
        # Patch contrastive learning parameters
        args['PCL_CNN_Architecture']='resnet50' # or resnet18
        args['PCL_N_Workers']=10 # Number of data loading workers 
        args['PCL_Epochs']=100 # Number of total epoch to run
        args['PCL_N_Crops_per_Image']=20 # Number of crops chosen per image
        args['PCL_Patch_Size']=40 # Size of patches in pixels
        args['PCL_Stride']=0 # Size of stride between consecutive patches
        args['PCL_Alpha_L']=1.15 # size ratio between image crop and image patch
        args['PCL_Z_Score']= True # Whether to apply z score per channel/marker
        args['PCL_Batch_Size']= 50 # Number of images per iteration
        args['PCL_Weight_Decay']= 1e-4 # Weight Decay
        args['PCL_Out_Dimensions']= 128 # Feature dimensions of patch
        args['PCL_Learning_Rate']= 0.0003 # Learning Rate
        args['PCL_Temperature']= 0.07 # Softmax temperature                
        args['PCL_eliminate_Black_Background'] = False
        args['PCL_eliminate_White_Background'] = False
        args['PCL_GPU_INDEX']= torch.device('cuda:0') # GPU where the training is carried out 
        args['PCL_Color_perturbation_Augmentation'] = False # Color augmentation for H&E tissue staining.

        # Label you want to infer with respect the images.
        args['experiment_Label'] = ['Unsupervised'] 

        # Architecture Search parameters
        args['num_samples_architecture_search'] = 1500  

        # Optimization Parameters
        args['NaroNet_n_workers'] = 10
        args['epochs'] = 1000
        args['lr_decay_factor'] = 0.1
        args['lr_decay_step_size'] = 10000
        args['weight_decay'] = 0
        args['batch_size'] = 128
        args['lr'] = 0.1 

        # General
        args['training_MODE'] = 'TrainALL' # TrainALL, NestedCrossValidation, CrossValidation # Whether to use nested cross validation or cross validation.        
        args['folds'] = 1
        args['device'] = 'cuda:0'
        args['Batch_Normalization'] = True
        args['dataAugmentationPerc'] = 0 #0 if debug=='Index' else hp.choice("dataAugmentationPerc", [0,0.0001,0.001]) if debug=='Object' else 0  

        # Neural Network
        args['N_Phenotypes'] = 72#2 if debug=='Index' else hp.choice('clusters1',[5,10,15,20]) if debug=='Object' else 15     
        args['N_Neighborhoods'] = 36#1 if debug=='Index' else hp.choice('clusters2',[6,11,16,21]) if debug=='Object' else 11 
        args['N_Areas'] = 6#0 if debug=='Index' else hp.choice('clusters3',[2,4,7]) if debug=='Object' else 2      
        args['n_hops_neighborhoods'] = 1
        args['Phenotype_Learning'] = True  
        args['Neighborhood_Learning'] = True
        args['Area_Learning'] = True
        args['dropoutRate'] = 0# 1 if debug=='Index' else hp.choice('dropoutRate', [0.1, 0.2, 0.3,0.4]) if debug=='Object' else 0.2        
        args['attntnThreshold'] = 0# if debug=='Index' else hp.choice('attntnThreshold', [0,.2,.4,.6,.8]) if debug=='Object' else 0  
        args['1Patch1Cluster'] = False
                
        # Losses
        args['ContrastACC_Pheno'] = 1#4 if debug=='Index' else hp.choice("orthoColor_Lambda0", [1,0.1,0.01,0.001,0.0001,0.00001]) if debug=='Object' else 0.0001                                
        args['ContrastACC_Neigh'] = 1#4 if debug=='Index' else hp.choice("orthoColor_Lambda1", [1, 0.1,0.01,0.001,0.0001,0.00001]) if debug=='Object' else 0.0001                                              
        args['ContrastACC_Area'] = 0#4 if debug=='Index' else hp.choice("orthoColor_Lambda1", [1, 0.1,0.01,0.001,0.0001,0.00001]) if debug=='Object' else 0.0001     
        args['Perc_high_conf_patches'] = 0.0001 # 1 is 100%. Great values generates phenotypes and neighborhoods with many patches. Low values generate rare populations.
        args['PatchEntropy_Pheno'] = 0#3 if debug=='Index' else hp.choice("min_Cell_entropy_Lambda0", [1,0.1,0.01,0.001,0]) if debug=='Object' else 0.001   
        args['PatchEntropy_Neigh'] = 0#4 if debug=='Index' else hp.choice("min_Cell_entropy_Lambda1", [1,0.1,0.01,0.001,0]) if debug=='Object' else 0
        args['PatchEntropy_Area'] = 1#1 if debug=='Index' else hp.choice("min_Cell_entropy_Lambda2", [1,0.1,0.01,0.001,0]) if debug=='Object' else 0.1          
        
        # Bioinsights parameters
        args['Bio_save_Orig_im'] = True
        args['TSNE_Perc_Pat'] = 0 # Percentage of patients used to calculate TSNE. 1 is 100% of patients
        args['Pheno_Perc_Pat'] = 1 # Percentage of patients used to calculate TSNE. 1 is 100% of patients
        args['Pheno_Excluded_from_analysis'] = [25] # Percentage of patients used to calculate TSNE. 1 is 100% of patients
        args['Neigh_Excluded_from_analysis'] = [] # Percentage of patients used to calculate TSNE. 1 is 100% of patients
    
    elif 'Pancreas_Adenocarcinoma' in path:            
        
        # Patch contrastive learning parameters
        args['PCL_CNN_Architecture']='resnet50' # or resnet18
        args['PCL_N_Workers']=10 # Number of data loading workers 
        args['PCL_Epochs']=600 # Number of total epoch to run
        args['PCL_N_Crops_per_Image']=40 # Number of crops chosen per image
        args['PCL_Patch_Size']=30 # Size of patches in pixels
        args['PCL_Stride']=0 # Size of stride between consecutive patches
        args['PCL_Alpha_L']=1.15 # size ratio between image crop and image patch
        args['PCL_Z_Score']= True # Whether to apply z score per channel/marker
        args['PCL_Batch_Size']= 20 # Number of images per iteration
        args['PCL_Weight_Decay']= 1e-4 # Weight Decay
        args['PCL_Out_Dimensions']= 128 # Feature dimensions of patch
        args['PCL_Learning_Rate']= 0.0003 # Learning Rate
        args['PCL_Temperature']= 0.07 # Softmax temperature                
        args['PCL_eliminate_Black_Background'] = False
        args['PCL_eliminate_White_Background'] = True
        args['PCL_GPU_INDEX']= torch.device('cuda:0') # GPU where the training is carried out 
        args['PCL_Color_perturbation_Augmentation'] = False # Color augmentation for H&E tissue staining.

        # Label you want to infer with respect the images.
        args['experiment_Label'] = ['Unsupervised'] 

        # Architecture Search parameters
        args['num_samples_architecture_search'] = 1500  

        # Optimization Parameters
        args['NaroNet_n_workers'] = 1
        args['epochs'] = 1000
        args['lr_decay_factor'] = 0.1
        args['lr_decay_step_size'] = 10000
        args['weight_decay'] = 0
        args['batch_size'] = 24
        args['lr'] = 0.0001 

        # General
        args['training_MODE'] = 'TrainALL' # TrainALL, NestedCrossValidation, CrossValidation # Whether to use nested cross validation or cross validation.        
        args['folds'] = 1
        args['device'] = 'cuda:0'
        args['Batch_Normalization'] = True
        args['dataAugmentationPerc'] = 0 #0 if debug=='Index' else hp.choice("dataAugmentationPerc", [0,0.0001,0.001]) if debug=='Object' else 0  

        # Neural Network
        args['N_Phenotypes'] = 6
        args['N_Neighborhoods'] = 10
        args['N_Areas'] = 4
        args['n_hops_neighborhoods'] = 2
        args['Phenotype_Learning'] = True  
        args['Neighborhood_Learning'] = True
        args['Area_Learning'] = False
        args['dropoutRate'] = 0# 1 if debug=='Index' else hp.choice('dropoutRate', [0.1, 0.2, 0.3,0.4]) if debug=='Object' else 0.2        
        args['attntnThreshold'] = 0# if debug=='Index' else hp.choice('attntnThreshold', [0,.2,.4,.6,.8]) if debug=='Object' else 0  
        args['1Patch1Cluster'] = False
                
        # Losses
        args['ContrastACC_Pheno'] = 1000#4 if debug=='Index' else hp.choice("orthoColor_Lambda0", [1,0.1,0.01,0.001,0.0001,0.00001]) if debug=='Object' else 0.0001                                
        args['ContrastACC_Neigh'] = 1000#4 if debug=='Index' else hp.choice("orthoColor_Lambda1", [1, 0.1,0.01,0.001,0.0001,0.00001]) if debug=='Object' else 0.0001                                              
        args['ContrastACC_Area'] = 0#4 if debug=='Index' else hp.choice("orthoColor_Lambda1", [1, 0.1,0.01,0.001,0.0001,0.00001]) if debug=='Object' else 0.0001     
        args['Perc_high_conf_patches'] = 0.0001 # 1 is 100%. Great values generates phenotypes and neighborhoods with many patches. Low values generate rare populations.
        args['PatchEntropy_Pheno'] = 0#3 if debug=='Index' else hp.choice("min_Cell_entropy_Lambda0", [1,0.1,0.01,0.001,0]) if debug=='Object' else 0.001   
        args['PatchEntropy_Neigh'] = 0#4 if debug=='Index' else hp.choice("min_Cell_entropy_Lambda1", [1,0.1,0.01,0.001,0]) if debug=='Object' else 0
        args['PatchEntropy_Area'] = 0#1 if debug=='Index' else hp.choice("min_Cell_entropy_Lambda2", [1,0.1,0.01,0.001,0]) if debug=='Object' else 0.1          
        
        # Bioinsights parameters
        args['Bio_save_Orig_im'] = True # Whether to save raw data again. Helpful when patients are composed by more than one image since it creates a mosaic.
        args['TSNE_Perc_Pat'] = 0 # Percentage of patients used to calculate TSNE. 1 is 100% of patients
        args['Pheno_Perc_Pat'] = 1 # Percentage of patients used to calculate TSNE. 1 is 100% of patients
        args['Pheno_Excluded_from_analysis'] = [] # Phenotype excluded from the analysis e.g., [1], [3,7] for eliminating phenotype 1 and phenotypes 3 and 7, respectively
        args['Neigh_Excluded_from_analysis'] = [] # Neighborhoods excluded from the analysis e.g., [1], [3,7] for eliminating neighborhood 1 and phenotypes 3 and 7, respectively


    else:
        
        # Patch contrastive learning parameters
        args['PCL_CNN_Architecture']='resnet50' # or resnet18
        args['PCL_N_Workers']=8 # Number of data loading workers 
        args['PCL_Epochs']=80 # Number of total epoch to run
        args['PCL_N_Crops_per_Image']=40 # Number of crops chosen per image
        args['PCL_Patch_Size']=30 # Size of patches in pixels
        args['PCL_Stride']=0 # Size of stride between consecutive patches
        args['PCL_Alpha_L']=1.15 # size ratio between image crop and image patch
        args['PCL_Z_Score']= True # Whether to apply z score per channel/marker
        args['PCL_Batch_Size']= 1 # Number of images per iteration
        args['PCL_Weight_Decay']= 1e-4 # Weight Decay
        args['PCL_Out_Dimensions']= 128 # Feature dimensions of patch
        args['PCL_Learning_Rate']= 0.003 # Learning Rate
        args['PCL_Temperature']= 0.07 # Softmax temperature    
        args['PCL_eliminate_Black_Background'] = False
        args['PCL_eliminate_White_Background'] = False            
        args['PCL_GPU_INDEX']= torch.device('cuda:0') # GPU where the training is carried out 

        # Label you want to infer with respect the images.
        args['experiment_Label'] = ['Clinical_Benefit'] 

        # Architecture Search parameters
        args['num_samples_architecture_search'] = 1500  

        # Optimization Parameters
        args['epochs'] = 1000# if debug else hp.quniform('epochs', 5, 25, 1)
        args['lr_decay_factor'] = 0.1# if debug else hp.uniform('lr_decay_factor', 0, 0.75)
        args['lr_decay_step_size'] = 10000#max(int(args['epochs']/5),1)# if debug else hp.quniform('lr_decay_step_size', 2, 20, 1)        
        args['weight_decay'] = 4 if debug=='Index' else hp.choice('weight_decay',[0.1,0.01,0.001,0.0001,0]) if debug=='Object' else 0
        args['batch_size'] = 3 if debug=='Index' else hp.choice('batch_size', [2, 4, 8, 24]) if debug=='Object' else 24
        args['lr'] = 0 if debug=='Index' else hp.choice('lr', [1,0.1,0.01,0.001,0.0001]) if debug=='Object' else 1

        # General
        args['training_MODE'] = 'TrainALL' # TrainALL, NestedCrossValidation, CrossValidation # Whether to use nested cross validation or cross validation.        
        args['folds'] = 1
        args['device'] = 'cuda:0'
        args['Batch_Normalization'] = True
        args['dataAugmentationPerc'] = 0 #0 if debug=='Index' else hp.choice("dataAugmentationPerc", [0,0.0001,0.001]) if debug=='Object' else 0  

        # Neural Network
        args['N_Phenotypes'] = 8#2 if debug=='Index' else hp.choice('clusters1',[5,10,15,20]) if debug=='Object' else 15     
        args['N_Neighborhoods'] = 16#1 if debug=='Index' else hp.choice('clusters2',[6,11,16,21]) if debug=='Object' else 11 
        args['N_Areas'] = 4#0 if debug=='Index' else hp.choice('clusters3',[2,4,7]) if debug=='Object' else 2      
        args['Phenotype_Learning'] = True  
        args['Neighborhood_Learning'] = True
        args['Area_Learning'] = True
        args['dropoutRate'] = 0# 1 if debug=='Index' else hp.choice('dropoutRate', [0.1, 0.2, 0.3,0.4]) if debug=='Object' else 0.2        
        args['attntnThreshold'] = 0# if debug=='Index' else hp.choice('attntnThreshold', [0,.2,.4,.6,.8]) if debug=='Object' else 0  
                
        # Losses
        args['ContrastACC_Pheno'] = 0.01#4 if debug=='Index' else hp.choice("orthoColor_Lambda0", [1,0.1,0.01,0.001,0.0001,0.00001]) if debug=='Object' else 0.0001                                
        args['ContrastACC_Neigh'] = 0.01#4 if debug=='Index' else hp.choice("orthoColor_Lambda1", [1, 0.1,0.01,0.001,0.0001,0.00001]) if debug=='Object' else 0.0001                                              
        args['ContrastACC_Area'] = 0.0001#4 if debug=='Index' else hp.choice("orthoColor_Lambda1", [1, 0.1,0.01,0.001,0.0001,0.00001]) if debug=='Object' else 0.0001                                              
        args['PatchEntropy_Pheno'] = 0.01#3 if debug=='Index' else hp.choice("min_Cell_entropy_Lambda0", [1,0.1,0.01,0.001,0]) if debug=='Object' else 0.001   
        args['PatchEntropy_Neigh'] = 0.01#4 if debug=='Index' else hp.choice("min_Cell_entropy_Lambda1", [1,0.1,0.01,0.001,0]) if debug=='Object' else 0
        args['PatchEntropy_Area'] = 0.0001#1 if debug=='Index' else hp.choice("min_Cell_entropy_Lambda2", [1,0.1,0.01,0.001,0]) if debug=='Object' else 0.1          
        
        # Bioinsights parameters
        args['Bio_save_Orig_im'] = True


    return args