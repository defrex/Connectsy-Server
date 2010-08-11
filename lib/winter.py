"""
Copyright (c) 2010 Patrick Stein, Connectsy Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

'''
Winter
======
Simple migrations.

Motivation
----------
Basically, you gotta handle schema changes.  This can be a bit of a hassle
with a document-based database like CouchDB, MongoDB, etc.  Winter helps ease
the pain by providing a straightforward and simple way to automatically handle
those changes.  It doesn't enforce a schema; it just lets you handle the
inevitable changes in document structure however you want to.

Usage
=====
Winter works with dict-like objects.

    #tells winter about a new object type
    winter.add('cricket')
    
    #first migration
    m = winter.migrate('cricket')
    m.add(foo='bar')
    
    #second migration
    m = winter.migrate('cricket')
    m.rename(foo='baz')
    m.add(looks='butt ugly', intelligence='rather low')
    
    # Alternatively
    #    winter.migrate('cricket').rename(foo='baz').add(looks='butt ugly',
    #        intelligence='rather low')
    # This works because all migration methods return the migration, allowing
    # calls to be chained.
    
    #builds out a new cricket objects
    cricket = winter.objects.cricket({})
    
Changes are applied in the order they're defined.  Available changes:

 - add(name='default_value')
 - delete('field1', 'field2')
 - rename(original_name='new_name')
 - modify(field=lambda a: a + ' modified!')
    
Once objects are built out, they have a revision number attached to
them (called '_winter').  When more transitions are added in the future, 
that object will only be updated with transitions there were added
after its revision number.  This allows Winter to migrate objects
pulled from a database, for example.

When working with multiple developers who need to make schema changes
to the same object, they should all work off of one migration file, and simply
add their changes to the bottom.  When they merge their changes back with
trunk (or master, if you're a git), they just need to merge in order and all
is well.  The migration file defines the process.
'''

import uuid
import hashlib

class MigrationManager(object):
    def __init__(self, name):
        #revisions is a dict from revision id to the next revision id
        #in sequence
        self.revisions  = {}
        #migrations is a dict from revision to migration
        self.migrations = {}
        self.base_hash = hashlib.sha1()
        self.base_hash.update(name)
        self.name = name
        #newest revision
        self.head = self.base_hash.hexdigest()

    def add(self, migration):
        '''
        Adds a new migration to the chain.
        '''
        #create a new hash for this migration
        new_rev = self.base_hash.copy()
        new_rev.update(str(len(self.revisions)))
        new_rev = new_rev.hexdigest()
        #update the revision trail
        self.revisions[self.head] = new_rev
        #and assign this new revision to head
        self.head = new_rev

        #store this migration
        self.migrations[new_rev] = migration
        
    def migrate(self, obj):
        '''
        Migrates an object from its current revision to the latest
        revision.
        '''
        if not '_winter' in obj:
            obj['_winter'] = self.base_hash.copy().hexdigest()
            
        rev = obj['_winter']
        while rev != self.head:
            #sanity check on the revision
            if not rev in self.revisions:
                raise Exception, "Dead end revision %s" % rev
                
            #grab the revision following the obj's revision
            rev = self.revisions[rev]
            #update the object to this revision
            self.migrations[rev].apply(obj)
            obj['_winter'] = rev
            
            
class Migration(object):

    # These class methods perform the actual actions
    @classmethod
    def _add(cls, obj, field, value):
        obj[field] = value
    
    @classmethod
    def _delete(cls, obj, field):
        del obj[field]
    
    @classmethod
    def _rename(cls, obj, field, name):
        obj[name] = obj[field]
        del obj[field]
    
    @classmethod
    def _modify(obj, field, f):
        obj[field] = f(obj[field])

    # We now return you to your regularly scheduled class    
    def __init__(self):
        self._actions = []


    def add(self, **kwargs):
        '''
        Adds fields, using key/value pairs.
        '''
        for field, value in kwargs.iteritems():
            self._actions.append((Migration._add, field, value))
        return self
        
    def delete(self, *args):
        '''
        Deletes fields.
        '''
        for field in args:
            self._actions.append((Migration._delete, field))
        return self
        
    def rename(self, **kwargs):
        '''
        Renames fields
        '''
        for name1, name2 in kwargs.iteritems():
            #sanity check
            if name1 == name2:
                raise Exception('Attempting to rename field "%s" to the same name' % name1)
            self._actions.append((Migration._rename, name1, name2))
        return self
        
    def modify(self, *args, **kwargs):
        '''
        Modifies fields with an arbitrary function.
        
        More docs TODO
        '''
        for field, f in kwargs.iteritems():
            #sanity check
            if not iscallable(f):
                raise Exception('Must supply a callable as a modifier for field %s' % field)
            self._action.append((Migration._modify, field, f))
        return self
    
    def apply(self, obj):
        '''
        Applies the revision to an object.
        '''
        
        #apply the actions
        for action in self._actions:
            action[0](obj, *action[1:])
            
        return self
        
class WinterObjects(object):
    def __init__(self):
        self._cache = {}

    def __getattr__(self, key):
        if not key in managers:
            raise Exception("Winter doesn't have '%s' registered" % key)
        elif key in self._cache:
            return self._cache[key]
        else:
            def migrator(obj):
                managers[key].migrate(obj)
                return obj
            self._cache[key] = migrator
            return migrator
            
    def __contains__(self, key):
        return key in managers
        
managers = {}
objects = WinterObjects()

def add(name):
    '''
    Creates an object in Winter with the given name
    '''
    #make sure this object isn't already added
    if name in managers:
        raise Exception("Object '%s' already added" % name)
        
    managers[name] = MigrationManager(name)
    
def migrate(name):
    '''
    Creates a new revision for the specified object with the given name
    '''
    if not name in managers:
        raise Exception("Object '%s' not registered with Winter; did you forget to call winter.add('%s')?" % s)
    
    m = Migration()
    managers[name].add(m)
    return m
    
# Test suite
if __name__ == '__main__':
    print 'Testing Winter...'

    # This is a pretty minimal test, but it should cover the majority of
    # the functionality.
    o = {}
    
    add('test1')
    
    # Addition!
    migrate('test1').add(a='a', b='b')
    o = objects.test1(o)
    
    assert 'a' in o
    assert o['a'] == 'a'
    assert 'b' in o
    assert o['b'] == 'b'
    
    # Renaming!
    migrate('test1').rename(a='c')
    o = objects.test1(o)
    
    assert not 'a' in o
    assert 'c' in o
    assert o['c'] == 'a'
    assert 'b' in o
    assert o['b'] == 'b'
    
    # Deletion!
    migrate('test1').delete('b')
    o = objects.test1(o)
    assert not 'b' in o
    
    # Modification!
    # TODO :(
    
    
    print 'Glorious Sucess'
    