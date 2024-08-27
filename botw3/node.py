import wx
import math

class Node:
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.radius = 20
        self.connections = []  # Lista para almacenar conexiones a otros nodos

    def draw(self, dc):
        # Dibujar el nodo
        dc.SetBrush(wx.Brush(wx.Colour(100, 150, 255)))
        dc.DrawCircle(self.position[0], self.position[1], self.radius)

        # Configurar la fuente y el antialiasing
        font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        dc.SetFont(font)
        dc.SetTextForeground(wx.Colour(255, 255, 255))

        # Obtener el tamaño del texto
        text_size = dc.GetTextExtent(self.name)

        # Calcular la posición para centrar el texto
        text_x = self.position[0] - text_size[0] // 2
        text_y = self.position[1] - text_size[1] // 2

        # Dibujar el texto centrado
        dc.DrawText(self.name, text_x, text_y)

class AutomatonPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.nodes = []
        self.popup_info = None
        self.selected_node = None # Para almacenar el pop-up de información
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_click)
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_right_click)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_MOTION, self.on_mouse_motion)

        self.SetBackgroundColour(wx.Colour(240, 240, 240))
        self.add_node("Node 1", (100, 100))
        self.add_node("Node 2", (300, 100))

    def on_paint(self, event):
        dc = wx.PaintDC(self)
        self.draw_nodes(dc)

    def draw_nodes(self, dc):
        # Dibujar líneas entre nodos
        dc.SetPen(wx.Pen(wx.BLACK, 2))
        for node in self.nodes:
            for connected_node in node.connections:
                self.draw_connection(dc, node, connected_node)

        # Dibujar cada nodo
        for node in self.nodes:
            node.draw(dc)

        # Dibujar el pop-up de información si existe
        if self.popup_info:
            self.draw_popup(dc)

    def draw_connection(self, dc, node1, node2):
        # Dibujar línea entre dos nodos
        dc.DrawLine(node1.position[0], node1.position[1], node2.position[0], node2.position[1])

    def on_left_click(self, event):
        x, y = event.GetPosition()
        for node in self.nodes:
            if self.is_point_in_node(node, (x, y)):
                self.show_node_info(node)
                return

    def on_right_click(self, event):
        x, y = event.GetPosition()
        for node in self.nodes:
            if self.is_point_in_node(node, (x, y)):
                self.show_context_menu(node, event.GetPosition())
                return

    def add_node(self, name, position):
        # Agregar un nuevo nodo
        new_node = Node(name, position)
        self.nodes.append(new_node)

        # Conectar el nuevo nodo al nodo original
        if self.selected_node:
            self.selected_node.connections.append(new_node)

        self.Refresh()  # Redibujar el panel

    def show_node_info(self, node):
        # Mostrar información del nodo en un pop-up
        self.popup_info = (node.name, node.position)
        self.Refresh()  # Redibujar para mostrar el pop-up

    def draw_popup(self, dc):
        if self.popup_info:
            label, position = self.popup_info
            text_size = dc.GetTextExtent(label)
            popup_x = position[0] - text_size[0] // 2
            popup_y = position[1] - text_size[1] - 10  # Mostrar encima del nodo
            dc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))
            dc.SetPen(wx.Pen(wx.BLACK))
            dc.DrawRectangle(popup_x - 5, popup_y - 5, text_size[0] + 10, text_size[1] + 10)
            dc.SetTextForeground(wx.Colour(0, 0, 0))
            dc.DrawText(label, popup_x, popup_y)

    def on_mouse_motion(self, event):
        # Si el mouse se mueve fuera del pop-up, ocultarlo
        if self.popup_info:
            mouse_pos = event.GetPosition()
            if not self.is_point_in_popup(mouse_pos):
                self.popup_info = None
                self.Refresh()

    def is_point_in_node(self, node, point):
        # Verificar si un punto está dentro del nodo
        distance = math.sqrt((point[0] - node.position[0]) ** 2 + (point[1] - node.position[1]) ** 2)
        return distance <= node.radius

    def is_point_in_popup(self, point):
        # Verificar si el punto está dentro del pop-up
        if self.popup_info:
            label, position = self.popup_info
            text_size = self.GetTextExtent(label)
            popup_x = position[0] - text_size[0] // 2
            popup_y = position[1] - text_size[1] - 10
            return (popup_x <= point[0] <= popup_x + text_size[0] + 10) and (popup_y <= point[1] <= popup_y + text_size[1] + 10)
        return False

    def show_context_menu(self, node, position):
        self.selected_node = node  # Asignar el nodo seleccionado
        menu = wx.Menu()
        add_item = menu.Append(wx.ID_ANY, "Add Node")
        self.Bind(wx.EVT_MENU, lambda e: self.add_node("Node", (position[0] + 50, position[1])), add_item)
        self.PopupMenu(menu)
        menu.Destroy()

    def on_size(self, event):
        self.Refresh()  # Redibujar al cambiar el tamaño

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Editable Automaton')
        self.panel = AutomatonPanel(self)
        self.SetSize((600, 400))
        self.Centre()

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()