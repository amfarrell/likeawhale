#!/usr/bin/env python
# -*- coding: utf-8 -*-

import httplib
import json
import re
import socket
import urllib
import os

from itertools import groupby
from operator import itemgetter
from contextlib import contextmanager


#regex patterns for various tagging options for entity parsing
SLASHTAGS_EPATTERN  = re.compile(r'(.+?)/([A-Z]+)?\s*')
XML_EPATTERN        = re.compile(r'<wi num=".+?" entity="(.+?)">(.+?)</wi>')
INLINEXML_EPATTERN  = re.compile(r'<([A-Z]+?)>(.+?)</\1>')

CHINESE_SEGMENTER_PORT = int(os.getenv('CHINESE_SEGMENTER_PORT'))



@contextmanager
def tcpip4_socket(host, port):
    """Open a TCP/IP4 socket to designated host/port."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
      s.connect((host, port))
      yield s
    finally:
      s.shutdown(socket.SHUT_RDWR)
      s.close()

class Seg(object):
    """Wrapper for server-based Stanford Word Segmenter."""
    
    def tag_text(self, text):
        pass

    def __slashTags_parse_entities(self, tagged_text):
        """Return a list of token tuples (entity_type, token) parsed
        from slashTags-format tagged text.
        
        :param tagged_text: slashTag-format entity tagged text
        """
        return (match.groups()[::-1] for match in
            SLASHTAGS_EPATTERN.finditer(tagged_text))

    def __xml_parse_entities(self, tagged_text):
        """Return a list of token tuples (entity_type, token) parsed
        from xml-format tagged text.
           
        :param tagged_text: xml-format entity tagged text
        """
        return (match.groups() for match in
            XML_EPATTERN.finditer(tagged_text))

    def __inlineXML_parse_entities(self, tagged_text):
        """Return a list of entity tuples (entity_type, entity) parsed
        from inlineXML-format tagged text.
        
        :param tagged_text: inlineXML-format tagged text
        """
        return (match.groups() for match in
            INLINEXML_EPATTERN.finditer(tagged_text))

    def __collapse_to_dict(self, pairs):
        """Return a dictionary mapping the first value of every pair
        to a collapsed list of all the second values of every pair.
    
        :param pairs: list of (entity_type, token) tuples
        """
        return dict((first, map(itemgetter(1), second)) for (first, second)
            in groupby(sorted(pairs, key=itemgetter(0)), key=itemgetter(0)))

    def get_entities(self, text):
        """Return all the named entities in text as a dict.
    
        :param text: string to parse entities
        :returns: a dict of entity type to list of entities of that type
        """
        tagged_text = self.tag_text(text)
        if self.oformat == 'slashTags':
            entities = self.__slashTags_parse_entities(tagged_text)
            entities = ((etype, " ".join(t[1] for t in tokens)) for (etype, tokens) in
                groupby(entities, key=itemgetter(0)))
        elif self.oformat == 'xml':
            entities = self.__xml_parse_entities(tagged_text)
            entities = ((etype, " ".join(t[1] for t in tokens)) for (etype, tokens) in
                groupby(entities, key=itemgetter(0)))
        else: #inlineXML
            entities = self.__inlineXML_parse_entities(tagged_text)
        return self.__collapse_to_dict(entities)

    def json_entities(self, text):
        """Return a JSON encoding of named entities in text.
        
        :param text: string to parse entities
        :returns: a JSON dump of entities parsed from text
        """
        return json.dumps(self.get_entities(text))


class SocketSeg(Seg):
    """Stanford Word Segmenter over simple TCP/IP socket."""

    def __init__(self, host='localhost', port = CHINESE_SEGMENTER_PORT, output_format='inlineXML'):
        if output_format not in ('slashTags', 'xml', 'inlineXML'):
            raise ValueError('Output format %s is invalid.' % output_format)
        self.host = host
        self.port = port
        self.oformat = output_format

    def segment_text(self, text):
        #for s in ('\f', '\n', '\r', '\t', '\v'): #strip whitespaces
        #    text = text.replace(s, '')
        #text += '\n' #ensure end-of-line
        try :
          text = text.encode('utf-8')
        except UnicodeDecodeError:
          pass
        with tcpip4_socket(self.host, self.port) as s:
            print text + '\n'
            s.sendall(text)
            tagged_text = s.recv(10*len(text)).decode('utf-8')
            print tagged_text + '\n'
        return tagged_text

if __name__ == '__main__':
  client = SocketSeg()
  print client.segment_text("英格蘭足總盃\n")


