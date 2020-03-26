# -*- coding: utf-8 -*-
import unittest, os
import sys
sys.path.append("..")
from corpora import Corpus
import shutil


class TestCorpus(unittest.TestCase):
    def setUp(self):
        try:
            shutil.rmtree('/tmp/TEST_CORPUS')
        except:
            pass

    def test_create(self):
        Corpus.create('/tmp/TEST_CORPUS', name=u"Fancy name")
        c = Corpus('/tmp/TEST_CORPUS')
        self.assertEqual(c.get_property('name'), u'Fancy name')
        self.assertEqual(c.get_property('current_chunk'), 0)
        self.assertTrue(os.path.isfile(os.path.join('/tmp/TEST_CORPUS/' , Corpus.CONFIG_FILE)))
        self.assertTrue(os.path.isfile(os.path.join('/tmp/TEST_CORPUS/' , Corpus.CHUNK_PREFIX + '0')))
        del c
        shutil.rmtree('/tmp/TEST_CORPUS')

    def test_save_config(self):
        Corpus.create('/tmp/TEST_CORPUS', name=u"Fancy name")
        c = Corpus('/tmp/TEST_CORPUS')    
        c.set_property('name', u"Not fancy")
        c.save_config()
        d = Corpus('/tmp/TEST_CORPUS')  
        self.assertEqual(d.get_property('name'), u"Not fancy")
        del c, d
        shutil.rmtree('/tmp/TEST_CORPUS')

    def test_make_new_chunk(self):
        Corpus.create('/tmp/TEST_CORPUS', name=u"Fancy name")
        c = Corpus('/tmp/TEST_CORPUS')
        c.make_new_chunk()
        d = Corpus('/tmp/TEST_CORPUS')
        
        self.assertEqual(d.get_property('current_chunk'), 1)
        self.assertTrue(os.path.isfile(os.path.join('/tmp/TEST_CORPUS/' , Corpus.CHUNK_PREFIX + '1')))
        
        del c, d
        shutil.rmtree('/tmp/TEST_CORPUS')
        
    def test_test_chunk_size(self):
        Corpus.create('/tmp/TEST_CORPUS', chunk_size=10)
        c = Corpus('/tmp/TEST_CORPUS')
        
        self.assertTrue(c.test_chunk_size(5))
        self.assertTrue(c.test_chunk_size(10))
        with self.assertRaises(Corpus.ExceptionTooBig):
            c.test_chunk_size(11)
        del c
        shutil.rmtree('/tmp/TEST_CORPUS')

    def test_get_chunk(self):
        Corpus.create('/tmp/TEST_CORPUS', chunk_size=10)
        c = Corpus('/tmp/TEST_CORPUS')
        self.assertIsNotNone(c.get_chunk())
        del c
        shutil.rmtree('/tmp/TEST_CORPUS')

    def test_add_get_duplicate(self):
        Corpus.create('/tmp/TEST_CORPUS')
        c = Corpus('/tmp/TEST_CORPUS')
        with self.assertRaises(Corpus.ExceptionDuplicate):
            c.add(u'Gżegżółką jaźń', 1, p1=1, p2="2", p3=[1,2,3,u'ą'])
            c.add(u'Gżegżółką jaźń', 1, p1=1, p2="2", p3=[1,2,3,u'ą'])
        del c
        shutil.rmtree('/tmp/TEST_CORPUS')

    def test_len(self):
        Corpus.create('/tmp/TEST_CORPUS')
        c = Corpus('/tmp/TEST_CORPUS')
        c.add(u'Gżegżółką jaźń', 1, p1=1, p2="2", p3=[1,2,3,u'ą'])
        c.add(u'Chrząszcz brzmi w czcinie', 2, p1=1, p2="2", p3=[1,2,3,u'ą'])                
        c.add(u'Żółte źrebie', 3, p1=1, p2="2", p3=[1,2,3,u'ą'])            
        self.assertEqual(len(c), 3)
        del c
        shutil.rmtree('/tmp/TEST_CORPUS')        
            
    
    def test_add_get(self):
        Corpus.create('/tmp/TEST_CORPUS')
        c = Corpus('/tmp/TEST_CORPUS')
        c.add(u'Gżegżółką jaźń', 1, p1=1, p2="2", p3=[1,2,3,u'ą'])
        c.add(u'Chrząszcz brzmi w czcinie', 2, p1=1, p2="2", p3=[1,2,3,u'ą'])                
        c.add(u'Żółte źrebie', 3, p1=1, p2="2", p3=[1,2,3,u'ą'])  
        c.save_indexes()      
        d = Corpus('/tmp/TEST_CORPUS')
        self.assertEqual(d.get(3), (  { 'p1':1, 'p2':"2", 'p3':[1,2,3,u'ą'], 'id':3},  u'Żółte źrebie'   ) )
        self.assertEqual(d.get(1), (  { 'p1':1, 'p2':"2", 'p3':[1,2,3,u'ą'], 'id':1},  u'Gżegżółką jaźń'   ) )
        self.assertEqual(d.get(2), (  { 'p1':1, 'p2':"2", 'p3':[1,2,3,u'ą'], 'id':2},  u'Chrząszcz brzmi w czcinie'  ) )
        del c, d
        shutil.rmtree('/tmp/TEST_CORPUS')         


    def test_chunking(self):
        Corpus.create('/tmp/TEST_CORPUS', chunk_size=13)
        c = Corpus('/tmp/TEST_CORPUS')
        c.add(u'12345', 1)
        c.add(u'12345', 2)
        
        (chunk_number, offset, head_len, text_len) = c.get_idx(c.get_ridx(2))
        self.assertEqual(chunk_number, 1)
        
        del c
        shutil.rmtree('/tmp/TEST_CORPUS')           

    def test_add_too_big(self):
        Corpus.create('/tmp/TEST_CORPUS', chunk_size=12)
        c = Corpus('/tmp/TEST_CORPUS')
        with self.assertRaises(Corpus.ExceptionTooBig):
            c.add(u'12345', 1)
        del c
        shutil.rmtree('/tmp/TEST_CORPUS')           



    def test_getitem(self):
        Corpus.create('/tmp/TEST_CORPUS')
        c = Corpus('/tmp/TEST_CORPUS')
        c.add(u'Gżegżółką jaźń', 1, p1=1, p2="2", p3=[1,2,3,u'ą'])
        c.add(u'Chrząszcz brzmi w czcinie', 2, p1=1, p2="2", p3=[1,2,3,u'ą'])                
        c.add(u'Żółte źrebie', 3, p1=1, p2="2", p3=[1,2,3,u'ą'])            
        self.assertEqual(c.get(2), c[2])
        del c
        shutil.rmtree('/tmp/TEST_CORPUS')        
 
    def test_iter(self):
        Corpus.create('/tmp/TEST_CORPUS')
        c = Corpus('/tmp/TEST_CORPUS')
        c.add(u'Gżegżółką jaźń', 3, p1=1, p2="2", p3=[1,2,3,u'ą'])
        c.add(u'Chrząszcz brzmi w czcinie', 1, p1=1, p2="2", p3=[1,2,3,u'ą'])                
        c.add(u'Żółte źrebie', 2, p1=1, p2="2", p3=[1,2,3,u'ą'])  
        c.save_indexes()      
        d = Corpus('/tmp/TEST_CORPUS')
        l = []
        for t in d:
            l.append(t[0]['id'])
        self.assertEqual(l, [3,1,2])
        del c, d
        shutil.rmtree('/tmp/TEST_CORPUS')                 
        
        
        
if __name__ == '__main__':

    unittest.main()