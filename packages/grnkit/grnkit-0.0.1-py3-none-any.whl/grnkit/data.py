import numpy as np
from itertools import product
import os.path as osp

class GRNDataset(object):
    r""" A generic data class for single shot non-single-cell data
    
    Parameters
    ----------
    expression_data : [ndarray, list of ndarray]
    number_of_genes: int
        number of all genes
    gene_names: list of strings, optional
        List of gene names
    regulator_genes: list of strings, optional
        List of regulator gene names
    gold_standard: list of [regulator gene, target gene, score], optional
        Gold standard if available
    """
    def __init__(self, expression_data, 
                 number_of_genes, number_of_samples,
                 gene_names=None, regulator_genes=None, 
                 gold_standard=None):
        # Check gene names
        if gene_names is None:
            gene_names = ['G' + str(i+1) for i in range(number_of_genes)]
        gene_idx = {x: i for (i, x) in enumerate(gene_names)}
        if len(gene_idx) != len(gene_names):
            raise ValueError('duplicated gene names are not allowed')
        
        # Convert regulator_genes to list of indexes
        if regulator_genes is None:
            regulator_genes = [i for i in range(number_of_genes)]
        else:
            regulator_genes = [gene_idx[reg_g] for reg_g in regulator_genes]
            
        self.expression_data = expression_data
        self.number_of_genes = number_of_genes
        self.number_of_samples = number_of_samples
        self.gene_names = gene_names
        self.gene_idx = gene_idx
        self.regulator_genes = regulator_genes
        
        # Generate gold standard link dictionary
        interaction_dict = {
            '|'.join(x):i for i, x in enumerate(product(gene_names, gene_names))
        }
        gold_standard_adj_list = [0] * (number_of_genes ** 2)
        for (g1, g2, x) in gold_standard:
            if x != 0:
                gold_standard_adj_list[interaction_dict[g1 + '|' + g2]] = x
        self.gold_standard = gold_standard_adj_list
        self.interaction_dict = interaction_dict
        
    def gold_standard_is_available(self):
        return (self.gold_standard is not None)
    
class SingleShotGRNDataset(GRNDataset):
    r"""A generic data class for single shot non-single-cell data (2D)
    
    Parameters
    ----------
    expression_data : ndarray
        Expression data array where rows are samples and columns are genes. Shape = N x D.
    """
    
    def __init__(self, expression_data, 
                 gene_names=None, regulator_genes=None, gold_standard=None):
        number_of_genes = expression_data.shape[1]
        super(SingleShotGRNDataset, self).__init__(
            expression_data = expression_data, 
            number_of_genes = number_of_genes,
            number_of_samples = 1,
            gene_names = gene_names, 
            regulator_genes = regulator_genes, 
            gold_standard = gold_standard
        )
        
class TimeseriesGRNDataset(GRNDataset):
    r"""A generic data class for timeseries non-single-cell data (3D)
    
    Parameters
    ----------
    expression_data : list of ndarray
        List of expression data. Each element is a ndarray from a single 
        timeseries sample in the shape of T x (D+1). The first dimension is for
        timestamps in interger format. All arrays need to have the same 
        dimension on gene (D). 
    """
    
    def __init__(self, expression_data, 
                 gene_names=None, regulator_genes=None, gold_standard=None):
        time_stamps = []
        for i in range(len(expression_data)):
            time_stamps.append(expression_data[i][:, 0])
            expression_data[i] = expression_data[i][:, 1:]
            
        number_of_samples = len(expression_data)
        number_of_genes = expression_data[0].shape[1]
            
        super(TimeseriesGRNDataset, self).__init__(
            expression_data = expression_data, 
            number_of_genes = number_of_genes,
            number_of_samples = number_of_samples, 
            gene_names = gene_names, 
            regulator_genes = regulator_genes, 
            gold_standard = gold_standard
        )
        self.time_stamps = time_stamps
        
class Dream4TimeseriesDataset(TimeseriesGRNDataset):
    def __init__(self, size=10, network=1):
        if size == 10:
            n_ts = 5
        elif size == 100:
            n_ts = 10
            
        data_dir_path = osp.join('..', 'data', 'dream4')
        dataset_name = 'insilico_size' + str(size) + '_' + str(network)
        
        expression_file_path = osp.join(
            data_dir_path, 'Size ' + str(size), 'DREAM4 training data',
            dataset_name, dataset_name + '_timeseries.tsv'
        )
        expression_data = np.loadtxt(expression_file_path, skiprows=1)
        expression_data = np.split(expression_data, n_ts)
        
        goldstandard_file_path = osp.join(
            data_dir_path, 'Size ' + str(size), 'DREAM4 gold standards',
            dataset_name + '_goldstandard.tsv'
        )
        goldstandard = np.loadtxt(goldstandard_file_path, skiprows=1, dtype=str)
        goldstandard = [[x[0], x[1], 1] for x in goldstandard if x[2] == '1']
        
        super(Dream4TimeseriesDataset, self).__init__(
            expression_data = expression_data, 
            gold_standard = goldstandard
        )
        
        self.benchmark_name = 'Dream'
        self.n_ts = n_ts
        self.size = size
        self.network_id = network
        
class Dream4MultifactorialDataset(SingleShotGRNDataset):
    def __init__(self, network=1):
        data_dir_path = osp.join('..', 'data', 'dream4')
        dataset_name = 'insilico_size100_' + str(network)
        
        expression_file_path = osp.join(
            data_dir_path, 'Size 100 multifactorial', 
            'DREAM4 training data',
            dataset_name + '_multifactorial.tsv'
        )
        expression_data = np.loadtxt(expression_file_path, skiprows=1)
        
        goldstandard_file_path = osp.join(
            data_dir_path, 'Size 100 multifactorial',  
            'DREAM4 gold standards',
            'insilico_size100_multifactorial_' + str(network) + 
            '_goldstandard.tsv'
        )
        goldstandard = np.loadtxt(goldstandard_file_path, skiprows=1, dtype=str)
        goldstandard = [[x[0], x[1], 1] for x in goldstandard if x[2] == '1']
        
        super(Dream4MultifactorialDataset, self).__init__(
            expression_data = expression_data, 
            gold_standard = goldstandard
        )
        
        self.benchmark_name = 'Dream'
        self.network_id = network