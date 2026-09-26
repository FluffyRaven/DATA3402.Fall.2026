import math

class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = [[' '] * width for i in range(height)]

    def set_pixel(self, row, col, char='*'):
        if 0 <= row < self.height and 0 <= col < self.width:
            self.data[row][col] = char

    def get_pixel(self, row, col):
        return self.data[row][col]
    
    def clear_canvas(self):
        self.data = [[' '] * self.width for i in range(self.height)]
    
    def v_line(self, x, y, h, **kargs):
        for i in range(x, x + h):
            self.set_pixel(i, y, **kargs)

    def h_line(self, x, y, w, **kargs):
        for i in range(y, y + w):
            self.set_pixel(x, i, **kargs)
            
    def line(self, x1, y1, x2, y2, **kargs):
        steps = max(abs(x2 - x1), abs(y2 - y1))
        if steps == 0:
            self.set_pixel(x1, y1, **kargs)
            return
        for i in range(steps + 1):
            r = int(round(x1 + (x2 - x1) * i / steps))
            c = int(round(y1 + (y2 - y1) * i / steps))
            self.set_pixel(r, c, **kargs)
            
    def display(self):
        print("\n".join(["".join(row) for row in self.data]))


class Shape:
    def __init__(self, x=0, y=0, name="", **kwargs):
        self.__x = x
        self.__y = y
        self.name = name
        self.kwargs = kwargs
    
    def get_x(self):
        return self.__x
    
    def get_y(self):
        return self.__y

    def set_x(self, x):
        self.__x = x

    def set_y(self, y):
        self.__y = y

    def area(self):
        raise NotImplementedError

    def perimeter(self):
        raise NotImplementedError

    def perimeter_points(self):
        raise NotImplementedError

    def is_inside(self, x, y):
        raise NotImplementedError

    def overlaps(self, other):
        for px, py in self.perimeter_points():
            if other.is_inside(px, py):
                return True
        for px, py in other.perimeter_points():
            if self.is_inside(px, py):
                return True
        return False

    def paint(self, canvas):
        raise NotImplementedError


class Rectangle(Shape):
    def __init__(self, x, y, length, width, name="", **kwargs):
        super().__init__(x, y, name=name, **kwargs)
        self.__length = length
        self.__width = width
    
    def area(self):
        return self.__length * self.__width
    
    def perimeter(self):
        return 2 * (self.__length + self.__width)
    
    def get_length(self):
        return self.__length

    def get_width(self):
        return self.__width

    def set_length(self, length):
        self.__length = length

    def set_width(self, width):
        self.__width = width

    def perimeter_points(self):
        x0, y0 = self.get_x(), self.get_y()
        L, W = self.__length, self.__width
        pts = []
        for i in range(4):
            t = i / 4.0
            pts.append((x0 + t * L, y0))
            pts.append((x0 + L, y0 + t * W))
            pts.append((x0 + (1 - t) * L, y0 + W))
            pts.append((x0, y0 + (1 - t) * W))
        return pts

    def is_inside(self, x, y):
        x0, y0 = self.get_x(), self.get_y()
        return (x0 <= x <= x0 + self.__length) and (y0 <= y <= y0 + self.__width)

    def paint(self, canvas):
        x, y = self.get_x(), self.get_y()
        h, w = self.__length, self.__width
        canvas.h_line(x, y, w + 1, **self.kwargs)
        canvas.h_line(x + h, y, w + 1, **self.kwargs)
        canvas.v_line(x, y, h + 1, **self.kwargs)
        canvas.v_line(x, y + w, h + 1, **self.kwargs)

    def __repr__(self):
        kw_str = "".join(f", {k}={repr(v)}" for k, v in self.kwargs.items())
        return f"Rectangle({repr(self.get_x())}, {repr(self.get_y())}, {repr(self.__length)}, {repr(self.__width)}, name={repr(self.name)}{kw_str})"


class Circle(Shape):
    def __init__(self, x, y, radius, name="", **kwargs):
        super().__init__(x, y, name=name, **kwargs)
        self.__radius = radius
    
    def area(self):
        return math.pi * self.__radius ** 2
    
    def perimeter(self):
        return 2 * math.pi * self.__radius
    
    def get_radius(self):
        return self.__radius

    def set_radius(self, radius):
        self.__radius = radius

    def perimeter_points(self):
        xc, yc = self.get_x(), self.get_y()
        r = self.__radius
        return [
            (xc + r * math.cos(2 * math.pi * i / 16),
             yc + r * math.sin(2 * math.pi * i / 16))
            for i in range(16)
        ]

    def is_inside(self, x, y):
        xc, yc = self.get_x(), self.get_y()
        return (x - xc) ** 2 + (y - yc) ** 2 <= self.__radius ** 2

    def paint(self, canvas):
        xc, yc = self.get_x(), self.get_y()
        r = self.__radius
        steps = max(16, int(2 * math.pi * r * 2))
        for i in range(steps):
            theta = 2 * math.pi * i / steps
            row = int(round(xc + r * math.cos(theta)))
            col = int(round(yc + r * math.sin(theta)))
            canvas.set_pixel(row, col, **self.kwargs)

    def __repr__(self):
        kw_str = "".join(f", {k}={repr(v)}" for k, v in self.kwargs.items())
        return f"Circle({repr(self.get_x())}, {repr(self.get_y())}, {repr(self.__radius)}, name={repr(self.name)}{kw_str})"


class Triangle(Shape):
    def __init__(self, x1, y1, x2, y2, x3, y3, name="", **kwargs):
        super().__init__(x1, y1, name=name, **kwargs)
        self.__x2 = x2
        self.__y2 = y2
        self.__x3 = x3
        self.__y3 = y3

    @staticmethod
    def _tri_area(ax, ay, bx, by, cx, cy):
        return 0.5 * abs(ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    
    def area(self):
        return self._tri_area(
            self.get_x(), self.get_y(),
            self.__x2, self.__y2,
            self.__x3, self.__y3
        )
    
    def perimeter(self):
        x1, y1 = self.get_x(), self.get_y()
        d1 = math.hypot(self.__x2 - x1, self.__y2 - y1)
        d2 = math.hypot(self.__x3 - self.__x2, self.__y3 - self.__y2)
        d3 = math.hypot(x1 - self.__x3, y1 - self.__y3)
        return d1 + d2 + d3
    
    def get_x2(self):
        return self.__x2

    def get_y2(self):
        return self.__y2

    def get_x3(self):
        return self.__x3

    def get_y3(self):
        return self.__y3

    def perimeter_points(self):
        v = [
            (self.get_x(), self.get_y()),
            (self.__x2, self.__y2),
            (self.__x3, self.__y3)
        ]
        pts = []
        for idx in range(3):
            x_start, y_start = v[idx]
            x_end, y_end = v[(idx + 1) % 3]
            for k in range(5):
                t = k / 5.0
                pts.append((x_start + t * (x_end - x_start),
                            y_start + t * (y_end - y_start)))
        return pts

    def is_inside(self, x, y):
        x1, y1 = self.get_x(), self.get_y()
        x2, y2 = self.__x2, self.__y2
        x3, y3 = self.__x3, self.__y3
        total = self.area()
        a1 = self._tri_area(x, y, x2, y2, x3, y3)
        a2 = self._tri_area(x1, y1, x, y, x3, y3)
        a3 = self._tri_area(x1, y1, x2, y2, x, y)
        return abs(total - (a1 + a2 + a3)) < 1e-9

    def paint(self, canvas):
        x1, y1 = self.get_x(), self.get_y()
        canvas.line(x1, y1, self.__x2, self.__y2, **self.kwargs)
        canvas.line(self.__x2, self.__y2, self.__x3, self.__y3, **self.kwargs)
        canvas.line(self.__x3, self.__y3, x1, y1, **self.kwargs)

    def __repr__(self):
        kw_str = "".join(f", {k}={repr(v)}" for k, v in self.kwargs.items())
        return (f"Triangle({repr(self.get_x())}, {repr(self.get_y())}, "
                f"{repr(self.__x2)}, {repr(self.__y2)}, "
                f"{repr(self.__x3)}, {repr(self.__y3)}, name={repr(self.name)}{kw_str})")


class CompoundShape(Shape):
    def __init__(self, shapes, name="", **kwargs):
        super().__init__(0, 0, name=name, **kwargs)
        self.shapes = shapes

    def paint(self, canvas):
        for s in self.shapes:
            s.paint(canvas)

    def __repr__(self):
        kw_str = "".join(f", {k}={repr(v)}" for k, v in self.kwargs.items())
        return f"CompoundShape({repr(self.shapes)}, name={repr(self.name)}{kw_str})"
