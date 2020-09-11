import logging

logging.basicConfig(
    filename='./logs.txt',
    level=logging.INFO,
    filemode='w',
    format='%(levelname)s-->%(asctime)s:|%(name)s|: %(message)s'

)

logger = logging.getLogger(__name__)

