#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 14:59:14 2022

@author: Yossi Eikelman
"""
import logging


def get_logger(name):
    """Logger function for logging from multiple .py files into dev.log."""
    log_format = "%(asctime)s. %(name)5s %(levelname)5s MESSAGE: '%(message)s'\n"
    logging.basicConfig(filename='dev.log', level=logging.INFO,
                        format=log_format, filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)
    console.setFormatter(logging.Formatter(log_format))
    logging.getLogger(name).addHandler(console)
    return logging.getLogger(name)


def extract_fields(in_fields, keys) -> dict:
    """Extractor for pulling relevant fields from instance fields/dictionary."""
    res = {}
    for k, v in in_fields.items():
        for key in keys:
            if key in k:
                res[k] = v
    return res
