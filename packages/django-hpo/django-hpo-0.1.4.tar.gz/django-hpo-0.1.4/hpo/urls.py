#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.urls import path
from hpo import api


urlpatterns = [
    path( r'phenotype/', api.phenotype, name='phenotype'),
    path( r'phenotype_top_parents/', api.phenotype_top_parents, name='phenotype_top_parents')
]
