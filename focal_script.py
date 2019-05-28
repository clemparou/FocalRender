import maya.cmds as cmds
import random
import math

# Load our plug-in.
cmds.loadPlugin( 'depthShader2.py' )

# Gathering datas from selected camera
cam = cmds.ls( selection = True )
camname = cmds.camera( cam, query = True, name = True )
camFD = cmds.getAttr( camname + '.ai_focus_distance' )
camAS = cmds.getAttr( camname + '.ai_aperture_size' )

# Test if a depth shader already exists
test = cmds.ls( 'depth*', type = 'surfaceShader' )
if len(test) == 0 :
    cmds.select( clear = True )
    cmds.select( test , add = True )

# Calculating distances
if camAS < 0.05:
	camF1 = camFD - camFD * ( 1 - 10 *camAS )
	camF2 = camFD + camFD * ( 1 - 10 *camAS )
else:
	if camAS > 0.7:
		camF1 = camFD - camFD * ( 0.1 - 0.1 *camAS )
		camF2 = camFD + camFD * ( 0.1 - 0.1 *camAS )
	else:
		camF1 = camFD - camFD * ( -0.1648051638 * math.log( camAS ) - 0.0264795515 )
		camF2 = camFD + camFD * ( -0.1648051638 * math.log( camAS ) - 0.0264795515 )

# Create or modifiy an instance of our depth shader.
if len(test) == 0 :
	depthShaderName = cmds.shadingNode( 'myDepthShader2', n = 'depthShader', asUtility = True )

cmds.setAttr( depthShaderName + '.gamma', 1.0 )
cmds.setAttr( depthShaderName + '.nearColor', 0, 1, 0 )
cmds.setAttr( depthShaderName + '.focalColor', 0, 0, 1 )
cmds.setAttr( depthShaderName + '.farColor', 1, 0, 0, type = 'double3' )
cmds.setAttr( depthShaderName + '.nearDistance', 5 )
cmds.setAttr( depthShaderName + '.focalDistance1', camF1 )
cmds.setAttr( depthShaderName + '.focalDistance2', camF2 )


if len(test) == 0 :
    # Create a surface shader to which we will attach our depth shader.
    surfaceShaderName = cmds.shadingNode( 'surfaceShader', n = 'depthShader' , asShader = True )
    cmds.connectAttr( depthShaderName + '.outColor', surfaceShaderName + '.outColor', force = True )
    
    # Create a shading group to tie everything together.
    shadingGroupName = cmds.sets( name = 'depthShader1SG', empty = True, noSurfaceShader = True, renderable = True )
    cmds.connectAttr( surfaceShaderName + '.outColor', shadingGroupName + '.surfaceShader', force = True )

# Scaning the scene and selecting the geometry
selec = cmds.ls( geometry = True)


# Assign to the scanned objects we had find, our surface (depth) shader.
cmds.sets( selec, e = True, forceElement = shadingGroupName )

# Selection of the camera for changes
cmds.select( clear = True )
cmds.select( cam , add = True )
