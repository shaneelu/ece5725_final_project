from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.core.audio import SoundLoader
from kivy.uix.image import Image
import border
import home
import analysis
import wave
import os


class ProcessWidget(FloatLayout):
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(ProcessWidget, self).__init__(**kwargs)
        with self.canvas:
            # Color(0.882, 0.976, 0.988, 1.0)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect)
        self.bind(size=self.update_rect)
        stud_file = kwargs.get("stud")
        prof_file = kwargs.get("prof")
        stud, prof = analysis.analyze(
            stud_file, prof_file)
        stud_sound = wave.open(stud_file)
        prof_sound = wave.open(prof_file)

        cmap = Image(source='cmap.png', pos_hint={
            'center_x': .5, 'center_y': .3}, size_hint=(0.7, 0.1))

        self.add_widget(cmap)

        self.add_widget(Button(
                        text="Student",
                        size_hint=(0.1, 0.04),
                        pos_hint=('center_x': 0.1, 'center_y': 0.8)))

        self.add_widget(Button(
                        text="Professional",
                        size_hint=(0.1, 0.04),
                        pos_hint=('center_x': 0.1, 'center_y': 0.5)))

        self.add_widget(
            border.BorderWidget(
                id="bottom",
                f=prof,
                audio=prof_sound,
                size_hint=(.9, .4),
                pos_hint={'center_x': .5, 'center_y': .3}))

        self.add_widget(
            border.BorderWidget(
                id="top",
                f=stud,
                audio=stud_sound,
                size_hint=(.9, .4),
                pos_hint={'center_x': .5, 'center_y': .75}))

        home = Button(
            id="home",
            size_hint=(0.1, 0.06),
            pos_hint={'center_x': .1, 'center_y': .05},
            text="Back",
            background_normal='',
            background_color=[0.5, 0.5, 0.6, 0.7]
        )

        self.add_widget(home)

        quit = Button(
            id="quit",
            size_hint=(0.1, 0.06),
            pos_hint={'center_x': .9, 'center_y': .05},
            text="Quit",
            background_normal='',
            background_color=[0.5, 0.5, 0.6, 0.7]
        )

        home.bind(on_release=self.home_page)
        quit.bind(on_release=self.quit_callback)

        self.add_widget(quit)

    def home_page(self, instance):
        self.add_widget(
            home.HomeWidget(
                id="home",
                size_hint=(1, 1),
                pos_hint={'center_x': .5, 'center_y': .5})
        )

    def quit_callback(self, instance):
        for file in os.listdir(os.getcwd()):
            if file.endswith(".pyc"):
                os.remove(file)
        quit()

    def update_rect(self, *kargs):
        self.rect.pos = self.pos
        self.rect.size = self.size
