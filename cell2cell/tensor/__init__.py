# -*- coding: utf-8 -*-
from cell2cell.tensor.factor_manipulation import (normalize_factors)
from cell2cell.tensor.metrics import (correlation_index)
from cell2cell.tensor.tensor import (InteractionTensor, PreBuiltTensor, build_context_ccc_tensor, generate_tensor_metadata,
                                     interactions_to_tensor)
from cell2cell.tensor.subset import (subset_tensor, subset_metadata)
