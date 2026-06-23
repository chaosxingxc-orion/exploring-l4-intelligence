"""Evaluation harness: build embedding matrices and score disentanglement.

All heavy deps stay lazy (the embedder and sklearn are imported inside the functions this
subpackage calls), so importing ``speechrl_common.eval`` is cheap.
"""
