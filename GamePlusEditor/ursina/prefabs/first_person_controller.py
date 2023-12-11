from GamePlusEditor.ursina import *
from GamePlusEditor.ursina.curve import out_expo
from GamePlusEditor.ursina.prefabs.health_bar import HealthBar

class FirstPersonController(Entity):
    def __init__(self,forward_key = "w",backward_key = "s",left_key = "a",right_key = "d",jump_key = " ",speed = 5,height = 3,sensitivity = 40, **kwargs):
        self.cursor = Entity(parent=camera.ui, model='quad', color=color.rgba(0,0,0,0), scale=.002, rotation_z=45)
        super().__init__()
##        self.rotation_x = direction_x
##        self.rotation_y = direction_y 
##        self.rotation_z = direction_z
        self.speed = speed
        self.height = height
        self.camera_pivot = Entity(parent=self, y=self.height)
        self.sensitivity = sensitivity

        camera.parent = self.camera_pivot                                       
        camera.position = (0,0,0)
        camera.rotation = (0,0,0)
        camera.fov = 100
        mouse.locked = True 
        self.mouse_sensitivity = Vec2(self.sensitivity,self.sensitivity)

        self.gravity = 1
        self.grounded = False
        self.for_key = forward_key
        self.back_key = backward_key
        self.left_key = left_key
        self.right_key = right_key
        self.jump_key = jump_key
        self.jump_height = 2
        self.jump_up_duration = .5
        self.fall_after = .35 # will interrupt jump up
        self.jumping = False
        self.air_time = 0
        self.healthbar = HealthBar(100, bar_color = color.hex("#ff1e1e"), roundness = 0, y = window.bottom_left[-1] + 0.1, scale_y = 0.04, scale_x = 0.3, enabled = False)
        self.healthbar.text = "Health"
        self.StaminaBar = HealthBar(1000, bar_color = color.hex("#50acff"), roundness = 0,position = window.bottom_left + (0.1, 0.06), scale_y = 0.025,dynamic = True, scale_x = 0.28, enabled = False)
        self.StaminaBar.text_entity.enabled = False
        self.total_number_of_coins = 34
        self.gun = None
        self.direction = Vec3(
            self.forward * (held_keys[self.for_key] - held_keys[self.back_key])
            + self.right * (held_keys[self.right_key] - held_keys[self.left_key])   
            ).normalized()

        self.traverse_target = scene     # by default, it will collide with everything. change this to change the raycasts' traverse targets.
        self.ignore_list = [self, ]


        for key, value in kwargs.items():
            setattr(self, key ,value)

        # make sure we don't fall through the ground if we start inside it0
        if self.gravity:
            ray = raycast(self.world_position+(0,self.height,0), self.down, traverse_target=self.traverse_target, ignore=self.ignore_list)
            if ray.hit:
                self.y = ray.world_point.y + 1


    def update(self):
        if mouse.locked:
            self.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[1]

            self.camera_pivot.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity[0]
            self.camera_pivot.rotation_x= clamp(self.camera_pivot.rotation_x, -90, 90)
    
        if self.StaminaBar.value > 0 and mouse.locked:
            self.direction = Vec3(
                self.forward * (held_keys[self.for_key] - held_keys[self.back_key])
                + self.right * (held_keys[self.right_key] - held_keys[self.left_key])   
                ).normalized()



        feet_ray = raycast(self.position+Vec3(0,0.5,0), self.direction, traverse_target=self.traverse_target, ignore=self.ignore_list, distance=.5, debug=False)
        head_ray = raycast(self.position+Vec3(0,self.height-.1,0), self.direction, traverse_target=self.traverse_target, ignore=self.ignore_list, distance=.5, debug=False)
        if not feet_ray.hit and not head_ray.hit and mouse.locked:
            move_amount = self.direction * time.dt * self.speed

            if raycast(self.position+Vec3(-.0,1,0), Vec3(1,0,0), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                 move_amount[0] = min(move_amount[0], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(-1,0,0), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                 move_amount[0] = max(move_amount[0], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(0,0,1), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[2] = min(move_amount[2], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(0,0,-1), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[2] = max(move_amount[2], 0)
            self.position += move_amount

            # self.position += self.direction * self.speed * time.dt


        if self.gravity:
            # gravity
            ray = raycast(self.world_position+(0,self.height,0), self.down, ignore=(self,))
            # ray = boxcast(self.world_position+(0,2,0), self.down, ignore=(self,))

            if ray.distance <= self.height+.1:
                if not self.grounded:
                    self.land()
                self.grounded = True
                # make sure it's not a wall and that the point is not too far up
                if ray.world_normal.y > .7 and ray.world_point.y - self.world_y < .5: # walk up slope
                    self.y = ray.world_point[1]
                return
            else:
                self.grounded = False

            # if not on ground and not on way up in jump, fall
            self.y -= min(self.air_time, ray.distance-.05) * time.dt * 100
            self.air_time += time.dt * .25 * self.gravity
    
    def input(self, key):
        if key == self.jump_key and mouse.locked:
            self.jump()


    def jump(self):
        if not self.grounded:
            return

        self.grounded = False
        self.animate_y(self.y+self.jump_height, self.jump_up_duration, resolution=int(1//time.dt), curve= out_expo)
        invoke(self.start_fall, delay=self.fall_after)


    def start_fall(self):
        self.y_animator.pause()
        self.jumping = False

    def land(self):
        # print('land')
        self.air_time = 0
        self.grounded = True


    def on_enable(self):
        mouse.locked = True
        self.cursor.enabled = True


    def on_disable(self):
        mouse.locked = False
        self.cursor.enabled = False
    def update_key(self,for_key,back_key,left_key,right_key):       
        self.for_key = for_key
        self.back_key = back_key
        self.left_key = left_key
        self.right_key = right_key

    def update_jump_key(self,jump_key):
        self.jump_key = jump_key




if __name__ == '__main__':
    from GamePlusEditor.ursina.prefabs.first_person_controller import FirstPersonController
    window.vsync = False
    app = Ursina()
    # Sky(color=color.gray)
    ground = Entity(model='plane', scale=(100,1,100), color=color.yellow.tint(-.2), texture='white_cube', texture_scale=(100,100), collider='mesh')
    e = Entity(model='cube', scale=(1,5,10), x=2, y=.01, rotation_y=45, collider='box', texture='white_cube')
    e.texture_scale = (e.scale_z, e.scale_y)
    e = Entity(model='cube', scale=(1,5,10), x=-2, y=.01, collider='box', texture='white_cube')
    e.texture_scale = (e.scale_z, e.scale_y)

    player = FirstPersonController(y=20, origin_y=-.5)
    player.ggun = None


    ggun = Button(parent=scene, model='cube', color=color.blue, origin_y=-.5, position=(3,0,3), collider='box')
    ggun.on_click = Sequence(Func(setattr, ggun, 'parent', camera), Func(setattr, player, 'gun', ggun))

    gun_2 = duplicate(ggun, z=7, x=8)
    slope = Entity(model='cube', collider='box', position=(0,0,8), scale=6, rotation=(45,0,0), texture='brick', texture_scale=(8,8))
    slope = Entity(model='cube', collider='box', position=(5,0,10), scale=6, rotation=(80,0,0), texture='brick', texture_scale=(8,8))
    # hill = Entity(model='sphere', position=(20,-10,10), scale=(25,25,25), collider='sphere', color=color.green)
    # hill = Entity(model='sphere', position=(20,-0,10), scale=(25,25,25), collider='mesh', color=color.green)
    # from ursina.shaders import basic_lighting_shader
    # for e in scene.entities:
    #     e.shader = basic_lighting_shader

    hookshot_target = Button(parent=scene, model='cube', color=color.brown, position=(4,5,5))
    hookshot_target.on_click = Func(player.animate_position, hookshot_target.position, duration=.5, curve=curve.linear)

    def input(key):
        if key == 'left mouse down' and player.gun:
            ggun.blink(color.orange)
            bullet = Entity(parent=gun, model='cube', scale=.1, color=color.black)
            bullet.world_parent = scene
            bullet.animate_position(bullet.position+(bullet.forward*50), curve=curve.linear, duration=1)
            destroy(bullet, delay=1)

    # player.add_script(NoclipMode())
    app.run()
