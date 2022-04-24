# this python file is to verify if a function is called inside try and
# this function messes up but goes to next line due to usage of try and except inside this function
# will this throw an exception outside too?

def dip():
    try:
        with open('gooo.py', 'r') as f:
            pass
	# else:
	# 	print(' successful ')
    finally:
        pass
    print('next line is printed no matter what')


try:
    dip()
except:
    print('outside function: function messed up')
