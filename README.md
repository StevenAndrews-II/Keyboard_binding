# ⌨️ Keyboard Binding API  

A lightweight Python library by **Steven Andrews II** for managing **keyboard bindings** in applications.  
It supports **customizable key registration, key remapping, toggled or continuous execution, function binding, and persistence with JSON storage**.  

---

## ✨ Features  

- 📦 Persistent storage of key mappings in JSON  
- ➕ Add / remove keys dynamically  
- 🔄 Remap keys to other keys or functions  
- ⚡ Bind functions to keys (head & tail execution)  
- 📚 Bulk bind / clear / swap bindings across keys  
- 🎛️ Toggle vs continuous modes (edge-triggered or continuous function calls)  
- 🪟 Application focus check (only processes input when target window is active)  

---

## 🚀 Installation  

This library requires the following dependencies:  

```bash
pip install keyboard pygetwindow
```

Clone this repo:  

```bash
git clone https://github.com/StevenAndrews-II/Keyboard_binding.git
cd Keyboard_binding
```

---

## 📖 Usage Example  

```python
from keyboard_binding import keyboard_binding

# Initialize with the window title of your app
kb = keyboard_binding(APP_TITLE="MyApp")

# Bind a simple function
def on_press():
    print("A was pressed!")

def on_release():
    print("A was released!")

kb.bind("a", head_func=on_press, tail_func=on_release, toggle=True)

# Main loop
while True:
    kb.update()
```

---

## 📚 API Reference  

### 🔑 Key Management  
- `load_keys(FILE="keyboard_map.json")` → load key mappings from JSON  
- `save_keys(FILE="keyboard_map.json")` → save current mappings  
- `add_key(key, remap=None, toggle=True)` → register a new key  
- `remove_key(key)` → remove a registered key  
- `remap(key, to_key)` → remap a key to another  

### 🔗 Binding Management  
- `bind(key, head_func, tail_func, toggle=True)` → bind single functions to a key  
- `bulk_bind(key, head_list, tail_list, toggle=True)` → bind lists of functions  
- `clear_bind(key)` → clear head & tail bindings  
- `remove_bind(key, head_tail, func)` → remove a specific function  
- `swap_binds(key_a, key_b)` → swap bindings between keys  
- `get_binds(key)` → get lists of head & tail functions  

### ⚙️ Execution  
- `update()` → processes all keys (should be called at a fixed FPS in your loop)  

---

## ⚠️ Notes  

- Keys only trigger when the **target window is focused** (`APP_TITLE` must match window title).  
- Toggle mode = edge-triggered execution (press/release).  
- Non-toggle mode = continuous execution + release events.  

---

## 🛠️ Project Info  

- Author: **Steven Andrews II**  
- Date: 08/28/2025  
- Version: 1.0  
- License: MIT
