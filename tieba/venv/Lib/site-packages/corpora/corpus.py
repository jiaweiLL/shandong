# -*- coding: utf-8 -*-

import os
import yaml
from struct import pack, unpack

try:
    from bsddb3 import btopen, hashopen, rnopen
except ImportError:
    from bsddb import btopen, hashopen, rnopen
    

class Corpus:
    '''Corpus class is responsible for creating new corpus and also represents a corpus as an object'''
    CHUNK_PREFIX='chunk'
    CONFIG_FILE='config'
    IDX_FILE='idx'
    RIDX_FILE='ridx'
    IDX_BYTEO='!QIII'
    RIDX_BYTEO="!Q"
    
    def __init__(self, path):
        self.corpus_path = path
        self.chunks = {}
        self.idx = rnopen(os.path.join(self.corpus_path, Corpus.IDX_FILE))  #FIXME: issue #2 this should be implemented with bsddb3 Queue
        self.ridx = hashopen(os.path.join(self.corpus_path, Corpus.RIDX_FILE))
        self.properties = yaml.load(file(os.path.join(self.corpus_path, Corpus.CONFIG_FILE), 'r'))
    
    def __len__(self):
        '''Returns size of document collection'''
        return self.idx.db.stat()['nkeys']  #FIXME: issue #1 find more elegant bsddb3 to 
    
    def __getitem__(self, key):
        '''Interface for get method'''
        return self.get(key)
    
    def __iter__(self):
        for e in self.idx:
            yield self.get_by_idx(self.get_idx(e))
            
    
    def get_property(self, prop):
        return self.properties[prop]
        
    def set_property(self, prop, val):
        self.properties[prop] = val
    
    def get_ridx(self, key):
        '''Return index of idx for given ``key``'''
        return unpack(Corpus.RIDX_BYTEO, self.ridx[str(key)])[0]
        
    def get_idx(self, index):
        '''Return tuple (chunk, offset, header len, text len) for given ``index``'''
        return unpack(Corpus.IDX_BYTEO, self.idx[index])
        
    @staticmethod
    def create( path, **properties ):
        '''Static method for creating new corpus in the given ``path``. Additional
        properties can be given as named arguments. '''
        os.makedirs(path)
        if not properties.has_key('chunk_size') :
            properties['chunk_size'] = 1024
        if not properties.has_key('encoding') :
            properties['encoding'] = 'utf-8'
        properties['current_chunk'] = 0
        
        yaml.dump(properties, file(os.path.join(path, Corpus.CONFIG_FILE), 'w'), default_flow_style=False)
        file(os.path.join(path, Corpus.CHUNK_PREFIX + "0"), 'w').close()
    
    def save_config(self):
        '''Saving properties of corpora to config file.'''
        yaml.dump(self.properties, file(os.path.join(self.corpus_path, Corpus.CONFIG_FILE), 'w'), default_flow_style=False)

    def save_indexes(self):
        '''Saving all indexes to apropriate files.'''
        self.idx.sync()
        self.ridx.sync()
    
    def make_new_chunk(self):
        '''Creates new chunk with next sequential chunk number.'''
        self.set_property('current_chunk' , self.get_property('current_chunk') + 1 )
            
        try:
            file(os.path.join(self.corpus_path, Corpus.CHUNK_PREFIX + str(self.get_property('current_chunk'))), 'w').close()
        except IOError, err:
                # Dealing with "too many files opened"
                if err.errno == 24:
                    self.chunks = {}
                    file(os.path.join(self.corpus_path, Corpus.CHUNK_PREFIX + str(self.get_property('current_chunk'))), 'w').close()
                else:
                    raise err
        self.save_config()
    
    def test_chunk_size(self, new_size):
        '''Tests if ``new_size`` data will fit into current chunk.'''
        chunk = self.get_chunk()
        chunk.seek(0,2)
        chunk_size = chunk.tell()
        if new_size > self.get_property('chunk_size'):
            raise Corpus.ExceptionTooBig()
        return chunk_size + new_size <=  self.get_property('chunk_size')
        
    def get_chunk(self, number=None):
        '''Getter for chunk. Default chunk is current_chunk. Method caches opened chunk files.'''
        if number is None:
            number = self.get_property('current_chunk')
        if self.chunks.has_key(number):
            return self.chunks[number]
        else:
            try:
                self.chunks[number] = file(os.path.join(self.corpus_path, Corpus.CHUNK_PREFIX + str(number)), 'r+b')
                return self.chunks[number]
            except IOError, err:
                # Dealing with "too many files opened"
                if err.errno == 24:
                    self.chunks = {}
                    self.chunks[number] = file(os.path.join(self.corpus_path, Corpus.CHUNK_PREFIX + str(number)), 'r+b')
                    return self.chunks[number]
                else:
                    raise err
    def add(self, text, ident, **headers):
        '''Appending new document to a corpus.'''
        if self.ridx.has_key(str(ident)):
            raise Corpus.ExceptionDuplicate()
        
        headers['id'] = ident
        headers_str = yaml.dump(headers, default_flow_style=False)
        text_str = text.encode(self.get_property('encoding'))  + "\n\n"

        if not self.test_chunk_size(len(headers_str) + len(text_str)) :
            self.make_new_chunk()
        
        chunk = self.get_chunk()
        chunk.seek(0,2)
        index = self.idx.db.append(
                    pack(               Corpus.IDX_BYTEO,
                                        self.get_property('current_chunk') , 
                                        chunk.tell(), 
                                        len(headers_str), 
                                        len(text_str)
                                )
                    )
        self.ridx[str(ident)] = pack(Corpus.RIDX_BYTEO, index)
        chunk.write(headers_str)
        chunk.write(text_str)
        chunk.flush()

    def get(self, ident):
        '''Get random document from a corpus.'''
        if not self.ridx.has_key(str(ident)):
            raise IndexError('Not found')
        return self.get_by_idx(self.get_idx(self.get_ridx(ident)))
        
    def get_by_idx(self, idx):
        '''Get document pointed by ``idx`` structure which is offset information in chunk file.'''
        (chunk_number, offset, head_len, text_len) = idx
        chunk = self.get_chunk(chunk_number)
        chunk.seek(offset,0)
        head = chunk.read(head_len)
        text = chunk.read(text_len)[:-2]    #stripping two end-of-lines
        return (yaml.load(head) , text.decode(self.get_property('encoding')))
        
            
    class ExceptionTooBig(Exception):
        '''Exception raised when document is to big to fit chunk file.'''
        pass
    class ExceptionDuplicate(Exception):
        '''Exception raised when appending document with duplicate ``id``'''
        pass    