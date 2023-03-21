import VectorMath
import Display
import time
import math
import json
import _thread
import gc

half_turn = math.radians(180)

full_turn = math.radians(360)
print(full_turn)


class Camera():
    position = VectorMath.V3(0, 1, 1)
    looking_at = VectorMath.V3(0, 0, 1)
    direction = (looking_at - position).normalize()
    plane_distance = 1.0
    WIDTH, HEIGHT = Display.get_bounds()
    HALF_WIDTH = WIDTH/2
    HALF_HEIGHT = WIDTH/2
    h_fov = 90
    h_fov_half_rad = math.radians(h_fov)/2
    v_fov = HEIGHT/WIDTH * h_fov
    v_fov_half_rad = math.radians(v_fov)/2
    #print(h_fov_half_rad)
    var_semaphore = _thread.allocate_lock()
    semaphore = _thread.allocate_lock()
    
    screen_space_points = []
    
    
    def is_point_in_front(self, point):
        fwd = self.position + self.direction * self.plane_distance
        return (point - self.position).magnitude() > (point - fwd).magnitude()
    
    def screen_space_point(self, point: VectorMath.V2):
        
        point_from_camera = point-self.position

        point_rotated = point_from_camera.rotated_z(self.direction.x_y.angle)

        camera_rotated = self.direction.rotated_z(self.direction.x_y.angle)
        point_rotated = point_rotated.rotated_x(-camera_rotated.z_y.angle)

        angle_h = point_rotated.x_y.angle
        angle_v = point_rotated.z_y.angle
        
        h = angle_h / self.h_fov_half_rad * self.HALF_WIDTH + self.HALF_WIDTH
        v = angle_v / self.v_fov_half_rad * self.HALF_HEIGHT + self.HALF_HEIGHT
        
                
        return VectorMath.V2(h, v)
    
    def get_screen_space_points(self, verts):
        points = [self.screen_space_point(vert) for vert in verts]
        self.var_semaphore.acquire()
        self.screen_space_points += points
        self.var_semaphore.release()
        self.semaphore.release()
    
    def draw_shape(self, shape):
        size_vert_array = len(shape.verts)
        self.screen_space_points=[]
        self.var_semaphore.acquire()
        self.semaphore.acquire()
        v=[shape.verts[size_vert_array//2:]]
        _thread.start_new_thread(self.get_screen_space_points,(v))
        for vert in shape.verts[:size_vert_array//2]:
            self.screen_space_points.append(self.screen_space_point(vert))
        self.var_semaphore.release()
        self.semaphore.acquire()
        self.semaphore.release()
        list_of_points=[]
        #self.screen_space_points+=self.screen_space_points_second_thread
        for edge in shape.edges:
            p1 =self.screen_space_points[edge[0]]
            p2 = self.screen_space_points[edge[1]]
            if p1[0] > 0 and p1[1] > 0 and p2[0] > 0 and p2[1] > 0:
                #print('p1: {p1}\np2: {p2}'.format(p1=p1, p2=p2))
                Display.line(int(p1.x), int(p1.y), int(p2.x), int(p2.y))
        gc.collect()
    
    def set_looking_at(self, point):
        self.looking_at = point
        self.direction = (self.looking_at - self.position).normalize()
        
    def set_position(self, point):
        self.position = point
        self.direction = (self.looking_at - self.position).normalize()
        #print(self.direction)

            

class Mesh:
    def __init__(self, name):
        f = open(name, "r")
        mesh = json.loads(f.read())
        self.verts = [VectorMath.V3(x[0]/50, x[2]/50, -x[1]/50) for x in mesh["vertices"]]
        self.edges = mesh["edges"]
        f.close()


'''class Cube:
    verts=[VectorMath.V3(-0.5,-0.5,-0.5),
           VectorMath.V3(-0.5,-0.5,0.5),
           VectorMath.V3(0.5,-0.5,0.5),
           VectorMath.V3(0.5,-0.5,0.-0.5),
           VectorMath.V3(-0.5,0.5,-0.5),
           VectorMath.V3(-0.5,0.5,0.5),
           VectorMath.V3(0.5,0.5,0.5),
           VectorMath.V3(0.5,0.5,0.-0.5)]
    edges=[(0,1),(1,2),(2,3),(3,0),(0,4),(4,5),(5,6),(6,7),(7,4),(1,5),(2,6),(3,7)]
'''
def Draw_cube(cube):
    Display.set_color(Display.WHITE)
    camera.draw_shape(cube)
    #for vert_conn in cube_vert_conn:
    #    Display.line(160+int(cube_verts[vert_conn[0]][0]*100),120+int(cube_verts[vert_conn[0]][1]*100),160+int(cube_verts[vert_conn[1]][0]*100),120+int(cube_verts[vert_conn[1]][1]*100))      
    #pass
    
    

draw_cube_event = (Draw_cube, 10)
camera = Camera()
print(camera.direction)
#cube = Cube()
#line = Line()
mesh = Mesh("wolf.json")
if __name__ == "__main__":
    if True:
        while True:
            Display.clear()
            camera.set_position(VectorMath.V3(math.cos(time.ticks_ms()/1000)*2, 3, -1))
            #print(camera.position)
            Draw_cube(mesh)
            Display.update()
            time.sleep(.0)
    else:
        Display.clear()
        Draw_cube()
        Display.update()
        time.sleep(.01)
