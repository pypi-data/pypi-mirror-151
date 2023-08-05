"""
ImageNode - a Python Class to govern the data and metadata of image data (JPG,PNG,XML,XMP)
"""
#IMPORT PACKAGES
import xml.etree.ElementTree as ET
import cv2
import PIL
from PIL.ExifTags import GPSTAGS, TAGS
from rdflib import Graph, URIRef
import numpy as np
import os
#IMPORT MODULES
from geomapi.node import Node
import geomapi.utils as ut
import geomapi.geometryutils as gt
import open3d as o3d
import math

SUPPORTED_POINT_FIELDS = {
    "xResolution": "(float)",
    "yResolution": "(float)",
    "resolutionUnit": "(float)",
    "imageWidth": "(float) number of pixels",
    "imageHeight": "(float) number of pixels",
    "focalLength35mm": "(float) focal length in mm",
    "principalPointU": "(float) u parameter of principal point (mm)",
    "principalPointV": "(float) v parameter of principal point (mm)",
    "distortionCoeficients": "(float[])",
    "features": "(float[])",
}

class ImageNode(Node):
    # class attributes
    
    def __init__(self,  graph : Graph = None, 
                        graphPath:str=None,
                        subject : URIRef = None,
                        path : str=None, 
                        xmpPath: str = None,
                        xmlPath: str = None,
                        xmlIndex: int = None,
                        getGeometry : bool = False,
                        img : np.ndarray  = None, 
                        **kwargs): 
        """
        Creates an ImageNode. Overloaded function.

        Args:
            0.graph (RDFlib Graph) : Graph with a single subject (if multiple subjects are present, only the first will be used to initialise the MeshNode)
            
            1.graphPath (str):  Graph file path with a single subject (if multiple subjects are present, only the first will be used to initialise the MeshNode)

            2.path (str) : path to .jpg or .png file (Note that this node will also contain the data)

            3.img (ndarray) : OpenCV image as numpy ndarray (Note that this node will also contain the data)
                
        Returns:
            A ImageNode with metadata (if you also want the data, call node.get_data() method)
        """  
         #instance attributes        
        super().__init__()   
        self.graph=graph
        self.graphPath=graphPath
        self.subject = subject
        self.path=path
        self.img = img
        self.xmpPath=xmpPath
        self.xmlPath=xmlPath
        self.xmlIndex=xmlIndex
        self.xResolution = None # (Float) 
        self.yResolution = None # (Float) 
        self.resolutionUnit = None # (string)
        self.imageWidth = None # (int) number of pixels
        self.imageHeight = None  # (int) number of pixels
        self.focalLength35mm = None # (Float) focal length in mm
        self.principalPointU= None # (Float) u parameter of principal point (mm)
        self.principalPointV= None # (Float) v parameter of principal point (mm)
        self.distortionCoeficients = None # (Float[])         
        # self.guid='{'+str(uuid.uuid1())+'}'     
        self.__dict__.update(kwargs)

        #data
        # self.exifData=None # (EXIF) optional exif data
        # self.features2d= None #o3d.registration.Feature() # http://www.open3d.org/docs/0.9.0/python_api/open3d.registration.Feature.html
      
        
        #Questions
        # where do we store the image masks?
        # where do we store depth maps?
        # where do we store undistorted images?
        # where do we store photogrammetric reconstructions => cartesian transform of the node?
        # where do we store polygon selections + classifications?
        # where do we store image classifications

        if graph is not None: 
            if type(graph) is Graph : #metadata
                self.get_metadata_from_graph() 
            else:
                raise ValueError('graph must be RDF Graph')

        elif graphPath is not None:  #metadata
            if graphPath.endswith('.ttl'):
                self.timestamp=ut.get_timestamp(graphPath)
                self.get_metadata_from_graph_path() 
            else:
                raise ValueError('file must be .ttl')        
        
        if path is not None:
            if path.endswith('.JPG') or path.endswith('.PNG'): #data + metadata
                self.name=ut.get_filename(path)
                self.timestamp=ut.get_timestamp(path)                
                self.get_metadata_from_exif_data()
            else:
                raise ValueError('file must be .JPG or .PNG')
       
        elif img is not None:
            if type(img) is np.ndarray: #data + metadata
                self.get_metadata_from_img()
            else:
                raise ValueError('variable must be OpenCV image')

        if xmpPath is not None:
            if xmpPath.endswith('.xmp'): #metadata
                self.name=ut.get_filename(xmpPath)
                self.timestamp=ut.get_timestamp(xmpPath)
                self.get_metadata_from_xmp()
            else:
                raise ValueError('file must be .xmp')
        
        elif xmlPath is not None and xmlIndex is not None:
            if xmlPath.endswith('.xml'): #metadata
                self.name=ut.get_filename(xmlPath)
                self.timestamp=ut.get_timestamp(xmlPath)
                self.get_metadata_from_xml()
            else:
                raise ValueError('file must be .xml')   

        if getGeometry:
                self.get_geometry()
                self.get_metadata_from_img()

    def clear_geometry(self):
        """Clear all geometries in the Node.
        """
        if getattr(self,'img',None) is not None:
            self.img=None

    def get_img(self):
        if getattr(self,'img',None) is not None:
            return self.img 
        else:
            return None  

    def get_virtual_image(self, geometries: o3d.geometry)-> o3d.cpu.pybind.geometry.Image:
        pinholeCamera=self.get_pinhole_camera_parameters()
        if pinholeCamera is not None:
            return gt.generate_virtual_image(geometries,pinholeCamera)
        else:
            return None

    def get_pinhole_camera_parameters(self) -> o3d.camera.PinholeCameraParameters():
        param=o3d.camera.PinholeCameraParameters()
        if getattr(self,'cartesianTransform',None) is not None:
            param.extrinsic=np.linalg.inv(self.cartesianTransform)
            param.intrinsic=self.get_intrinsic_camera_parameters()
            self.pinholeCamera=param
            return self.pinholeCamera
        else:
            return None

    def get_intrinsic_camera_parameters(self) -> o3d.camera.PinholeCameraIntrinsic():

        if (getattr(self,'imageWidth',None) is not None and
            getattr(self,'imageHeight',None) is not None and
            getattr(self,'focalLength35mm',None) is not None and
            getattr(self,'resolutionUnit',None) is not None and
            getattr(self,'xResolution',None) is not None and 
            getattr(self,'yResolution',None) is not None):
                width=math.floor(self.imageWidth/(2*self.resolutionUnit))
                height=math.floor(self.imageHeight/(2*self.resolutionUnit)) 
                fx=self.focalLength35mm*self.xResolution/self.resolutionUnit
                fy=self.focalLength35mm*self.yResolution/self.resolutionUnit
        else:
            width=640
            height=480
            fx=400
            fy=400

        if (getattr(self,'principalPointU',None) is not None and
            getattr(self,'principalPointV',None) is not None ):
            cx=width/2-0.5+self.principalPointU
            cy=height/2-0.5+self.principalPointV
        else:
            cx=width/2-0.5
            cy=height/2-0.5
        return o3d.camera.PinholeCameraIntrinsic(width,height,fx,fy,cx,cy)

    def get_geometry(self)->bool: 
        """
        get cv2 image from self.path or self.name
        
        Returns:
            bool: True if exif data is sucesfully parsed
        """
        if getattr(self,'img',None) is None:
            if getattr(self,'path',None) is not None and os.path.exists(self.path) :
                self.img = cv2.imread(self.path)    
                return True

            if getattr(self,'name',None) is not None and getattr(self,'sessionPath',None) is not None:
                allSessionFilePaths=ut.get_list_of_files(self.sessionPath)
                testJPGPath= self.sessionPath +'\\'+ self.name + '.JPG'
                testPNGPath= self.sessionPath + '\\'+ self.name + '.PNG'
                if testJPGPath in allSessionFilePaths:
                    self.path=testJPGPath
                    self.img = cv2.imread(self.path)  
                    return True
                elif testPNGPath in allSessionFilePaths:
                    self.path=testPNGPath
                    self.img = cv2.imread(self.path)  
                    return True
        return False
    
    def get_metadata_from_img(self) -> bool:
        if getattr(self,'img',None) is not None:
           self.imageHeight=self.img.shape[0]
           self.imageWidth=self.img.shape[1]
           return True
        else:
            return False

    def get_metadata_from_exif_data(self) -> bool:
        """Read Metadata from image exif data including GPSInfo if present.

        Returns:
            bool: True if metadata is sucesfully parsed
        """
 
        pix = PIL.Image.open(self.path) 
        # exifData=pix._getexif()
        exifData=ut.get_exif_data(pix)#pix._getexif()

        if exifData is not None:
            self.timestamp=ut.get_if_exist(exifData, "DateTime")
            self.xResolution=ut.get_if_exist(exifData,"XResolution")
            self.yResolution=ut.get_if_exist(exifData,"YResolution")
            self.resolutionUnit=ut.get_if_exist(exifData,"ResolutionUnit")
            self.imageWidth=ut.get_if_exist(exifData,"ExifImageWidth")
            self.imageHeight=ut.get_if_exist(exifData,"ExifImageHeight")
            
            if 'GPSInfo' in exifData:
                gps_info = exifData["GPSInfo"]
                if gps_info is not None:
                    # self.GlobalPose=GlobalPose # (structure) SphericalTranslation(lat,long,alt), Quaternion(qw,qx,qy,qz)
                    self.geospatialTransform=[  ut.get_if_exist(gps_info, "GPSLatitude"), 
                                                ut.get_if_exist(gps_info, "GPSLongitude"),
                                                ut.get_if_exist(gps_info, "GPSAltitude")]
                    self.coordinateSystem='geospatial-wgs84'
            return True
        else:
            return False
    
    def get_metadata_from_xmp(self)->bool:
        """Read Metadata from .xmp file generated by https://www.capturingreality.com/

        Returns:
            bool: True if metadata is sucesfully parsed
        """
        if getattr(self,'xmpPath',None) is not None: 
            try:
                mytree = ET.parse(self.xmpPath)
                root = mytree.getroot()                       

                for img_description in root.iter('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Description'):
                    lat=ut.xcr_to_lat(img_description.attrib['{http://www.capturingreality.com/ns/xcr/1.1#}latitude'])
                    long=ut.xcr_to_long(img_description.attrib['{http://www.capturingreality.com/ns/xcr/1.1#}longitude'])
                    alt=ut.xcr_to_alt(img_description.attrib['{http://www.capturingreality.com/ns/xcr/1.1#}altitude'])
                    if (lat is not None and
                        long is not None and
                        alt is not None):
                        self.geospatialTransform=np.array([lat, long, alt])
                    
                    self.coordinateSystem=img_description.attrib['{http://www.capturingreality.com/ns/xcr/1.1#}Coordinates']

                    self.focalLength35mm=ut.xml_to_float(img_description.attrib['{http://www.capturingreality.com/ns/xcr/1.1#}FocalLength35mm'])
                    self.principalPointU=ut.xml_to_float(img_description.attrib['{http://www.capturingreality.com/ns/xcr/1.1#}PrincipalPointU'])
                    self.principalPointV=ut.xml_to_float(img_description.attrib['{http://www.capturingreality.com/ns/xcr/1.1#}PrincipalPointV'])

                    rotationnode=img_description.find('{http://www.capturingreality.com/ns/xcr/1.1#}Rotation')
                    if rotationnode is not None:
                        rotationMatrix=ut.string_to_rotation_matrix(rotationnode.text)
                        self.cartesianTransform=rotationMatrix

                    positionnode=img_description.find('{http://www.capturingreality.com/ns/xcr/1.1#}Position')
                    if positionnode is not None:
                        self.cartesianTransform[0,3]=ut.xml_to_float(positionnode.text.split(' ')[0])
                        self.cartesianTransform[1,3]=ut.xml_to_float(positionnode.text.split(' ')[1])
                        self.cartesianTransform[2,3]=ut.xml_to_float(positionnode.text.split(' ')[2])

                    coeficientnode=img_description.find('{http://www.capturingreality.com/ns/xcr/1.1#}DistortionCoeficients')
                    if coeficientnode is not None:
                        self.distortionCoeficients=ut.string_to_array(coeficientnode.text)  
                return True   
            except:
                print('XCR parsing error')
                return False

    def get_metadata_from_xml(self) ->bool:
        """NOT IMPLEMENTED

        Returns:
            bool: True if metadata is sucesfully parsed
        """
        if getattr(self,'xmlPath',None) is not None and getattr(self,'xmlIndex',None) is not None: 
            try:

                 return True   
            except:
                print('XML parsing error')
                return False