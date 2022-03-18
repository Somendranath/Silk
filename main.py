import os
import cv2
from skimage.io import imsave
from skimage.filters import hessian
import numpy as np
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import NumericProperty,ObjectProperty,StringProperty
from kivy.uix.textinput import TextInput
from kivy import platform

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a

#from code import calculate_d
# property manager that gives you the instance of the ScreenManager used.
if platform=="android":
    from android.permissions import Permission,request_permissions
    request_permissions([Permission.CAMERA,Permission.READ_EXTERNAL_STORAGE,Permission.WRITE_EXTERNAL_STORAGE])

Window.maximize()
Builder.load_string("""
<MenuScreen>:
    BoxLayout:
        orientation: 'vertical'
        
        spacing: 20
        padding: 50
        
        Label:
            text: 'APP'
            pos_hint: {'center_x':0.5,'center_y':0.5}
            size_hint: (0.5,0.5)
            
        Button:
            text: 'Camera'
            pos_hint: {'center_x':0.5,'center_y':0.5}
            size_hint: (0.5,0.5)
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.current = 'camera'
        Button:
            text: 'Upload from Gallery'
            pos_hint: {'center_x':0.5,'center_y':0.5}
            size_hint: (0.5,0.5)
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.current = 'files'
                
        Button:
            text: 'Quit'
            pos_hint: {'center_x':0.5,'center_y':0.5}
            size_hint: (0.5,0.5)
            on_press: app.stop()


<CameraScreen>:
    FloatLayout:
        orientation: 'horizontal'
        Camera:
            id: camera
            resolution:(10000,10000)
            allow_stretch: True
            keep_ratio: True
            play: True
            
        Button:
            text: 'Capture'
            background_color: 0,1,0,1
            size_hint: (.075,.075) 
            pos_hint: {'bottom': 1,'center_x':0.5}
                
            on_press: 
                root.capture()
                root.manager.transition.direction = 'left'
                root.manager.current = 'display'
                
        Button:
            text: '< Back'
            background_color: 0,0,1,1
            size_hint: (.075,.075)
            pos_hint: {'bottom':1, 'left': 1}
                
            on_press:
                root.manager.transition.direction = 'right'
                root.manager.current = 'menu'
<MyWidget>:
    BoxLayout:
        id: my_widget
        FileChooserIconView:
            id: filechooser
            on_selection: 
                root.select(*args)
        FloatLayout:
            Button:
                text: 'next >'
                pos_hint: {'bottom': 1,'right':1}
                size_hint: (.3,.1)
                on_press:
                    root.manager.transition.direction = 'left'
                    root.manager.current = 'distanceu'
                    
            Button:
                text: '< back'
                pos_hint: {'bottom': 1,'left':1}
                size_hint: (.3,.1)
                on_press:
                    root.manager.transition.direction = 'right'
                    root.manager.current = 'menu'
        Image:
            id: image
            source: ""
            
<DisplayImageScreen>:
    
    FloatLayout:
        Image:      
            id: image
            source: 'image.png'
            allow_stretch: True  
        Button:
            
            text: 'Re-Capture'
            background_color: 0,1,0,1
            size_hint: (.075,.075)
            pos_hint: {'center_x': 0.4,'bottom':1}
                
            on_press: 
                root.manager.transition.direction = 'right'
                root.manager.current = 'camera'
                
        Button:
            text: 'Next'
            background_color: 0,0,1,1
            size_hint: (.075,.075)
            pos_hint: {'center_x': 0.6,'bottom':1}
                
            on_press:
                
                root.build()
                root.manager.transition.direction = 'left'
                root.manager.current = 'distance'

<DistanceScreen>:
    BoxLayout:
        orientation: 'vertical' 
        spacing: 20
        padding: 50
           
                
        TextInput:
            id: input
            input_filter: 'int'
            hint_text:'Enter Distance'
            multiline:False
            pos_hint: {'center_x':0.5,'center_y':0.5}
            size_hint: (0.9,0.01)

        Button:
            text: 'show result'
            pos_hint: {'center_x':0.5,'center_y':0.5}
            size_hint: (0.3,0.01)
            
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.current = 'result'

<DistanceUScreen>:
    BoxLayout:
        orientation: 'vertical' 
        spacing: 20
        padding: 50
           
                
        TextInput:
            id: input
            input_filter: 'int'
            hint_text:'Enter Distance'
            multiline:False
            pos_hint: {'center_x':0.5,'center_y':0.5}
            size_hint: (0.9,0.01)

        Button:
            text: 'show result'
            pos_hint: {'center_x':0.5,'center_y':0.5}
            size_hint: (0.3,0.01)
            
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.current = 'resultu'
                
<ResultScreen>:
    
    BoxLayout:
        orientation: 'vertical'
        
        spacing: 20
        padding: 50
        
        Label:
            id: lb1
            text: 'Distance: {} cm'.format(root.dist)
            pos_hint: {'center_x':0.5,'center_y':0.5}
            size_hint: (0.5,0.5)
            
        Label:
            id: lb2
            text: 'Result dier: {} D'.format(root.value)
            pos_hint: {'center_x':0.5,'center_y':0.5}
            size_hint: (0.5,0.5)           
            
        Button:
            text: 'Recapture'
            pos_hint: {'center_x':0.5,'center_y':0.5}
            
            size_hint: (0.5,0.5)
            on_press:
                root.cls_screen()
                root.manager.transition.direction = 'right'
                root.manager.current = 'camera'
        Button:
            text: 'Back to menu'
            pos_hint: {'center_x':0.5,'center_y':0.5}
            size_hint: (0.5,0.5)
            on_press:
                root.manager.transition.direction = 'right'
                root.manager.current = 'menu'
        Button:
            text: 'Quit'
            pos_hint: {'center_x':0.5,'center_y':0.5}
            size_hint: (0.5,0.5)
            on_press: 
                app.stop()
                os.remove()
<ResultUScreen>:
    
    BoxLayout:
        orientation: 'vertical'
        
        spacing: 20
        padding: 50
        
        Label:
            id: lb1
            text: 'Distance: {} cm'.format(root.dist)
            pos_hint: {'center_x':0.5,'center_y':0.5}
            size_hint: (0.5,0.5)
            
        Label:
            id: lb2
            text: 'Result dier: {} D'.format(root.value)
            pos_hint: {'center_x':0.5,'center_y':0.5}
            size_hint: (0.5,0.5)           
            
        Button:
            text: 'Back to menu'
            pos_hint: {'center_x':0.5,'center_y':0.5}
            
            size_hint: (0.5,0.5)
            on_press:
                root.cls_screen()
                root.manager.transition.direction = 'right'
                root.manager.current = 'menu'
        Button:
            text: 'Quit'
            pos_hint: {'center_x':0.5,'center_y':0.5}
            size_hint: (0.5,0.5)
            on_press: app.stop()
             
""")

class MenuScreen(Screen):
    pass

      
class CameraScreen(Screen):
    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        camera.export_to_png('image.png')

class MyWidget(Screen):
    path = StringProperty()
    def select(self, *args):
        try: 
            self.ids.image.source = args[1][0]
            self.path = self.ids.image.source
        except: pass
        
class DisplayImageScreen(Screen):
    def __init__(self, **kwargs):
       super(DisplayImageScreen,self).__init__(**kwargs)
       # Photo can be reference by running the photo function once:
       Clock.schedule_interval(self.photo,1.0/5)
    
    def photo(self,dt):
        image = self.ids['image']
        image.reload()
        
    def build(self):
        image = self.ids['image']
        image.reload()

class DistanceScreen(Screen):
    #code for measuring the diameter and return the output
    pass

class DistanceUScreen(Screen):
    #code for measuring the diameter and return the output
    pass   

class ResultScreen(Screen):
    
    value = ObjectProperty()
    dist = NumericProperty()
    
    def on_enter(self, *largs):
        try:
            result_screen = self.manager.get_screen('distance')
            self.dist = result_screen.ids.input.text
####################################################################################
#############################   Segmentation   #####################################

            img = cv2.imread("image.png")
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

            #generate hessian image
            hessian_img = hessian(gray)
            imsave("hessian_img.png",hessian_img)
        
            image = cv2.imread('hessian_img.png')

            image = cv2.resize(image,(img.shape[1],img.shape[0]),interpolation = cv2.INTER_AREA)
            gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

            edged = cv2.Canny(gray,30,200)
            ##
            retr,thresh = cv2.threshold(gray,100,255,cv2.THRESH_BINARY_INV)
            contours,hierarchy = cv2.findContours(thresh, 
                                              cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            mask = np.zeros(image.shape[:2],dtype = image.dtype)
            for contour in contours:
                if cv2.contourArea(contour) > 10:
                    x,y,w,h = cv2.boundingRect(contour)
                    cv2.drawContours(mask,[contour],0,(255),-1)

            result = cv2.bitwise_and(image,image,mask=mask)        
            result = cv2.bitwise_not(result)

            xxx = np.bitwise_and(image,result)

            cv2.imwrite('image_1.png',xxx)
            #Draw contours

            Test = cv2.imread('image_1.png')
            gray = cv2.cvtColor(Test,cv2.COLOR_BGR2GRAY)

            contours ,hier = cv2.findContours(gray,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
            cv2.drawContours(Test,contours,-1,(0,255,0),3)
            #keep the largest contour

            largest = sorted(contours,key = cv2.contourArea)
            mask = np.zeros(Test.shape,np.uint8)
            cv2.drawContours(mask,[largest[-1]],0,(255,255,255),-1)
            removed = cv2.bitwise_and(Test,mask)

            cv2.imwrite('removed.png',removed)
        
            gray_image = cv2.cvtColor(removed,cv2.COLOR_BGR2GRAY)

            (thresh, bin_img) = cv2.threshold(gray_image,50,255,cv2.THRESH_BINARY)

            cv2.imwrite('Finalimage.png',bin_img)
            pl = cv2.imread('Finalimage.png',0)
            pp = np.reshape(pl,img.shape[0]*img.shape[1])
            self.value = np.sum([pp>107])
        except Exception:
            a=0
    def cls_screen(self, *largs):
        self.dist = 0
        self.value = 0
        self.ids.lb1.text = 'Distance: {} cm'.format(self.dist)
        self.ids.lb2.text = 'Result dier: {} D'.format(self.value)
        result_screen = self.manager.get_screen('distance')
        result_screen.ids.input.text = ''
        
class ResultUScreen(Screen):
    
    value = ObjectProperty()
    dist = NumericProperty()
    path = StringProperty()
    
    def on_enter(self, *largs):
        try:
            result_screen = self.manager.get_screen('distanceu')
            self.dist = result_screen.ids.input.text
            result = self.manager.get_screen('files')
            self.path = result.ids.image.source
####################################################################################
#############################   Segmentation   #####################################

            img = cv2.imread(self.path)
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

            #generate hessian image
            hessian_img = hessian(gray,mode='constant')
            imsave("hessian_img.png",hessian_img)
        
            image = cv2.imread('hessian_img.png')
            image = cv2.resize(image,(img.shape[1],img.shape[0]),interpolation = cv2.INTER_AREA)
            gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

            edged = cv2.Canny(gray,30,200)
        ##
            retr,thresh = cv2.threshold(gray,100,255,cv2.THRESH_BINARY_INV)
            contours,hierarchy = cv2.findContours(thresh, 
                                              cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            mask = np.zeros(image.shape[:2],dtype = image.dtype)
            for contour in contours:
                if cv2.contourArea(contour) > 10:
                    x,y,w,h = cv2.boundingRect(contour)
                    cv2.drawContours(mask,[contour],0,(255),-1)

            result = cv2.bitwise_and(image,image,mask=mask)        
            result = cv2.bitwise_not(result)

            xxx = np.bitwise_and(image,result)

            cv2.imwrite('image_1.png',xxx)
            #Draw contours

            Test = cv2.imread('image_1.png')
            gray = cv2.cvtColor(Test,cv2.COLOR_BGR2GRAY)

            contours ,hier = cv2.findContours(gray,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
            cv2.drawContours(Test,contours,-1,(0,255,0),3)
            #keep the largest contour

            largest = sorted(contours,key = cv2.contourArea)
            mask = np.zeros(Test.shape,np.uint8)
            cv2.drawContours(mask,[largest[-1]],0,(255,255,255),-1)
            removed = cv2.bitwise_and(Test,mask)

            cv2.imwrite('removed.png',removed)
        
            gray_image = cv2.cvtColor(removed,cv2.COLOR_BGR2GRAY)

            (thresh, bin_img) = cv2.threshold(gray_image,50,255,cv2.THRESH_BINARY)

            cv2.imwrite('Finalimage.png',bin_img)
            pl = cv2.imread('Finalimage.png',0)
            pp = np.reshape(pl,img.shape[0]*img.shape[1])
            self.value = np.sum([pp>107])
        except Exception:
            a=0
            
    def cls_screen(self, *largs):
        self.dist = 0
        self.value = 0
        self.path = ''
        
        self.ids.lb1.text = 'Distance: {} cm'.format(self.dist)
        self.ids.lb2.text = 'Result dier: {} D'.format(self.value)
        
        result_screen = self.manager.get_screen('distanceu')
        result_screen.ids.input.text = ''
        
class TestApp(App):

    def build(self):
        file = "StorageFile"
        try:
            os.mkdir(file)
            s = os.getcwd()+"\\"+file
            os.chdir(s)
        except Exception:
            s = os.getcwd()+"\\"+file
            os.chdir(s)
        
        blank_image = np.zeros(shape=[512,512],dtype=np.uint8)
        cv2.imwrite('image.png',blank_image)
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(CameraScreen(name='camera'))
        sm.add_widget(MyWidget(name='files'))
        sm.add_widget(DisplayImageScreen(name='display'))
        sm.add_widget(DistanceScreen(name='distance'))
        sm.add_widget(DistanceUScreen(name='distanceu'))
        sm.add_widget(ResultScreen(name='result'))
        sm.add_widget(ResultUScreen(name='resultu'))
        
        return sm

if __name__ == '__main__':
    TestApp().run()
