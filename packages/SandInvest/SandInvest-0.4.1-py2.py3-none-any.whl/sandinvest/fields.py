#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author : SandQuant
# @Email: data@sandquant.com


class summary:
    code_ = 'code'
    name_ = 'name'
    symbol_ = 'symbol'
    company_cn = 'company_cn'
    company_en = 'company_en'
    list_date_ = 'list_date'
    delist_date_ = 'delist_date'
    market_ = 'market'
    board_ = 'board'
    all_ = [
        code_, name_, symbol_,
        company_cn, company_en, list_date_, delist_date_,
        market_, board_,
    ]


class price:
    open_ = 'open'
    close_ = 'close'
    high_ = 'high'
    low_ = 'low'
    volume_ = 'volume'
    amount_ = 'amount'
    pre_close_ = 'pre_close'
    pct_change_ = 'pct_change'
    vwap_ = 'vwap'
    limit_up_ = 'limit_up'
    limit_down_ = 'limit_down'
    status_ = 'status'
    all_ = [
        open_, close_, high_, low_, volume_, amount_,
        pre_close_, pct_change_, vwap_, limit_up_, limit_down_, status_,
    ]


class shares:
    total_shares_ = 'total_shares'
    float_shares_ = 'float_shares'
    total_cap_ = 'total_cap'
    float_cap_ = 'float_cap'
    turnover_ = 'turnover'
    all_ = [
        total_shares_, float_shares_, total_cap_, float_cap_, turnover_
    ]


class industry:
    code_ = 'code'
    time_ = 'name'
    ind_code_ = 'ind_code'
    ind_name_ = 'ind_name'
    list_date_ = 'list_date'
    source_ = 'source'
    all_ = [
        code_, time_, ind_code_, ind_name_, list_date_, source_
]
