import keyboard
import pygetwindow
import json


''' Keyboard_binding: ( open source )
    
    Storage: 

                    load_keys(FILE = "keyboard_map.json")               ->    loads key binds from a json file 
                    save_keys(FILE = "keyboard_map.json")               ->    saves keymaps to json file 
    
    Key manipulation: 

                    add_key( key )                                      ->    adds a new key to the key register 
                    change_toggle( key )                                ->    changes the toggle state   ->   rising edge call + falling edge call  || continuous function calling + falling edge call
                    remove_key( key )                                   ->    removes a key from the register 
                    remap( key , to_key )                               ->    remaps a key to another keys functions lists 

    Binding manipulation:
   
                    bind( key , head_func , tail_func , toggle )        ->    binds a single head & tail function to a key   ->   toggle = continuous + falling edge || rising + falling
                    bulk_bind( key , [] , [] , toggle )                 ->    binds entire function lists to a key 
                    clear_binds( key )                                  ->    removes all bound functions from head & tail lists 
                    remove_bind( key , bool (heads or tails ) , func )  ->    removes a specific function from the bind list 
                    swap_binds( key_a , key_b )                         ->    swaps key binds with another key 

    Handler:
                    update()                                            ->    should be FPS limited 





    By :                                            Steven Andrews II 
    Date :                                              08/28/25
    Version :                                              1.0
'''


class keyboard_binding():

      def __init__(self,APP_TITLE):

          self.APP_TITLE = APP_TITLE                    # application title  - must be name of the window!      note:  needed for window focus for multi-window applications 

          self.keys  = { # registered application keys 
                                                        # [0] = button mapping / [1] = is pressed value  / [2] = toggle state / [3] = toggle enable
                                                        # [4][0] = head functions //  [4][1] = tail functions
                      "a" : ["a",0,0,True,[[],[]]],    
                      "b" : ["b",0,0,True,[[],[]]],
                      "c" : ["c",0,0,True,[[],[]]],
                      "d" : ["d",0,0,True,[[],[]]],
                      "e" : ["e",0,0,True,[[],[]]],
                      "f" : ["f",0,0,True,[[],[]]],
                      "g" : ["g",0,0,True,[[],[]]],
                      "h" : ["h",0,0,True,[[],[]]],
                      "i" : ["i",0,0,True,[[],[]]],
                      "j" : ["j",0,0,True,[[],[]]],
                      "k" : ["k",0,0,True,[[],[]]],
                      "l" : ["l",0,0,True,[[],[]]],
                      "m" : ["m",0,0,True,[[],[]]],
                      "n" : ["n",0,0,True,[[],[]]],
                      "o" : ["o",0,0,True,[[],[]]],
                      "p" : ["p",0,0,True,[[],[]]],
                      "q" : ["q",0,0,True,[[],[]]],
                      "r" : ["r",0,0,True,[[],[]]],
                      "s" : ["s",0,0,True,[[],[]]],
                      "t" : ["t",0,0,True,[[],[]]],
                      "u" : ["u",0,0,True,[[],[]]],
                      "v" : ["v",0,0,True,[[],[]]],
                      "w" : ["w",0,0,True,[[],[]]],
                      "x" : ["x",0,0,True,[[],[]]],
                      "y" : ["y",0,0,True,[[],[]]],
                      "z" : ["z",0,0,True,[[],[]]],

                      "1" : ["1",0,0,True,[[],[]]],    
                      "2" : ["2",0,0,True,[[],[]]],
                      "3" : ["3",0,0,True,[[],[]]],
                      "4" : ["4",0,0,True,[[],[]]],
                      "5" : ["5",0,0,True,[[],[]]],
                      "6" : ["6",0,0,True,[[],[]]],
                      "7" : ["7",0,0,True,[[],[]]],
                      "8" : ["8",0,0,True,[[],[]]],
                      "9" : ["9",0,0,True,[[],[]]],
                      "0" : ["0",0,0,True,[[],[]]],

                      "shift" : ["shift",0,0,True,[[],[]]], 
                      "ctrl"  : ["ctrl",0,0,True,[[],[]]],
                      "alt"   : ["alt",0,0,True,[[],[]]],
              }
 



      ''' load_keys:
          > loads a json file with key mappings / remappings 
          > if a key exists in the file, but not in the registered. It will create the k,v pair from file  
      '''
      def load_keys(self,FILE = "keyboard_map.json"):
          try:
              with open(FILE, 'r') as f:
                   data = json.load(f)
                   for k,v in data.items():
                       key = self.keys.get(k)
                       if not key:
                           self.add_key(k,v) 
                           continue
                       else:
                           if key != v:
                              key[0] = v
              return True
          except:
              return False


      ''' save_keys:
          > save current map settings to file 
      '''
      def save_keys(self,FILE = "keyboard_map.json"):
          with open(FILE, 'w') as f:
               pack = {k: v[0] for k, v in self.keys.items()}
               json.dump( pack, f, indent=2)



      ''' add_key:
          > Adds a new key to the registered keys list 
      '''
      def add_key(self,key,remap = None,toggle = True):
          if not remap:
              remap = key
          self.keys[key] = [remap,0,0,toggle,[[],[]]] 


      ''' Change_toggle:
          > changes the toggle of a key
      '''
      def change_toggle(self,key):
          if self.keys.get(key):
             if self.keys[key][3] == True:
                self.keys[key][3]  = False
             else:
                self.keys[key][3]  = True
             return True
          return False



      ''' remove_key:
          > Removes a key from the registered keys 
      '''
      def remove_key(self,key):
          if self.keys.get(key):
             self.keys.pop(key)
             return True 
          return False

   

      ''' remap:
          > remaps a key to another keys functions call lists 
      '''
      def remap(self,key,to_key):
          value = self.keys.get(key) 
          if value:
             value[0] = to_key
             return True
          return False



      ''' bind:
          > binds a single function to a key
          > toggle on = rising and falling edge function calls
          > toggle of = continous calling and falling edge calls 
      '''
      def bind(self,key,head_func = None,tail_func = None,toggle = True):         
          value     = self.keys.get(key)
          if value:
              value[3]  = toggle 

              if callable(head_func): 
                 value[4][0].insert(0,head_func)

              if callable(tail_func):
                 value[4][1].insert(0,tail_func)
              return True
          return False



      ''' bulk_bind:
          > binds / extends functions lists 
          > does not check list contents - must be functions 
      '''
      def bulk_bind(self,key,head_list = None,tail_list = None,toggle = True): 
          value     = self.keys.get(key)
          if value:
              value[3]  = toggle 
              if type(head_list) == list:
                 value[4][0].extend(head_list)
              if type(tail_list) == list:
                 value[4][1].extend(tail_list)
              return True
          return False



      ''' clear_bind:
          > clears both function lists ( head & tail )
      '''
      def clear_bind(self,key):        
          value = self.keys.get(key)
          if value:
              value[4][0].clear()
              value[4][1].clear()
              return True
          return False
      


      ''' remove_bind: 
          > removes head or tail functions 
      '''
      def remove_bind(self,key,head_tail,func):  
          value = self.keys.get(key)
          if head_tail == True:
             for i in range(len(value[4][0])):
                if value[4][0][i] == func:  # head functions
                   value[4][0].pop(i)
                   return True
             return False
          for i in range(len(value[4][1])): # tail functions
                if value[4][1][i] == func:
                   value[4][1].pop(i)
                   return True
          return False 



      ''' Swap_binds:
          > copies function lists (head & tail) to new binding
      '''
      def swap_binds(self,key_a,key_b):
           a        = self.keys.get(key_a)
           b        = self.keys.get(key_b)
           if a and b:
               a_head   = a[4][0].copy() 
               a_tail   = a[4][1].copy()
               b_head   = b[4][0].copy()
               b_tail   = b[4][1].copy()
               a[4][0]  = b_head
               a[4][1]  = b_tail
               b[4][0]  = a_head
               b[4][1]  = a_tail
               return True
           return False



      ''' get_binds:
          > returns head and tail functions lists 
      '''
      def get_binds(self,key):
           value = self.keys.get(key)
           if value:
              return value[4][0],value[4][1]
           return None,None



      ''' Internal use: 
          > calls found functions list of a key 
      '''
      def __call_bind(self,key_data,index):
          for i in range(len(key_data[4][index])):
              key_data[4][index][i]()



      ''' Internal use: 
          > get users current screen focus  
      '''
      def __is_app_active(self):
          try:
              win = pygetwindow.getActiveWindow()
              if win.title == self.APP_TITLE:            
                 return True
          except:
              return False



      ''' updates at a fixed FPS ''' 
      def update(self): 
          if not self.__is_app_active():                            
              return
          for k,v in self.keys.items():                            

              remap = v                                           
              if v[0] != k:
                 temp = self.keys.get(v[0]) 
                 if temp:
                    remap = temp

              if keyboard.is_pressed(k):                          
                 remap[1] = 1  
                                                
                 if remap[3]:                                                      
                    if remap[2] == 0:                          
                       self.__call_bind(remap,0)                   
                       remap[2] = 1 
                 else:                           
                       self.__call_bind(remap,0)                   
                       remap[2] = 1                               
              else:                              
                    remap[1] = 0                                  
                    if remap[2] == 1:                             
                       remap[2] = 0
                       self.__call_bind(remap,1)             
