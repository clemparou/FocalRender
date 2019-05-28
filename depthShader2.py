# depthShader2.py

import sys
import math
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

# Plug-in information:
kPluginNodeName = 'myDepthShader2'
kPluginNodeClassify = 'utility/general'
kPluginNodeId = OpenMaya.MTypeId( 0x870FF )

# Default attribute values
defaultNearDistance = 20.0
defaultFocalDistance1 = 40.0
defaultFocalDistance2 = 50.0
defaultFarDistance  = 100
defaultNearColor    = ( 0.0, 1.0, 0.0 ) # (r,g,b) green
defaultFocalColor   = ( 0.0, 0.0, 1.0 ) # (r,g,b) blue
defaultFarColor     = ( 1.0, 0.0, 0.0 ) # (r,g,b) red
defaultGamma        = 1.0
minGamma            = 0.1
maxGamma            = 5.0

##########################################################
# Plug-in 
##########################################################
class depthShader(OpenMayaMPx.MPxNode):
	''' Creates a depth shader which renders in Maya's software renderer. '''
	# Define the static variables to which we will assign the node's attributes
	# in nodeInitializer() defined below.
	surfacePointAttribute = OpenMaya.MObject()
	nearDistanceAttribute = OpenMaya.MObject()
	focalDistance1Attribute = OpenMaya.MObject()
	focalDistance2Attribute = OpenMaya.MObject()
	farDistanceAttribute  = OpenMaya.MObject()
	nearColorAttribute    = OpenMaya.MObject()
	focalColorAttribute   = OpenMaya.MObject()
	farColorAttribute     = OpenMaya.MObject()
	gammaAttribute        = OpenMaya.MObject()    
	outColorAttribute     = OpenMaya.MObject()
	
	def __init__( self ) :
		''' Constructor. '''
		OpenMayaMPx.MPxNode.__init__( self )
	
	def compute(self, pPlug, pDataBlock) :
		''' 
		Node computation method. 
		  - pDataBlock contains the data on which we will base our computations. 
		  - pPlug is a connection point related to one of our node attributes (either an input or an output). 
		'''
		if ( pPlug == depthShader.outColorAttribute ) :
			
			# Get the data handles corresponding to your attributes among the values in the data block.
			surfacePointDataHandle = pDataBlock.inputValue( depthShader.surfacePointAttribute )
			nearDistanceDataHandle = pDataBlock.inputValue( depthShader.nearDistanceAttribute )
			focalDistance1DataHandle = pDataBlock.inputValue( depthShader.focalDistance1Attribute )
			focalDistance2DataHandle = pDataBlock.inputValue( depthShader.focalDistance2Attribute )
			farDistanceDataHandle  = pDataBlock.inputValue( depthShader.farDistanceAttribute )
			nearColorDataHandle    = pDataBlock.inputValue( depthShader.nearColorAttribute )
			focalColorDataHandle    = pDataBlock.inputValue( depthShader.focalColorAttribute )
			farColorDataHandle     = pDataBlock.inputValue( depthShader.farColorAttribute )
			gammaDataHandle        = pDataBlock.inputValue( depthShader.gammaAttribute )
			
			# Obtain the (x,y,z) location of the currently rendered point in camera coordinates.
			surfacePoint = surfacePointDataHandle.asFloatVector()
			
			# Since the camera is looking along its negative Z axis (the Y axis is 
			# the up vector), we must take the absolute value of the Z coordinate
			# to obtain the point's depth.
			depth = abs( surfacePoint.z ) 
			
			# Get the actual near and far threshold values.
			nearValue = nearDistanceDataHandle.asFloat()
			focalValue1 = focalDistance1DataHandle.asFloat()
			focalValue2 = focalDistance2DataHandle.asFloat()
			farValue = farDistanceDataHandle.asFloat()
			
			# Find the proportion of depth between the near and far values.
			
			focalField = focalValue2 - focalValue1

			if focalField != 0 :

				gradient1Begin = focalValue1 - 0.5 * focalField
				gradient2End = focalValue2 + 0.5 * focalField
				depthProportion = 0

				if depth >= gradient1Begin and depth <= focalValue1 :
					depthProportion = ( depth - gradient1Begin ) / ( focalValue1 - gradient1Begin )

				if depth >= focalValue2 and depth <= gradient2End :
					depthProportion = ( depth - focalValue2 ) / ( gradient2End - focalValue2 )

			if focalField == 0 :

				gradient1Begin = focalValue1 - 2
				gradient2End = focalValue2 + 2
				depthProportion = 0

				if depth >= gradient1Begin and depth <= focalValue1 :
					depthProportion = ( depth - gradient1Begin ) / ( 2 )

				if depth >= focalValue2 and depth <= gradient2End :
					depthProportion = ( depth - focalValue2 ) / ( 2 )
								
			# Clamp the depthProportion value in the interval [0.0, 1.0]
			depthProportion = max( 0, min( depthProportion, 1.0 ) )
			
			# Modify the depth proportion using the gamma roll-off bias.
			gammaValue = gammaDataHandle.asFloat()
			depthProportion = math.pow( depthProportion, gammaValue )
			
			# Linearly interpolate the output color based on the depth proportion.
			outColor = OpenMaya.MFloatVector( 0, 0, 0 )
			nearColor = nearColorDataHandle.asFloatVector()
			focalColor = focalColorDataHandle.asFloatVector()
			farColor = farColorDataHandle.asFloatVector()
			
			if depth < gradient1Begin :
				outColor.x = nearColor.x 
				outColor.y = nearColor.y 
				outColor.z = nearColor.z 

			if  depth >= gradient1Begin and depth <= focalValue1 :
				outColor.x = nearColor.x + ( ( focalColor.x - nearColor.x ) * depthProportion )
				outColor.y = nearColor.y + ( ( focalColor.y - nearColor.y ) * depthProportion )
				outColor.z = nearColor.z + ( ( focalColor.z - nearColor.z ) * depthProportion )

			if depth > focalValue1 and depth < focalValue2 :
				outColor.x = focalColor.x 
				outColor.y = focalColor.y 
				outColor.z = focalColor.z 
			
			if  depth >= focalValue2  and  depth <= gradient2End :	
				outColor.x = focalColor.x + ( ( farColor.x - focalColor.x ) * depthProportion )
				outColor.y = focalColor.y + ( ( farColor.y - focalColor.y ) * depthProportion )
				outColor.z = focalColor.z + ( ( farColor.z - focalColor.z ) * depthProportion )

			if depth > gradient2End :
				outColor.x = farColor.x 
				outColor.y = farColor.y 
				outColor.z = farColor.z 

			# Write to the output data.
			outColorDataHandle = pDataBlock.outputValue( depthShader.outColorAttribute )
			outColorDataHandle.setMFloatVector( outColor )
			outColorDataHandle.setClean()
		else:
			return OpenMaya.kUnknownParameter

##########################################################
# Plug-in initialization.
##########################################################
def nodeCreator():
	''' 
	Creates an instance of our node plug-in and delivers it to Maya as a pointer. 
	'''
	return OpenMayaMPx.asMPxPtr( depthShader() )

def nodeInitializer():
	''' 
	Defines the set of attributes for our node. The attributes
	declared in this function are assigned as static members to our
	depthShader class. Instances of depthShader will use these attributes
	to create plugs for use in the compute() method.
	'''
	# Create a numeric attribute function set, since our attributes will all be defined by numeric types.
	numericAttributeFn = OpenMaya.MFnNumericAttribute()
	
	#==================================
	# INPUT NODE ATTRIBUTE(S)
	#==================================
	# - The (x,y,z) point on the surface defined according to the camera's frame of reference.
	#   > (!) Important: the 'pointCamera' string relates to the samplerInfo maya node.
	#   > This value is supplied by the render sampler at computation time.
	depthShader.surfacePointAttribute = numericAttributeFn.createPoint( 'pointCamera', 'p')
	numericAttributeFn.setStorable( False )
	numericAttributeFn.setHidden( True )
	depthShader.addAttribute( depthShader.surfacePointAttribute )
	
	# - The 'near' distance, i.e. the minimum distance threshold from the camera after which the 
	#   pixel's color is modified by the depth of the point.
	#   > This value can be defined by the user, and is storable.
	global defaultNearDistance
	global defaultFarDistance
	global defaultFocalDistance1
	global defaultFocalDistance2

	depthShader.nearDistanceAttribute = numericAttributeFn.create( 'nearDistance', 'nd', 
																	OpenMaya.MFnNumericData.kFloat, defaultNearDistance )
	numericAttributeFn.setStorable( True )
	numericAttributeFn.setMin( 0.0 )
	numericAttributeFn.setMax( 1000 )
	depthShader.addAttribute( depthShader.nearDistanceAttribute )
	
	# - The 'focal' distance, i.e. the distance of the focal point
	#   pixel's color is modified by the depth of the point.
	#   > This value can be defined by the user, and is storable.
	depthShader.focalDistance1Attribute = numericAttributeFn.create( 'focalDistance1', 'fod1', 
																	 OpenMaya.MFnNumericData.kFloat, defaultFocalDistance1 )
	numericAttributeFn.setStorable( True )
	numericAttributeFn.setMin( 1.0 ) # Add an epsilon value of 0.1 to avoid near distance overlap.
	numericAttributeFn.setMax( 1001 )
	depthShader.addAttribute( depthShader.focalDistance1Attribute )

	# - The 'focal' distance, i.e. the distance of the focal point
	#   pixel's color is modified by the depth of the point.
	#   > This value can be defined by the user, and is storable.
	depthShader.focalDistance2Attribute = numericAttributeFn.create( 'focalDistance2', 'fod2', 
																	 OpenMaya.MFnNumericData.kFloat, defaultFocalDistance2 )
	numericAttributeFn.setStorable( True )
	numericAttributeFn.setMin( 1.0 ) # Add an epsilon value of 0.1 to avoid near distance overlap.
	numericAttributeFn.setMax( 1001 )
	depthShader.addAttribute( depthShader.focalDistance2Attribute )

	# - The 'far' distance, i.e. the minimum distance threshold from the camera before which the
	#   pixel's color is modified by the depth of the point.
	#   > This value can be defined by the user, and is storable.
	depthShader.farDistanceAttribute = numericAttributeFn.create( 'farDistance', 'fd', 
																   OpenMaya.MFnNumericData.kFloat, defaultFarDistance )
	numericAttributeFn.setStorable( True )
	numericAttributeFn.setMin( 2 ) # Add an epsilon value of 0.1 to avoid near distance overlap.
	numericAttributeFn.setMax( 1002 )
	depthShader.addAttribute( depthShader.farDistanceAttribute )
	
	# - The 'near' color.
	#   > This value can be defined by the user using a color picker, and is storable.
	global defaultNearColor
	depthShader.nearColorAttribute = numericAttributeFn.createColor( 'nearColor', 'nc' )
	numericAttributeFn.setStorable( True )
	numericAttributeFn.setDefault( defaultNearColor[0], defaultNearColor[1], defaultNearColor[2] )
	depthShader.addAttribute( depthShader.nearColorAttribute )

	# - The 'focal' color.
	#   > This value can be defined by the user using a color picker, and is storable
	global defaultFocalColor
	depthShader.focalColorAttribute = numericAttributeFn.createColor( 'focalColor', 'foc' )
	numericAttributeFn.setStorable( True )
	numericAttributeFn.setDefault( defaultFocalColor[0], defaultFocalColor[1], defaultFocalColor[2] )
	depthShader.addAttribute( depthShader.focalColorAttribute )	

	# - The 'far' color.
	#   > This value can be defined by the user using a color picker, and is storable.
	global defaultFarColor
	depthShader.farColorAttribute = numericAttributeFn.createColor( 'farColor', 'fc' )
	numericAttributeFn.setStorable( True )
	numericAttributeFn.setDefault( defaultFarColor[0], defaultFarColor[1], defaultFarColor[2] )
	depthShader.addAttribute( depthShader.farColorAttribute )
	
	# - The gamma value, or roll-off bias, which will affect how the color is interpolated between
	#   the near and far colors.
	#   > This value can be defined by the user using a slider, and is storable.
	global defaultGamma, minGamma, maxGamma
	depthShader.gammaAttribute = numericAttributeFn.create( 'gamma', 'g', 
															OpenMaya.MFnNumericData.kFloat, defaultGamma )
	numericAttributeFn.setStorable( True )
	numericAttributeFn.setMin( minGamma )
	numericAttributeFn.setMax( maxGamma )
	depthShader.addAttribute( depthShader.gammaAttribute )
	
	#==================================
	# OUTPUT NODE ATTRIBUTE(S)
	#==================================    
	# - The pixel color output.
	#   > This value is computed in our depthShader.compute() method, and should not be stored.
	depthShader.outColorAttribute = numericAttributeFn.createColor( 'outColor', 'oc')
	numericAttributeFn.setStorable( False )
	numericAttributeFn.setWritable( False )
	numericAttributeFn.setReadable( True )
	numericAttributeFn.setHidden( False )
	depthShader.addAttribute( depthShader.outColorAttribute )
	
	#==================================
	# NODE ATTRIBUTE DEPENDENCIES
	#==================================
	#  - All the input attributes affect the computation of the pixel color output (outColor).
	depthShader.attributeAffects( depthShader.surfacePointAttribute, depthShader.outColorAttribute )
	depthShader.attributeAffects( depthShader.nearDistanceAttribute, depthShader.outColorAttribute )
	depthShader.attributeAffects( depthShader.focalDistance1Attribute,  depthShader.outColorAttribute )
	depthShader.attributeAffects( depthShader.focalDistance2Attribute,  depthShader.outColorAttribute )
	depthShader.attributeAffects( depthShader.farDistanceAttribute,  depthShader.outColorAttribute )
	depthShader.attributeAffects( depthShader.nearColorAttribute,    depthShader.outColorAttribute )
	depthShader.attributeAffects( depthShader.focalColorAttribute,     depthShader.outColorAttribute )
	depthShader.attributeAffects( depthShader.farColorAttribute,     depthShader.outColorAttribute )
	depthShader.attributeAffects( depthShader.gammaAttribute,        depthShader.outColorAttribute )


def initializePlugin( mobject ):
	''' Initializes the plug-in. '''
	mplugin = OpenMayaMPx.MFnPlugin( mobject )
	try:
		mplugin.registerNode( kPluginNodeName, kPluginNodeId, nodeCreator, 
					nodeInitializer, OpenMayaMPx.MPxNode.kDependNode, kPluginNodeClassify )
	except:
		sys.stderr.write( "Failed to register node: " + kPluginNodeName )
		raise

def uninitializePlugin( mobject ):
	''' Unitializes the plug-in. '''
	mplugin = OpenMayaMPx.MFnPlugin( mobject )
	try:
		mplugin.deregisterNode( kPluginNodeId )
	except:
		sys.stderr.write( "Failed to deregister node: " + kPluginNodeName )
		raise
