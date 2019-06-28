# -*- coding: utf-8 -*-

from __future__ import absolute_import

import pandas as pd
from cell2cell.preprocessing import ppi, gene_ontology

## RNAseq data
def get_modified_rnaseq(rnaseq_data, function_type='binary', **kwargs):
    if function_type == 'binary':
        modified_rnaseq = get_binary_rnaseq(rnaseq_data, kwargs['cutoffs'])
    else:
        # As other functions are implemented, other elif condition will be included here.
        raise NotImplementedError("Function type {} to compute pairwise cell-interactions is not implemented".format(function_type))
    return modified_rnaseq


def get_binary_rnaseq(rnaseq_data, cutoffs):
    binary_rnaseq_data = rnaseq_data.copy()
    for column in rnaseq_data.columns:
        binary_rnaseq_data[column] = binary_rnaseq_data[column].to_frame().apply(axis=1, func=lambda row: 1.0 if (row[column] >= cutoffs.loc[row.name, 'value']) else 0.0).values
    return binary_rnaseq_data


## PPI data
def get_weighted_ppi(ppi_data, modified_rnaseq_data, column='value', function_type='binary'):
    if function_type == 'binary':
        weighted_ppi = get_binary_ppi(ppi_data, modified_rnaseq_data, column)
    else:
        # As other functions are implemented, other elif condition will be included here.
        raise NotImplementedError("Function type {} to compute pairwise cell-interactions is not implemented".format(function_type))
    return weighted_ppi


def get_binary_ppi(ppi_data, binary_rnaseq_data, column='value'):
    #binary_ppi = pd.DataFrame(columns=ppi_data.columns)
    binary_ppi = ppi_data.copy()
    binary_ppi['A'] = binary_ppi['A'].apply(func=lambda row: binary_rnaseq_data.loc[row, column])
    binary_ppi = binary_ppi[['A', 'score']].reset_index(drop=True)

    # binary_ppi['B'] = binary_ppi['B'].apply(func=lambda row: binary_rnaseq_data.loc[row, column])
    # binary_ppi = binary_ppi[['A', 'B', 'score']].reset_index(drop=True)
    return binary_ppi


def ppis_from_proteins(ppi_data, contact_proteins, mediator_proteins=None, interaction_columns=['A', 'B']):

    all_ppis = dict()
    all_ppis['contacts'] = ppi.filter_ppi_network(ppi_data,
                                              contact_proteins,
                                              mediator_proteins=mediator_proteins,
                                              interaction_type='contacts',
                                              interaction_columns=interaction_columns)
    if mediator_proteins is not None:
        all_ppis['mediated'] = ppi.filter_ppi_network(ppi_data,
                                                  contact_proteins,
                                                  mediator_proteins=mediator_proteins,
                                                  interaction_type='mediated',
                                                  interaction_columns=interaction_columns)

        all_ppis['combined'] = ppi.filter_ppi_network(ppi_data,
                                                  contact_proteins,
                                                  mediator_proteins=mediator_proteins,
                                                  interaction_type='combined',
                                                  interaction_columns=interaction_columns)
    # else:
    #     columns = interaction_columns + ['score']
    #     all_ppis['mediated'] = pd.DataFrame(columns=columns)
    #     all_ppis['combined'] = pd.DataFrame(columns=columns)
    # This is omitted because other functions use all_ppis.values() instead of checking all types of interactions.
    return all_ppis


def ppis_from_goterms(ppi_data, go_annotations, go_terms, contact_go_terms, mediator_go_terms=None, use_children=True,
                      go_header='GO', gene_header='Gene', interaction_columns=['A', 'B'], verbose=True):




    if use_children == True:
        contact_proteins = gene_ontology.get_genes_from_parent_go_terms(go_annotations,
                                                                        go_terms,
                                                                        contact_go_terms,
                                                                        go_header=go_header,
                                                                        gene_header=gene_header,
                                                                        verbose=verbose)

        mediator_proteins = gene_ontology.get_genes_from_parent_go_terms(go_annotations,
                                                                         go_terms,
                                                                         mediator_go_terms,
                                                                         go_header=go_header,
                                                                         gene_header=gene_header,
                                                                         verbose=verbose)
    else:
        contact_proteins = gene_ontology.go2genes(go_annotations,
                                                  contact_go_terms,
                                                  go_header=go_header,
                                                  gene_header=gene_header)

        mediator_proteins = gene_ontology.go2genes(go_annotations,
                                                   mediator_go_terms,
                                                   go_header=go_header,
                                                   gene_header=gene_header)

    ppi_dict = ppis_from_proteins(ppi_data,
                                  contact_proteins,
                                  mediator_proteins,
                                  interaction_columns=interaction_columns)

    return ppi_dict