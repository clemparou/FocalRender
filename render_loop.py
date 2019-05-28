import maya.mel as mel
import maya.cmds as mc
import os.path as path

objectDistance = 0
camAS = 0.55
camFD = 25
while camAS == 0.55:
    while camFD <= 35:
        objectDistance = camFD - 2
        while objectDistance <= camFD - 1:
            print 'D:/scene/pics/AS%s/FD%s/shot_%s_%s_%s.iff' %(camAS,camFD,camAS,camFD,objectDistance)
            print path.isfile( 'D:/scene/pics/AS%s/FD%s/shot_%s_%s_%s.iff' %(camAS,camFD,camAS,camFD,objectDistance) )
            
            if path.isfile( 'D:/scene/pics/AS%s/FD%s/shot_%s_%s_%s.iff' %(camAS,camFD,camAS,camFD,objectDistance) ) == 0 :
                                
	            print 'Processing : CamAS : %s , CamsFD : %s , objectDistance : %s' %(camAS,camFD,objectDistance)
	            cmds.move( 0, -25 , objectDistance, ['pPlane1'] ) 
	            cmds.setAttr( 'cameraShape1.ai_aperture_size', camAS)
	            cmds.setAttr( 'cameraShape1.ai_focus_distance', camFD) 
	            mel.eval('RenderIntoNewWindow;')
	            mc.renderWindowEditor( 'renderView' , e=True , crc='camera1')
	            mc.renderWindowEditor( 'renderView' , e=True , wi='D:/scene/pics/AS%s/FD%s/shot_%s_%s_%s' %(camAS,camFD,camAS,camFD,objectDistance) )
	            objectDistance = objectDistance + 0.1
        
        camFD = camFD + 5
    camAS = camAS - 0.05
    camFD = 5