from GamePlusEditor.ursina import *
from panda3d.bullet import BulletWorld, BulletPlaneShape, BulletBoxShape, BulletRigidBodyNode, BulletDebugNode


app = Ursina()

world = BulletWorld()
world.setGravity(Vec3(0, -9.81, 0))


class RB(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = Cone()
        # self.color = color.black33
        self.color = color.red
        shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
        self.rigidbody_node = BulletRigidBodyNode('BulletRigidBodyNode')
        self.rigidbody_node.setMass(1.0)
        self.rigidbody_node.addShape(shape)
        self.parent = self.rigidbody_node
        world.attachRigidBody(self.rigidbody_node)

        self.physics_np = NodePath(self.rigidbody_node)
        self.physics_np.reparentTo(render)
        self.physics_np.setPos(self.getPos())
        self.physics_np.setHpr(self.getHpr())
        self.physics_np.setScale(self.getScale())


    # def update(self):
    #     self.setPos(self.physics_np.getPos())
    #     self.setHpr(self.physics_np.getHpr())


RB(y=20)
EditorCamera()

ground = Entity(model='plane', scale=10, texture='grass')
shape = BulletPlaneShape(Vec3(0, 1, 0), 0)
node = BulletRigidBodyNode('Ground')
node.addShape(shape)
np = render.attachNewNode(node)
ground.parent = np
world.attachRigidBody(node)

cursor_3d = Entity(model='cube', scale=.1, color=color.orange)

def update():
    if held_keys['space']:
        world.doPhysics(time.dt)

    if base.mouseWatcherNode.has_mouse():
        pMouse = base.mouseWatcherNode.getMouse()
        pFrom = Vec3()
        pTo = Vec3()
        base.camLens.extrude(pMouse, pFrom, pTo)

        # Transform to global coordinates
        # pFrom = render.getRelativePoint(base.cam, pFrom)
        # pTo = render.getRelativePoint(base.cam, pTo)
        result = world.rayTestAll(pFrom, pTo)
        # result = world.rayTestClosest(Vec3(0,0,-10), Vec3(0,0,0))

        print(result.hasHits())
        # # print(result.getHitPos())
        # # print(result.getHitNormal())
        # # print(result.getHitFraction())
        # # print(result.getNode())
        # cursor_3d.enabled = result.hasHit()
        # cursor_3d.position = result.getHitPos()
    else:
        print('no mouse')



debugNode = BulletDebugNode('Debug')
debugNode.showWireframe(True)
debugNode.showConstraints(True)
debugNode.showBoundingBoxes(False)
debugNode.showNormals(False)
debugNP = render.attachNewNode(debugNode)
debugNP.show()
world.setDebugNode(debugNP.node())
app.run()
