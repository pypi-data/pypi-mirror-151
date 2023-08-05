from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from django.core.management import call_command
from io import StringIO
import json


class HpoTests(TestCase):
    def setUp(self):
        self.user = self.init_user('goofy')
        self.base_path = '/hpo/phenotype/?term='
        self.base_top_parent_path = '/hpo/phenotype_top_parents/'
        self.fake_agent = 'Mozilla/5.0'
        self.call_import_hpo_command()

    def init_user(self, username):
        usr, created = User.objects.get_or_create(username=username, last_name='Gota', first_name='Filippo')
        usr.set_password('lapassword')
        return usr

    def call_import_hpo_command(self, *args, **kwargs):
        out = StringIO()
        with self.settings(MAX_HPO_RECORDS=500):
            # MAX_HPO_RECORDS so that includes more than one top_parent
            print("wait for database initialization...")
            call_command(
                "import_hpo",
                *args,
                stdout=out,
                stderr=StringIO(),
                **kwargs,
            )
            print("database initialization finished.")
            return out.getvalue()

    def test_search_api_no_user(self):
        """check if AnonymousUser receive status code 302"""
        from hpo.api import phenotype
        rf = RequestFactory()
        request = rf.get(self.base_path + 'a', HTTP_USER_AGENT=self.fake_agent)
        request.user = AnonymousUser()
        response = phenotype(request)
        self.assertEquals(response.status_code, 302)

    def test_search_api(self):
        """check if api has status_code = 200 for authorized user"""
        from hpo.api import phenotype
        rf = RequestFactory()
        request = rf.get(self.base_path + 'a', HTTP_USER_AGENT=self.fake_agent)
        request.user = self.user
        request.session = {}
        response = phenotype(request)
        self.assertEquals(response.status_code, 200)

    def test_search_result(self):
        """check if it finds name in api results"""
        from hpo.api import phenotype
        from hpo.models import Phenotype
        pht = Phenotype.objects.all().order_by('name').first()
        rf = RequestFactory()
        request = rf.get(self.base_path + pht.name, HTTP_USER_AGENT=self.fake_agent)
        request.user = self.user
        request.session = {}
        response = phenotype(request)
        res = json.loads(response.content)
        self.assertEquals(res[0]['value'], pht.name)

    def get_top_parents(self):
        from hpo.api import phenotype_top_parents
        rf = RequestFactory()
        request = rf.get(self.base_top_parent_path, HTTP_USER_AGENT=self.fake_agent)
        request.user = self.user
        request.session = {}
        response = phenotype_top_parents(request)
        res = json.loads(response.content)
        return res

    def test_top_parents(self):
        res = self.get_top_parents()
        self.assertLessEqual(len(res), 23)

    def test_filter(self):
        from hpo.api import phenotype
        from hpo.models import Phenotype
        id_list = []
        top_parent = self.get_top_parents()[0]
        rf = RequestFactory()
        request = rf.get(self.base_path + '&top_parent=' + top_parent['id'], HTTP_USER_AGENT=self.fake_agent)
        request.user = self.user
        request.session = {}
        response = phenotype(request)
        res = json.loads(response.content)
        for r in res:
            id_list.append(r['id'])
        self.assertLessEqual(len(res), Phenotype.objects.filter(id__in=id_list, top_parent_id=top_parent['id']).count())
