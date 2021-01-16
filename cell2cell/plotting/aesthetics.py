# -*- coding: utf-8 -*-

from matplotlib import pyplot as plt
import matplotlib.patches as patches

def get_colors_from_labels(labels, cmap='gist_rainbow', factor=1):
    assert factor >= 1

    colors = dict.fromkeys(labels, ())

    factor = int(factor)
    NUM_COLORS = factor * len(colors)
    cm = plt.get_cmap(cmap)

    for i, label in enumerate(colors.keys()):
        colors[label] = cm((1 + ((factor-1)/factor)) * i / NUM_COLORS)
    return colors


def map_colors_to_metadata(df, metadata, colors=None, sample_col='#SampleID', group_col='Groups',
                           meta_cmap='gist_rainbow'):
    meta_ = metadata.set_index(sample_col).reindex(df.columns)
    labels = meta_[group_col].unique().tolist()
    if colors is None:
        colors = get_colors_from_labels(labels, cmap=meta_cmap)
    else:
        upd_dict = dict([(v, (1., 1., 1., 1.)) for v in labels if v not in colors.keys()])
        colors.update(upd_dict)

    new_colors = meta_[group_col].map(colors)
    new_colors.index = meta_.index
    new_colors.name = group_col.capitalize()

    return new_colors


def generate_legend(color_dict, loc='center left', bbox_to_anchor=(1.01, 0.5), ncol=1, fancybox=True, shadow=True,
                    title='legend', fontsize=14, fig=None):
    color_patches = []
    for k, v in sorted(color_dict.items()):
        color_patches.append(patches.Patch(color=v, label=k.replace('_', ' ')))

    legend1 = plt.legend(handles=color_patches,
                         loc=loc,
                         bbox_to_anchor=bbox_to_anchor,
                         ncol=ncol,
                         fancybox=fancybox,
                         shadow=shadow,
                         title=title,
                         fontsize=fontsize)

    if fig is None:
        plt.setp(legend1.get_title(), fontsize=fontsize)
        plt.gca().add_artist(legend1)
    else:
        plt.setp(legend1.get_title(), fontsize=fontsize)
    return legend1