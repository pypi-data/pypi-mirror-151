from django.db import models


class Phenotype(models.Model):
    # HPO syntax for id: HP:5000046, id: HP:0000001, ...
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=2000)
    comment = models.TextField(blank=True, null=True)
    definition = models.TextField(blank=True, null=True)
    '''
        synonyms: una lista di sinonimi, al momento solo in inglese
        {
          'en': ['', '', '', '']
        }
    '''
    synonyms = models.JSONField(blank=True, null=True)
    '''
        lista di riferimenti con la sintassi:
        ['MSH:D021782', 'SNOMEDCT_US:204962002', 'SNOMEDCT_US:82525005', 'UMLS:C3714581']
    '''
    xrefs = models.JSONField(blank=True, null=True)
    is_a = models.ManyToManyField('Phenotype')
    top_parent = models.ForeignKey('Phenotype', related_name='descendants', on_delete=models.CASCADE)
    # top_parents are the first level children of Phenotypic abnormality 'HP:0000118'
    #   Abnormal cellular phenotype
    #   Abnormality of blood ...
    #   Abnormality of head or neck
    #   ...
    #   ...
    # They are stored (breaking db normalization) in each node so that queries can efficiently filter by them
    # https://bioportal.bioontology.org/ontologies/HP/?p=classes&conceptid=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FHP_0000118
    # HPO is a graph; as of may 2022 there are no nodes that belong to different top parent nodes.
    # So a FK is sufficient.

    def __str__(self):
        return "%s - %s" % (self.id, self.name)

    def str_html(self):
        return '<a href="https://hpo.jax.org/app/browse/term/%s" target="_blank">%s</a>' % (self.id, self)
