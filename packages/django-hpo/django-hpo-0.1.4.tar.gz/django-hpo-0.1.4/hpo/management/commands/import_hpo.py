# -*- coding: utf-8 -*-

import logging, os, urllib.request, zipfile
from django.db import transaction
from django.core.management.base import BaseCommand
from hpo.models import Phenotype
from obonetx.ontology import Ontology
from django.conf import settings

logger = logging.getLogger(__name__)
max_records = getattr(settings, 'MAX_HPO_RECORDS', 0)


def import_hpo_node(hpo_node, hpo_as_dict, idx, parent=None, top_parent=None):
    try:
        if max_records and idx >= max_records:
            return idx
        id_ = hpo_node['id_']
        if Phenotype.objects.filter(id=id_).exists():
            ph = Phenotype.objects.get(id=id_)
        else:
            ph = Phenotype()
        ph.id = id_
        ph.name = hpo_node['name']
        if 'comment' in hpo_node:
            ph.comment = hpo_node['comment']
        if 'def' in hpo_node:
            ph.definition = hpo_node['def'][1 + hpo_node['def'].find('"'):hpo_node['def'].rfind('"')]
        if 'synonym' in hpo_node:
            ph.synonyms = [s[1 + s.find('"'):s.rfind('"')] for s in hpo_node['synonym']]
        if 'xref' in hpo_node:
            ph.xrefs = hpo_node['xref']
        if top_parent:
            ph.top_parent = top_parent
        else:
            ph.top_parent = ph
        ph.save()
        if parent:
            ph.is_a.add(parent)
        idx += 1
        hpo_node_children = [v for k, v in hpo_as_dict.items() if
                             ('is_a' in v.keys() and v['is_a'] == [id_])]
        for hpo_node in hpo_node_children:
            idx = import_hpo_node(hpo_node, hpo_as_dict, idx, ph, ph.top_parent)
        return idx
    except Exception as ex:
        pass


class Command(BaseCommand):
    help = '''Imports HPO Human Phenotype Onthology'''

    def handle(self, *args, **options):
        hpo_url = 'http://purl.obolibrary.org/obo/hp.obo'
        hpo = Ontology(hpo_url)
        idx = 0
        try:
            is_a_2bcompleted = []
            hpo_as_dict = dict(hpo.graph.nodes(data=True))
            # https://bioportal.bioontology.org/ontologies/HP/?p=classes&conceptid=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FHP_0000118
            # I want to get only what's under "Phenotypic abnormality"
            phenotypic_abnormality_id = 'HP:0000118'
            root_id = 'HP:0000001'
            for k, v in hpo_as_dict.items():
                v.update({'id_': k})
            root_children = [v for k, v in hpo_as_dict.items() if
                                               ('is_a' in v.keys() and v['is_a'] == [root_id])]
            phenotypic_abnormality_children = [v for k, v in hpo_as_dict.items() if
                                               ('is_a' in v.keys() and v['is_a'] == [phenotypic_abnormality_id])]
            for hpo_node in phenotypic_abnormality_children:
                idx = import_hpo_node(hpo_node, hpo_as_dict, idx)
        except Exception as ex:
            logger.error("Blocking error importing HPO Human Phenotype Onthology: %s" % str(ex))
        logger.info("END END END importing HPO Human Phenotype Onthology END END END")
