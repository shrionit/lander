import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import *
from core import input


class Window:
    WIDTH = 480
    HEIGHT = 270
    TITLE = "OPENGL"

    def __init__(self, W, H, TITLE):
        if not glfw.init():
            return
        self.clearColor = [0.15, 0.15, 0.15, 1.0]
        self.create(W, H, TITLE)
        self._prevTime = 0
        self._deltatime = 0

    def create(self, W, H, TITLE):
        Window.WIDTH = W
        Window.HEIGHT = H
        Window.TITLE = TITLE
        self.window = glfw.create_window(W, H, TITLE, None, None)

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.SAMPLES, 4)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
        glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, glfw.TRUE)

        if not self.window:
            glfw.terminate()
            return
        glfw.make_context_current(self.window)
        glViewport(0, 0, Window.WIDTH, Window.HEIGHT)
        glClearColor(*self.clearColor)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)
        # Callbacks
        self.setup_callbacks()
        return self.window

    def isNotClosed(self):
        return not glfw.window_should_close(self.window)

    def get_window(self):
        return self.window

    def get_deltatime(self):
        return self._deltatime

    def setup_callbacks(self):
        glfw.set_scroll_callback(self.window, input.on_scroll)
        glfw.set_window_size_callback(self.window, self.on_resize)
        glfw.set_key_callback(self.window, input.keyboard_handler)
        glfw.set_cursor_pos_callback(self.window, input.mouse_handler)
        glfw.set_mouse_button_callback(self.window, input.mouse_button_handler)

    def update(self):
        currTime = glfw.get_time()
        self._deltatime = currTime - self._prevTime
        self._prevTime = currTime
        glfw.swap_buffers(self.window)
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)  # type: ignore

    def on_resize(self, _, width, height):
        Window.WIDTH = width
        Window.HEIGHT = height
        glViewport(0, 0, Window.WIDTH, Window.HEIGHT)

    def close(self):
        glfw.terminate()
