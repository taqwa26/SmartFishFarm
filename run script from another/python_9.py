import time
x=5
myVars = {'x':x}
exec(open('python_8.py').read(), myVars)
time.sleep(5)
x=10
print('masih jalan')