import logging

# set logger configuration
logging.basicConfig(filename='test.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s'
                    )


def dip():
    try:
        with open('gooo.py', 'r') as f:
            pass
        # else:
        # 	print(' successful ')
    finally:
        pass
    logging.info('next line is printed no matter what')


try:
    dip()
except Exception as e:
    logging.info('sdv'+str(e))
