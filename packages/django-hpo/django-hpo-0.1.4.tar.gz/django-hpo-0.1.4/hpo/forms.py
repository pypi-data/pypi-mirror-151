#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms


class PhenotypeInput(forms.Widget):
    template_name = 'hpo/widgets/phenotype.html'

    def __init__(self, attrs=None):
        super(PhenotypeInput, self).__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        """
        Returns this Widget rendered as HTML, as a Unicode string.
        """
        context = self.get_context(name, value, attrs)
        if value is not None:
            from hpo.models import Phenotype
            try:
                context['phenotype'] = Phenotype.objects.get(pk=value)
            except:
                pass
        return self._render(self.template_name, context, renderer)


class PhenotypeMultipleInput(forms.Widget):
    # esempio di widget fatto per gestire dei valori multipli
    # prima di tutto c'è da tener presente che il campo ManyToMany del model è fatto per interagire con l'outp della
    # select multipla in html. Questo significa che si aspetta una lista di valori con lo stesso nome, ad esempio:
    # ?valori=1&valori=2&valori=5
    # c'è da notare che lo stesso output in una form si può ottenere definendo n campi di input (o n select singole) con lo stesso nome
    # quindi l'idea è di utilizzare n volte il widget del PhenotypeInput dando lo stesso nome a tutte le copie del widget
    # lasciando che la gestione del dato lato server rimanga quella normale dei campi m2m
    #
    # oltre a questo, il widget prende in input min_objects, max_objecs, required

    template_name = 'hpo/widgets/phenotype_multiple.html'

    def __init__(self, attrs=None):
        super(PhenotypeMultipleInput, self).__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        """
        Returns this Widget rendered as HTML, as a Unicode string.
        """
        context = self.get_context(name, value, attrs)
        if value is not None:
            from hpo.models import Phenotype
            try:
                context['phenotypes'] = Phenotype.objects.filter(pk__in=value)
            except:
                pass
        return self._render(self.template_name, context, renderer)

