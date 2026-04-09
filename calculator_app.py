from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import math
from kivy.uix.popup import Popup
from kivy.uix.label import Label

class CalculatorApp(App):
    def build(self):
        self.current = "0"
        self.previous = ""
        self.operator = ""
        self.should_reset = False
        
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 显示屏
        self.display = TextInput(
            text='0',
            readonly=True,
            font_size=40,
            size_hint_y=None,
            height=100,
            halign='right',
            multiline=False,
            background_color=[1, 1, 1, 1],
            foreground_color=[0, 0, 0, 1]
        )
        main_layout.add_widget(self.display)
        
        # 按钮布局
        buttons_layout = GridLayout(cols=4, spacing=5, size_hint_y=1)
        
        buttons = [
            ("C", "clear"), ("±", "sign"), ("√", "sqrt"), ("/", "divide"),
            ("7", "7"), ("8", "8"), ("9", "9"), ("*", "multiply"),
            ("4", "4"), ("5", "5"), ("6", "6"), ("-", "subtract"),
            ("1", "1"), ("2", "2"), ("3", "3"), ("+", "add"),
            ("0", "0"), (".", "decimal"), ("DEL", "delete"), ("=", "equals"),
            ("sin", "sin"), ("cos", "cos"), ("ln", "ln"), ("!", "factorial")
        ]
        
        for button_text, button_type in buttons:
            btn = Button(
                text=button_text,
                font_size=20,
                background_normal='',
                background_color=self.get_button_color(button_type)
            )
            btn.bind(on_press=lambda x, bt=button_type: self.handle_button(bt))
            buttons_layout.add_widget(btn)
        
        main_layout.add_widget(buttons_layout)
        return main_layout
    
    def get_button_color(self, button_type):
        if button_type in ['add', 'subtract', 'multiply', 'divide', 'equals', 'sqrt', 'sin', 'cos', 'ln', 'factorial']:
            return [1, 0.58, 0, 1]  # 橙色
        elif button_type in ['clear', 'delete', 'sign']:
            return [0.65, 0.65, 0.65, 1]  # 灰色
        else:
            return [0.2, 0.2, 0.2, 1]  # 深灰色
    
    def handle_button(self, button_type):
        try:
            if button_type.isdigit() or button_type == 'decimal':
                self.input_number(button_type)
            elif button_type in ['add', 'subtract', 'multiply', 'divide']:
                self.input_operator(button_type)
            elif button_type == 'equals':
                self.calculate()
            elif button_type == 'clear':
                self.clear()
            elif button_type == 'delete':
                self.delete_last()
            elif button_type == 'sign':
                self.toggle_sign()
            elif button_type == 'sqrt':
                self.square_root()
            elif button_type == 'sin':
                self.trig_function('sin')
            elif button_type == 'cos':
                self.trig_function('cos')
            elif button_type == 'ln':
                self.natural_log()
            elif button_type == 'factorial':
                self.factorial()
        except Exception as e:
            self.show_error(f"计算错误: {str(e)}")
    
    def input_number(self, num):
        if self.should_reset:
            self.current = "0"
            self.should_reset = False
        
        if self.current == "0" and num != 'decimal':
            self.current = "0" if num == "0" else num
        elif num == 'decimal' and "." not in self.current:
            self.current += "."
        elif num != 'decimal':
            self.current += num
        
        self.display.text = self.current
    
    def input_operator(self, op):
        if self.operator and not self.should_reset:
            self.calculate()
        
        self.previous = self.current
        self.operator = op
        self.should_reset = True
    
    def calculate(self):
        if self.operator and self.previous:
            try:
                prev_val = float(self.previous)
                curr_val = float(self.current)
                
                if self.operator == 'add':
                    result = prev_val + curr_val
                elif self.operator == 'subtract':
                    result = prev_val - curr_val
                elif self.operator == 'multiply':
                    result = prev_val * curr_val
                elif self.operator == 'divide':
                    if curr_val == 0:
                        self.show_error('除数不能为零')
                        return
                    result = prev_val / curr_val
                
                # 格式化结果
                if result == int(result):
                    self.current = str(int(result))
                else:
                    self.current = f"{result:.10g}"
                
                self.display.text = self.current
                self.operator = ""
                self.previous = ""
                self.should_reset = True
            except Exception as e:
                self.show_error(f'计算错误: {str(e)}')
    
    def clear(self):
        self.current = "0"
        self.previous = ""
        self.operator = ""
        self.should_reset = False
        self.display.text = "0"
    
    def delete_last(self):
        if len(self.current) > 1:
            self.current = self.current[:-1]
        else:
            self.current = "0"
        self.display.text = self.current
    
    def toggle_sign(self):
        if self.current != "0":
            if self.current.startswith("-"):
                self.current = self.current[1:]
            else:
                self.current = "-" + self.current
            self.display.text = self.current
    
    def square_root(self):
        try:
            val = float(self.current)
            if val < 0:
                self.show_error('负数不能开平方根')
                return
            result = math.sqrt(val)
            if result == int(result):
                self.current = str(int(result))
            else:
                self.current = f"{result:.10g}"
            self.display.text = self.current
            self.should_reset = True
        except Exception as e:
            self.show_error(f'计算错误: {str(e)}')
    
    def trig_function(self, func_name):
        try:
            angle_deg = float(self.current)
            angle_rad = math.radians(angle_deg)
            
            if func_name == 'sin':
                result = math.sin(angle_rad)
            elif func_name == 'cos':
                result = math.cos(angle_rad)
            
            self.current = f"{result:.10g}"
            self.display.text = self.current
            self.should_reset = True
        except Exception as e:
            self.show_error(f'计算错误: {str(e)}')
    
    def natural_log(self):
        try:
            val = float(self.current)
            if val <= 0:
                self.show_error('真数必须大于0')
                return
            result = math.log(val)
            self.current = f"{result:.10g}"
            self.display.text = self.current
            self.should_reset = True
        except Exception as e:
            self.show_error(f'计算错误: {str(e)}')
    
    def factorial(self):
        try:
            val = float(self.current)
            if val < 0 or val != int(val):
                self.show_error('阶乘只能计算非负整数')
                return
            result = math.factorial(int(val))
            self.current = str(result)
            self.display.text = self.current
            self.should_reset = True
        except Exception as e:
            self.show_error(f'计算错误: {str(e)}')
    
    def show_error(self, message):
        popup = Popup(title='错误', content=Label(text=message), size_hint=(0.6, 0.4))
        popup.open()

if __name__ == '__main__':
    CalculatorApp().run()
