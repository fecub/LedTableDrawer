import logging

#logger = logging.getLogger('example_logger')

# format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S'
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='a', format='[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logging.info('This is an info message')
logging.warning('This will get logged to a file')

# logging.debug('This is a debug message')
# logging.warning('This is a warning message')
# logging.error('This is an error message')
# logging.critical('This is a critical message')
