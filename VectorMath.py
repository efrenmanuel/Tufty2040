import math
class V2:
    x = 0
    y = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    
    def __getitem__(self, index):
        return [self.x, self.y][index]
    
    def __sub__(self, o):
        return V2(self[0] - o[0], self[1] - o[1])
    
    def __add__(self, o):
        return V2(self[0] + o[0], self[1] + o[1])
    
    def __mul__(self, o):
        return self[0] * o[0] + self[1] * o[1]
    
    def __str__(self):
        return 'V2 \n    x:{x}\n    y:{y}'.format(x=self.x,y=self.y)
    
    def __neg__(self):
        return V2(-self[0], -self[1])

    @property
    def magnitude(self):
        return (self[0]**2+self[1]**2)**0.5
    
        
    def rotated(self, angle):
        s = math.sin(angle)
        c = math.cos(angle)

        xnew = self.x * c - self.y * s
        ynew = self.x * s + self.y * c
    
        return V2(xnew, ynew)

    @property
    def angle(self):    
        return math.atan2(self.x, self.y);
    
    def get_angle_2(self, o):
        angle_radians_self = self.angle
        angle_radians_o = o.angle

        return angle_radians_self - angle_radians_o
        
    def normalize(self):
        return self / self.magnitude

class V3:
    x = 0.
    y = 0.
    z = 0.
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __getitem__(self, index):
        return [self.x, self.y, self.z][index]
    
    def __add__(self, o):
        if isinstance(o, V3):
            return V3(self[0] + o[0], self[1] + o[1], self[2] + o[2])
        elif type(o) == float:
            return V3(self[0] + o, self[1] + o, self[2] + o)
    
    def __sub__(self, o):
        if isinstance(o, V3):
            return V3(self[0] - o[0], self[1] - o[1], self[2] - o[2])
        elif type(o) == float:
            return V3(self[0] - o, self[1] - o, self[2] - o)
    
    def __mul__(self, o):
        if isinstance(o, V3):
            return self[0] * o[0] + self[1] * o[1] + self[2] * o[2]
        elif isinstance(o, float):
            return V3(self[0] * o, self[1] * o, self[2] * o)
        
    def __div__(self, o):
        if isinstance(o, V3):
            return self[0] / o[0] + self[1] / o[1] + self[2] / o[2]
        elif isinstance(o, float):
            return V3(self[0] / o, self[1] / o, self[2] / o)
        
    def __truediv__(self, o):
        if isinstance(o, V3):
            return self[0] / o[0] + self[1] / o[1] + self[2] / o[2]
        elif isinstance(o, float):
            return V3(self[0] / o, self[1] / o, self[2] / o)
    
    def __str__(self):
        return 'V3 \n    x:{x}\n    y:{y}\n    z:{z}'.format(x=self.x,y=self.y,z=self.z)
    
    def __eq__(self,o):
        return self.x == o.x and self.y == o.y and self.z == o.z
    
    @property
    def magnitude(self):
        return (self[0]**2+self[1]**2+self[2]**2)**0.5
    
    def get_angle(self, o):
        #print("d")
        dot = self * o
        #print("d"+str(dot))
        magnitude_self = self.magnitude()
        magnitude_o = o.magnitude()
        #print("dm")
        dot_divided_by_mag = dot / (magnitude_self * magnitude_o)
        #print("acos")
        return math.acos(dot_divided_by_mag)
    
    @property
    def x_y(self):
        return V2(self.x, self.y)
    
    @x_y.setter
    def set_x_y(self, o):
        x = o[0]
        y = o[1]
    
    @property
    def y_z(self):
        return V2(self.y, self.z)
    
    @y_z.setter
    def set_y_z(self, o):
        y = o[0]
        z = o[1]

    @property
    def z_y(self):
        return V2(self.z, self.y)
    
    @y_z.setter
    def set_z_y(self, o):
        z = o[0]
        y = o[1]
    
    def get_h_v_angles(self, o):
        angle_x_y = self.get_x_y().get_angle(o.get_x_y())
        angle_y_z = self.get_y_z().get_angle(o.get_y_z())
        return(angle_x_y, angle_y_z)      

    def rotated_z(self, angle):
        s = math.sin(angle)
        c = math.cos(angle)

        xnew = self.x * c - self.y * s
        ynew = self.x * s + self.y * c
    
        return V3(xnew, ynew, self.z)
    
    def rotated_x(self, angle):
        s = math.sin(angle)
        c = math.cos(angle)

        ynew = self.y * c - self.z * s
        znew = self.y * s + self.z * c
    
        return V3(self.x, ynew, znew)
  
        
    def normalize(self):
        return self / self.magnitude
    

if __name__ == "__main__":
    v21 =V2(0,1)
    print(v21.angle)


