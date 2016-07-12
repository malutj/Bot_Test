from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Client ( models.Model ):
    client_name    = models.CharField  ( max_length = 50  )
    client_email   = models.EmailField (                  )
    client_page_id = models.CharField  ( max_length = 100 )

    def __str__ ( self ):
        return self.client_name


class Lead ( models.Model ):
    facebook_id  = models.CharField  ( max_length = 100 )
    first_name   = models.CharField  ( max_length = 30  )
    last_name    = models.CharField  ( max_length = 30  )
    email        = models.EmailField (                  )
    phone_number = models.CharField  ( max_length = 20  )

    client       = models.ForeignKey ( Client, on_delete=models.CASCADE )

    def __str__ ( self ):
        return ', '.join ([ self.last_name, self.first_name])

