"""Demo for test if I can bind some data to a instance from a fixed class.
Not recommended to use this in production code.
"""

import pytest
import gc
from guppy import hpy

class DummyClass:
    def __init__(self, data):
        self.data = data
    
    def callable_instance(self):
        return f"Data: {self.callable_instance.__dict__.get('func_data', 'No func data')}"

    def __del__(self):
        print(f"DummyClass instance with data '{self.data}' is being deleted.")

def setattr_to_instance(instance, data_name, data_value):
    assert not hasattr(instance, data_name), f"instance already has attribute '{data_name}' with value '{getattr(instance, data_name)}'"
    setattr(instance, data_name, data_value)
    
def add_data_to_instance(instance, data_name, data_value):
    assert not hasattr(instance, data_name), f"instance already has attribute '{data_name}' with value '{getattr(instance, data_name)}'"
    instance.__dict__[data_name] = data_value

def test_setattr_to_instance():
    instance = DummyClass("initial")
    setattr_to_instance(instance, 'new_data', 'value1')
    assert hasattr(instance, 'new_data')
    assert instance.new_data == 'value1'

def test_add_data_to_instance():
    instance = DummyClass("initial") 
    add_data_to_instance(instance, 'new_data', 'value2')
    assert hasattr(instance, 'new_data')
    assert instance.new_data == 'value2'

# 虽然每次生成新的instance时，method对象都是临时对象，但是直接修改__dict__属性后, python会缓存method对象的__dict__属性
def test_callable_instance():
    instance = DummyClass("initial").callable_instance
    add_data_to_instance(instance, 'new_data', 'value3')
    assert hasattr(instance, 'new_data')
    assert instance.new_data == 'value3'

# method对象不支持setattr操作
def test_callable_instance_with_setattr():
    instance = DummyClass("initial").callable_instance
    with pytest.raises(AttributeError):
        setattr_to_instance(instance, 'new_data', 'value4')

def test_memory_usage():
    h = hpy()
    initial_memory = h.heap().size
    instance = DummyClass("initial")
    setattr_to_instance(instance, 'new_data', 'value5')
    final_memory = h.heap().size
    assert final_memory > initial_memory, "Memory usage should increase after adding data to instance"

def test_callable_instance_memory():
    a = DummyClass("initial")
    add_data_to_instance(a.callable_instance, 'func_data', '1')
    a.callable_instance() 
    a.callable_instance()
