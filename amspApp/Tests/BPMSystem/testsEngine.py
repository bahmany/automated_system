import json
import os
import uuid
from django.core.wsgi import get_wsgi_application
from django.test.utils import setup_test_environment
from django.utils import unittest


class MyEngineTests(unittest.TestCase):
    def setUp(self):
        os.environ['DJANGO_SETTINGS_MODULE'] = 'amspApp.Tests.settings'
        # from mongoengine import connect

        # connect("amsPlusMongo")
        application = get_wsgi_application()
        # settings.configure(_settings)
        setup_test_environment()


    def test_create_instance_of_MyEngnine_class(self):
        """
        Scenario: this test check creating(__init__) instance of MyEngine class
        :return:
        """

        from amspApp.BPMSystem.MyEngine.BpmEngine import BpmEngine
        from amspApp.Bpms.models import LunchedProcess

        lp_instance = LunchedProcess.objects.all()
        newEngine = BpmEngine(lp_instance[34])


    def test_run_of_MyEngine_class(self):
        """
        Scenario: check run() function of MyEngine class
        :return:
        """

        from amspApp.BPMSystem.MyEngine.BpmEngine import BpmEngine
        from amspApp.Bpms.models import LunchedProcess

        lp_instance = LunchedProcess.objects.all()
        newEngine = BpmEngine(lp_instance[34]).run()

    def test_of_get_this_performers_MyEngine_class(self):
        """
        Scenario: check get_this_performers() function of MyEngine class
        :return:
        """

        from amspApp.BPMSystem.MyEngine.BpmEngine import BpmEngine
        from amspApp.Bpms.models import LunchedProcess

        lp_instance = LunchedProcess.objects.all()
        newEngine = BpmEngine(lp_instance[34]).get_this_performers(lp_instance)






