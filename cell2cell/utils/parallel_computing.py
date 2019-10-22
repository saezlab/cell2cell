# -*- coding: utf-8 -*-

from __future__ import absolute_import

from multiprocessing import cpu_count

# GENERAL
def agents_number(n_jobs):
    '''
    This function computes the number of available agents based on the number of jobs provided.

    '''
    if n_jobs < 0:
        agents = cpu_count() + 1 + n_jobs
        if agents < 0:
            agents = 1
    elif n_jobs > cpu_count():
        agents = cpu_count()

    elif n_jobs == 0:
        agents = 1
    else:
        agents = n_jobs
    return agents

# CORE FUNCTIONS
def parallel_subsampling_interactions(inputs):
    '''
    Parallel computing in cell2cell2.subsampling.SubsamplingSpace
    '''
    from cell2cell.core import subsampling_operation
    results = subsampling_operation(cell_ids=inputs['cells'],
                                    last_item= inputs['list_end'],
                                    rnaseq_data=inputs['rnaseq'],
                                    ppi_dict=inputs['ppi'],
                                    interaction_type=inputs['interaction_type'],
                                    gene_cutoffs=inputs['cutoffs'],
                                    score_type=inputs['score_type'],
                                    score_metric=inputs['score_metric'],
                                    cci_matrix_template=inputs['cci_matrix'],
                                    seed=inputs['seed'],
                                    verbose=inputs['verbose'])

    return results


# CLUSTERING FUNCTIONS
def parallel_community_detection(inputs):
    '''
    Parallel computing in cell2cell2.clustering.clustering_interactions
    '''
    from cell2cell.clustering import louvain_community

    included_cells = inputs['interaction_elements']['cells']
    cci_matrix = inputs['interaction_elements']['cci_matrix'].loc[included_cells, included_cells]

    results = louvain_community(cci_matrix=cci_matrix,
                                seed=inputs['seed'],
                                package=inputs['package'],
                                verbose=inputs['verbose'])
    return results


def parallel_leiden_community(inputs):
    '''
    Parallel computing in cell2cell2.clustering.clustering_interactions
    '''
    from cell2cell.clustering import leiden_community

    included_cells = inputs['interaction_elements']['cells']
    cci_matrix = inputs['interaction_elements']['cci_matrix'].loc[included_cells, included_cells]

    results = leiden_community(cci_matrix=cci_matrix,
                               verbose=inputs['verbose'])
    return results