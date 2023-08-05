import torch
import numpy as np
from typing import *
from torch import nn, Tensor
from torch.nn import TransformerEncoder, TransformerEncoderLayer

from .txt import (ContextTransformer, MeanMaxPooling, PositionalEncoding,
                  SequenceTransformerHistory)

# Transformer x Embedding x Embedding as Bottom

class SequenceTransformerHistoryLite(SequenceTransformerHistory):
    def __init__(self, cross_size, item_embedding, seq_embed_dim, seq_max_length=8, seq_num_heads=4,
                 seq_hidden_size=512, seq_transformer_dropout=0.0, seq_num_layers=2, seq_pooling_dropout=0.0,
                 seq_pe=True):
        super(SequenceTransformerHistory, self).__init__()
        self.seq_embedding = item_embedding
        self.seq_pos = seq_pe
        self.seq_embed_dim = seq_embed_dim
        if seq_pe:
            self.pos_encoder = PositionalEncoding(d_model=seq_embed_dim,
                                                  dropout=seq_transformer_dropout,
                                                  max_len=seq_max_length)
        encoder_layers = TransformerEncoderLayer(d_model=seq_embed_dim,
                                                 nhead=seq_num_heads,
                                                 dropout=seq_transformer_dropout,
                                                 dim_feedforward=seq_hidden_size,
                                                 activation='relu',
                                                 batch_first=True)
        self.seq_encoder = TransformerEncoder(encoder_layers, num_layers=seq_num_layers)
        self.seq_pooling_dp = MeanMaxPooling(dropout=seq_pooling_dropout)
        self.seq_dense = torch.nn.Linear(in_features=2 * seq_embed_dim, out_features=cross_size)


class ContextHead(nn.Module):
    """
    [[B, ] * C] -> [B, cross_size]
    """
    def __init__(self, deep_dims, num_wide, cross_size, item_embedding, deep_embed_dims=100):
        super().__init__()
        if isinstance(deep_embed_dims, int):
            self.deep_embedding = nn.ModuleList([
                nn.Embedding(deep_dim, deep_embed_dims)
                for deep_dim in deep_dims
            ])
            dense_in = len(deep_dims) * deep_embed_dims
        elif isinstance(deep_embed_dims, list) or isinstance(deep_embed_dims, tuple):
            self.deep_embedding = nn.ModuleList([
                nn.Embedding(deep_dim, deep_embed_dim)
                for deep_dim, deep_embed_dim in zip(deep_dims, deep_embed_dims)
            ])
            dense_in = sum(deep_embed_dims)
        else:
            raise NotImplementedError()
        self.ctx_pe = False
        self.layer_norm = nn.LayerNorm(num_wide)
        self.deep_embed_dims = deep_embed_dims
        self.device_embed = item_embedding
        self.ctx_dense = torch.nn.Linear(in_features=dense_in+num_wide+item_embedding.embedding_dim, out_features=cross_size)


    def forward(self, deep_in:List[Tensor], wide_in:List[Tensor], device_in:Tensor):
        """
        :param deep_in: list, a list of Tensor of shape [batch_size, 1]
        :param wide_in: list, a list of Tensor of shape [batch_size, 1]
        :param device_in: Tensor
        :return: Tensor, shape [batch_size, cross_size]
        """
        # [[B, ] * C]
        deep_embedding_list = [self.deep_embedding[i](input_deep).unsqueeze(1)
                              for i, input_deep in enumerate(deep_in)]  # -> [(B, 1, E_i) * C]
        device_out = self.device_embed(device_in).unsqueeze(1)
        device_out = torch.nan_to_num(device_out)
        deep_embedding_list.append(device_out) # -> [(B, 1, E_i) * C]
        deep_out = torch.cat(deep_embedding_list, dim=2).squeeze(1) # -> [B, sum(E_i)]
        wide_in_list = [wide_i.float() for wide_i in wide_in]
        wide_cat = torch.stack(wide_in_list, dim=0)
        wide_out = torch.transpose(wide_cat, dim1=1, dim0=0)
        wide_out_norm = self.layer_norm(wide_out)
        ctx_out = torch.cat((deep_out, wide_out_norm), dim=1) # -> [B, sum(E_i)]
        ctx_out = self.ctx_dense(ctx_out)  # -> (B, cross_size)
        return ctx_out



class BST(nn.Module):
    def __init__(self, deep_dims, seq_dim, seq_embed_dim, num_wide, ctx_cross_size=100, seq_cross_size=200,
                 context_head_kwargs=None, sequence_transformer_kwargs=None):
        super().__init__()
        context_head_kwargs = context_head_kwargs if context_head_kwargs else {}
        sequence_transformer_kwargs = sequence_transformer_kwargs if sequence_transformer_kwargs else {}
        self.features_dim = seq_cross_size + ctx_cross_size
        self.item_embedding = nn.Embedding(seq_dim, seq_embed_dim)
        self.context_head = ContextHead(
            deep_dims=deep_dims,
            cross_size=ctx_cross_size,
            num_wide=num_wide,
            item_embedding=self.item_embedding,
            **context_head_kwargs,
        )
        self.sequence_transformer = SequenceTransformerHistoryLite(
            cross_size=seq_cross_size,
            item_embedding=self.item_embedding,
            seq_embed_dim=seq_embed_dim,
            **sequence_transformer_kwargs,
        )

    def forward(self, deep_in, wide_in, seq_in, device_in, vl_in, seq_history=None):
        """
        :param ctx_in: list, a list of Tensor of shape [batch_size, 1]
        :param num_in: list, a list of Tensor of shape [batch_size, 1]
        :param seq_in: Tensor, shape [batch_size, seq_len]
        :param vl_in: Tensor, shape [batch_size]
        :param candidate_in: Tensor, shape [batch_size]
        :param seq_history: Tensor, shape [batch_size, history_len]
        :return:
        """
        # input [[B, 1] * C] and [B, 5]
        ctx_out = self.context_head(deep_in=deep_in, wide_in=wide_in, device_in=device_in)
        seq_out = self.sequence_transformer(seq_in=seq_in, vl_in=vl_in, seq_history=seq_history)
        seq_out = torch.nan_to_num(seq_out)
        outs = torch.cat([seq_out, ctx_out], dim=1)  # -> [B, CROSS_seq + CROSS_ctx]
        return outs


class TxT(nn.Module):
    def __init__(self, ctx_nums, seq_num, cross_size=200, is_candidate_mode=True,
                 context_transformer_kwargs=None, sequence_transformer_kwargs=None):
        super().__init__()
        context_transformer_kwargs = context_transformer_kwargs if context_transformer_kwargs else {}
        sequence_transformer_kwargs = sequence_transformer_kwargs if sequence_transformer_kwargs else {}
        self.is_candidate_mode = is_candidate_mode
        self.features_dim = cross_size
        self.context_transformer = ContextTransformer(
            ctx_nums=ctx_nums,
            cross_size=cross_size,
            **context_transformer_kwargs,
        )
        self.sequence_transformer = SequenceTransformerHistory(
            seq_num=seq_num,
            cross_size=cross_size,
            **sequence_transformer_kwargs,
        )
        if is_candidate_mode:
            # self.candidate_dense = nn.Linear(
            #     in_features=self.sequence_transformer.seq_embed_size,
            #     out_features=cross_size
            # )
            pass

    def forward(self, ctx_in, seq_in, vl_in, candidate_in, seq_history=None):
        """
        :param ctx_in: list, a list of Tensor of shape [batch_size, 1]
        :param seq_in: Tensor, shape [batch_size, seq_len]
        :param vl_in: Tensor, shape [batch_size]
        :param candidate_in: Tensor, shape [batch_size]
        :param seq_history: Tensor, shape [batch_size, history_len]
        :return:
        """
        # input [[B, 1] * C] and [B, 5]
        ctx_out = self.context_transformer(ctx_in=ctx_in)
        seq_out = self.sequence_transformer(seq_in=seq_in, vl_in=vl_in, seq_history=seq_history)
        outs = torch.mul(seq_out, ctx_out)  # -> [B, cross_size]
        if self.is_candidate_mode:
            candidate_embed = self.sequence_transformer.seq_embedding(candidate_in)
            outs = torch.concat([outs, candidate_embed], dim=1)  # -> [B, seq_embed_size]
        return outs
