# Example Package
# MUSE-PyTorch
This repo is a pytorch-lightning implementation of the official [MUSE: multi-modality structured embedding for spatially resolved transcriptomics analysis](https://github.com/AltschulerWu-Lab/MUSE):
 
> Bao, F., Deng, Y., Wan, S. et al. Integrative spatial analysis of cell morphologies and transcriptional states with MUSE. Nat Biotechnol (2022). https://doi.org/10.1038/s41587-022-01251-z

## Requirements

 - numpy==1.22.3
 - online_triplet_loss==0.0.6
 - pandas==1.4.2
 - PhenoGraph==1.5.7
 - pytorch_lightning==1.6.3
 - scipy==1.8.0
 - torch==1.11.0


## Installation

To install MUSE PyTorch package, use

```terminal
pip install muse_pytorch
```

## Usage

```python
import muse_pytorch as muse
```

The library exposes the same fit_predict method as the orignial one. 

```python
z, x_hat, y_hat, latent_x, latent_y = muse.fit_predict(trans_features,
                                                       morph_features,
                                                       trans_labels,
                                                       morph_labels,
                                                       init_epochs=3, 
                                                       refine_epochs=3, 
                                                       cluster_epochs=6, 
                                                       cluster_update_epoch=2, 
                                                       joint_latent_dim=50, 
                                                       batch_size=512)
```
The method expects the same parameters, and more. 
```
Parameters:

  trans_features:           input for transcript modality; matrix of  n * p, where n = number of cells, p = number of genes.
  morph_features:           input for morphological modality; matrix of n * q, where n = number of cells, q is the feature dimension.
  trans_labels:             initial reference cluster label for transcriptional modality.
  morph_labels:             inital reference cluster label for morphological modality.
  latent_dim:               size of the latent dimension for the single modalities
  joint_latent_dim:         size of the latent dimension of the joint representation
  lambda_reg:               factor for the regularisation term in the loss function
  lambda_sup:               factor for the self-supervised term in the loss function
  lr:                       learning rate for the optimizer
  init_epochs:              epochs for the initializing phase
  refine_epochs:            epochs for the refining phase
  cluster_epochs:           epochs for the clustering phase
  cluster_update_epoch:     interval after which the single modality clusters will be updated      
  batch_size:               batch size for the dataloaders

Outputs:

  z:            joint latent representation learned by MUSE.
  x_hat:        reconstructed feature matrix corresponding to input data_x.
  y_hat:        reconstructed feature matrix corresponding to input data_y.
  h_x:          modality-specific latent representation corresponding to data_x.
  h_y:          modality-specific latent representation corresponding to data_y.
```

On top of this, it is also possible to further personalize the training by importing PyTorch Lightning Module & Datamodule


```python
from muse_pytorch import MUSE, MUSEDataModule
```

For a complete description of the project please head to the [original repo](https://github.com/AltschulerWu-Lab/MUSE)