from django.test import TestCase
from test_bot.models import Lead

# Create your tests here.
class LeadTests ( TestCase ):

    def test_string ( self ):
        lead = Lead ( first_name = 'Jason', last_name = 'Malutich' )
        self.assertEquals ( str ( lead ), 'Jason Malutich' )
