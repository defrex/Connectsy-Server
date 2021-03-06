'''
Set up indexes here.

This file is automatically run when the database connection is
initialized.
'''
import pymongo

indexes = {}

indexes['event'] = {
    # Geospacial index for events.  Note that this currently is NOT shardable!
    # From the bugtracker it looks like they're aiming for 1.7 with this one,
    # but we'll want to wait for the stable 1.8 release.  
    u'posted_from': pymongo.GEO2D,
}