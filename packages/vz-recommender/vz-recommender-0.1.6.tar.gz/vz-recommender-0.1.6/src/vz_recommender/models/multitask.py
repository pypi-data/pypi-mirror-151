from torch import nn

from .mmoe import MMoE
from .bottom import BST, TxT


class MultiTaskBST(nn.Module):
    def __init__(self, deep_dims, seq_dim, seq_embed_dim, num_wide, expert_num, expert_hidden_sizes,
                 task_num, task_hidden_sizes, task_last_activations,
                 ctx_cross_size=100, seq_cross_size=200, context_head_kwargs=None, 
                 sequence_transformer_kwargs=None):
        super(MultiTaskBST, self).__init__()
        self.shared_bottom = BST(
            deep_dims=deep_dims,
            seq_dim=seq_dim,
            seq_embed_dim=seq_embed_dim,
            num_wide=num_wide,
            ctx_cross_size=ctx_cross_size,
            seq_cross_size=seq_cross_size,
            context_head_kwargs=context_head_kwargs,
            sequence_transformer_kwargs=sequence_transformer_kwargs,
        )
        mmoe_input_size = ctx_cross_size + seq_cross_size
        self.mmoe = MMoE(
            input_size=mmoe_input_size,
            expert_num=expert_num,
            expert_hidden_sizes=expert_hidden_sizes,
            task_num=task_num,
            task_hidden_sizes=task_hidden_sizes,
            task_last_activations=task_last_activations,
        )

    def forward(self, deep_in, wide_in, seq_in, device_in, vl_in, seq_history=None):
        bottom_features = self.shared_bottom(deep_in=deep_in, wide_in=wide_in, seq_in=seq_in, device_in=device_in, vl_in=vl_in, seq_history=seq_history)
        outs = self.mmoe(bottom_features)
        return outs


class MultiTaskTxT(nn.Module):
    def __init__(self, ctx_nums, seq_num, expert_num, expert_hidden_sizes,
                 task_num, task_hidden_sizes, task_last_activations,
                 cross_size=200, is_candidate_mode=True,
                 context_transformer_kwargs=None, sequence_transformer_kwargs=None):
        super().__init__()
        self.is_candidate_mode = is_candidate_mode
        self.shared_bottom = TxT(
            ctx_nums=ctx_nums,
            seq_num=seq_num,
            cross_size=cross_size,
            is_candidate_mode=is_candidate_mode,
            context_transformer_kwargs=context_transformer_kwargs,
            sequence_transformer_kwargs=sequence_transformer_kwargs,
        )
        mmoe_input_size = cross_size + self.shared_bottom.sequence_transformer.seq_embed_dim
        self.mmoe = MMoE(
            input_size=mmoe_input_size,
            expert_num=expert_num,
            expert_hidden_sizes=expert_hidden_sizes,
            task_num=task_num,
            task_hidden_sizes=task_hidden_sizes,
            task_last_activations=task_last_activations,
        )

    def forward(self, ctx_in, seq_in, vl_in, candidate_in, seq_history=None):
        bottom_features = self.shared_bottom(ctx_in, seq_in, vl_in, candidate_in, seq_history)
        outs = self.mmoe(bottom_features)
        return outs
