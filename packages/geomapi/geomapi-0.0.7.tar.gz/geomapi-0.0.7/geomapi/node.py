"""
Node - a Python Class to govern the data and metadata of remote sensing data (pcd, images, meshes, orthomozaik)
"""

#IMPORT PACKAGES
from ast import Try
from logging import NullHandler
from pathlib import Path
from typing import Type
from typing_extensions import Self
from urllib.request import ProxyBasicAuthHandler
import xml.etree.ElementTree as ET
from xmlrpc.client import Boolean 
import open3d as o3d 
# from pathlib import Path # https://docs.python.org/3/library/pathlib.html
import numpy as np 
import os
import sys
import re
from typing import List
import uuid    

import math
import rdflib #https://rdflib.readthedocs.io/en/stable/
# from rdflib.serializer import Serializer #pip install rdflib-jsonld https://pypi.org/project/rdflib-jsonld/
from rdflib import Graph
from rdflib import URIRef, BNode, Literal
from rdflib.namespace import CSVW, DC, DCAT, DCTERMS, DOAP, FOAF, ODRL2, ORG, OWL, \
                           PROF, PROV, RDF, RDFS, SDO, SH, SKOS, SOSA, SSN, TIME, \
                           VOID, XMLNS, XSD
from rdflib.term import _is_valid_uri

# import pye57 #conda install xerces-c  =>  pip install pye57
from scipy.spatial.transform import Rotation as R

#IMPORT MODULES
import geomapi.utils as ut

SUPPORTED_POINT_FIELDS = {
    "name": "(string)",
    "guid": "(string)",
    "sessionName": "(string)",
    "timestamp": "(string)",
    "sensor": "(string)",
    "CartesianBounds": "(float nparray [6x1) [xMin,xMax,yMin,yMax,zMin,zMax]",
    "accuracy": "(float)",
    "cartesianTransform": "(float nparray [4x4]) 3D transform including location, scale and rotation",
    "geospatialTransform": "(float nparray [3x1]) ellipsoidal WGS84 coordinate system {latitude (+=East), longitude(+=North), altitude (+=Up)}",
    "coordinateSystem": "(string) Lambert72, Lambert2008, geospatial-wgs84, local",
    "path": "(string) relative path to the RDF graph folder",
    "graph": "(Graph) RDFLIB ",
    }

class Node:

    def __init__(self):
        #instance attributes
        self.name = None          # (string) name of the node
        self.subject =None
        self.guid=str(uuid.uuid1())
        # self.guid = None          # (string) guid of the node
        # self.sessionName = None   # (string) session node name
        # self.timestamp = None     # (string) e.g. 2020-04-11 12:00:01 UTC
        # self.sensor = None        # (string) sensor information P30, BLK, Hololens2, CANON, etc.

        # #Geometry
        # self.cartesianBounds=None     # (nparray [6x1]) [xMin,xMax,yMin,yMax,zMin,zMax]
        # self.orientedBounds = None    # (nparray [8x3]) 
        # self.accuracy = None          # (float) metric data accuracy e.g. 0.05m

        # #Coordinate system information
        # self.cartesianTransform=None  # (nparray [4x4]) 3D transform including location, scale and rotation 
        # self.geospatialTransform=None # (nparray [3x1]) ellipsoidal WGS84 coordinate system {latitude (+=East), longitude(+=North), altitude (+=Up)}
        # self.coordinateSystem = None  # (string) coordinate system i.e. Lambert72, Lambert2008, geospatial-wgs84, local + reference /offset
  
        # #paths
        # self.path = None # (string) absolute path to the node
        # self.sessionPath =None # (string) absolute path to the session folder
        # self.graphPath= None # (string) absolute path to the folder with the RDF graph 
        
        # #metadata
        # self.graph = None # (Graph) rdflib

        # #Relations
        # self.hasPcd = None #(List[URIRef]) link to observed pcd of the node (MB)
        # self.hasMesh = None #(List[URIRef]) link to observed meshes of the node (MB)
        # self.hasOrtho = None #(List[URIRef]) link to observed orthomosaics of the node (MB)
        # self.hasImg = None #(List[URIRef]) link to observed images of the node (MB)
        # self.hasCAD= None #do we want to establish such a link?
        # self.hasBIM=None #(List[URIRef]) link to BIMNodes that also represent this node (MB)


    def get_metadata_from_graph(self):
        """Convert a graph to a set of Nodes

        Args:
            graph (RDFlib.Graph):  Graph to parse
            sessionPath (str): folder path of the session    
            or
            graphPath (str): folder path of the graph    

        Returns:
            A Node with metadata
        """
        self.subject=next(self.graph.subjects()) 
        self.name = str(self.subject).replace('http://','') 

        for predicate, object in self.graph.predicate_objects(subject=self.subject):
            attr=ut.predicate_to_attribute(predicate)
            #GEOMETRY
            if attr == 'cartesianBounds':
                self.cartesianBounds=ut.literal_to_cartesianBounds(self.graph.value(subject=self.subject,predicate=predicate)) 
            elif attr == 'orientedBounds':
                self.orientedBounds=ut.literal_to_orientedBounds(self.graph.value(subject=self.subject,predicate=predicate)) 
            elif attr == 'cartesianTransform':
                self.cartesianTransform=ut.literal_to_cartesianTransform(self.graph.value(subject=self.subject,predicate=predicate))
            elif attr == 'geospatialTransform':
                self.geospatialTransform=ut.literal_to_geospatialTransform(self.graph.value(subject=self.subject,predicate=predicate))
            #PATHS
            elif re.search('path', attr, re.IGNORECASE):
                path=ut.literal_to_string(self.graph.value(subject=self.subject,predicate=predicate))
                if path is not None:
                    setattr(self,attr,(self.get_folder_path()+'\\'+path)) 
                    # if getattr(self,'graphPath',None) is not None:
                    #     setattr(self,attr,(self.graphPath+'\\'+path)) 
                    # elif getattr(self,'sessionPath',None) is not None:
                    #     setattr(self,attr,(self.sessionPath+'\\'+path))    
                    # else:
                    #     setattr(self,attr,(os.getcwd()+'\\'+path))   
            #INT    
            elif attr in ['recordCount','faceCount','label','e57Index']:
                setattr(self,attr,ut.literal_to_int(object)) 
            #FLOAT
            elif attr in ['xResolution','yResolution','imageWidth','imageHeight','focalLength35mm','principalPointU','principalPointV','accuracy']:
                setattr(self,attr,ut.literal_to_float(object)) 
            #LISTS
            elif attr in ['hasBIM','hasCAD','hasPcd','hasMesh','hasImg','hasOrtho','hasChild','hasParent','distortionCoeficients']:
                setattr(self,attr,ut.literal_to_list(object)) 
            #STRINGS
            else:
                setattr(self,attr,object.toPython()) # this solely covers string

    def get_metadata_from_graph_path(self):
        g=Graph()
        g=g.parse(self.graphPath) 
        myGraph=Graph()
        if getattr(self,'subject',None) is None: 
            subject=next(g.subjects()) 
            myGraph += g.triples((subject, None, None))
        else:
            myGraph += g.triples((self.subject, None, None))        
        self.get_metadata_from_graph()

    def get_triples(self,graph:Graph, subject:URIRef = None):
        if subject is not None:
            g=Graph()
            self.graph += g.triples((subject, None, None))
        elif getattr(self,'subject',None) is not None:
            g=Graph()
            self.graph += g.triples((self.subject, None, None))
        else:
            g=Graph()
            subject=next(graph.subjects()) 
            self.graph += g.triples((subject, None, None))

    def get_name(self) :
        if getattr(self,'name',None) is not None:
            self.name=ut.check_string_validity(self.name)            
        else:            
            self.name = self.guid

    def get_subject(self):
        if getattr(self,'subject',None) is not None:
            if _is_valid_uri(self.subject):            
                pass
            else:
                self.subject= URIRef('http://'+ut.check_string_validity(self.subject))
        else:
            self.get_name()
            self.subject= URIRef('http://'+self.name)

    def get_folder_path(self) -> str:
        if getattr(self, 'graphPath',None) is not None: 
            folderPath=self.graphPath
        elif getattr(self, 'sessionPath',None) is not None:
            folderPath=self.sessionPath
        else:
            folderPath=os.getcwd()
        return folderPath

    def to_graph(self):
        """
        Register all parameters to RDF graph
        """
        self.get_subject()  
        # if graph does not exist => create graph
        if getattr(self,'graph',None) is None : 
            graph=Graph()              
            self.graph=ut.bind_ontologies(graph)             
            self.graph.add((self.subject, RDF.type, Literal(str(type(self)))))
  
        # enumerate attributes in node and write them to triples
        attributes = ut.get_variables_in_class(self)
        attributes=ut.clean_attributes_list(attributes)        
        pathlist=ut.get_paths_in_class(self)
              
        for attribute in attributes: 
            value=getattr(self,attribute)
            if value is not None and attribute not in pathlist:
                #find appropriete RDF URI
                predicate = ut.match_uri(attribute)
                # Add triple to graph
                self.graph.add((self.subject, predicate, Literal(str(value))))
            elif value is not None and attribute in pathlist:
                predicate = ut.match_uri(attribute)
                folderPath=self.get_folder_path()
                relpath=os.path.relpath(value,folderPath)
                self.graph.add((self.subject, predicate, Literal(relpath)))

    def get_path(self):
        """
        Get resource (full) path
        """
        allSessionFilePaths=ut.getListOfFiles(self.sessionPath) 
        for path in allSessionFilePaths:
            if self.name in path:
                self.path=path
                return True
        return False   
    
