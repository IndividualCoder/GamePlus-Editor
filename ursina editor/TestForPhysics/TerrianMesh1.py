from panda3d.bullet import BulletCharacterControllerNode
from panda3d.bullet import BulletCapsuleShape
from panda3d.bullet import ZUp


height = 1.75
radius = 0.4
shape = BulletCapsuleShape(radius, height - 2*radius, ZUp)

playerNode = BulletCharacterControllerNode(shape, 0.4, 'Player')
playerNP = self.worldNP.attachNewNode(playerNode)
playerNP.setPos(-2, 0, 14)
playerNP.setH(45)
playerNP.setCollideMask(BitMask32.allOn())

world.attachCharacter(playerNP.node())

def processInput(self):
    speed = Vec3(0, 0, 0)
    omega = 0.0

    if inputState.isSet('forward'): speed.setY( 3.0)
    if inputState.isSet('reverse'): speed.setY(-3.0)
    if inputState.isSet('left'):    speed.setX(-3.0)
    if inputState.isSet('right'):   speed.setX( 3.0)
    if inputState.isSet('turnLeft'):  omega =  120.0
    if inputState.isSet('turnRight'): omega = -120.0

    self.player.setAngularMovement(omega)
    self.player.setLinearMovement(speed, True)

def doJump(self):
    self.player.setMaxJumpHeight(5.0)
    self.player.setJumpSpeed(8.0)
    self.player.doJump()

self.crouching = False

def doCrouch(self):
    self.crouching = not self.crouching
    sz = self.crouching and 0.6 or 1.0

    self.player.getShape().setLocalScale(Vec3(1, 1, sz))

    self.playerNP.setScale(Vec3(1, 1, sz) * 0.3048)
    self.playerNP.setPos(0, 0, -1 * sz)