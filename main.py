import numpy as np

from models.cnn import CNN
from models.cnn_grl import CNNGRL
from utils.preprocessing import get_data
from utils.config import *


(x_train, y_train), (x_test, y_test) = get_data(image_size=IMAGE_SIZE, channels=CHANNELS, domains=DOMAINS, num_classes=NUM_CLASSES, subset=SUBSET, ignore_labels=IGNORE_LABELS)

architecture = 'CNNGRL'

if architecture == 'CNN':
    model = CNN()
    y_train = y_train[0]
    y_test = y_test[0]
elif architecture == 'CNNGRL':
    model = CNNGRL()

model._run_all(x_train, x_test, y_train, y_test, num_classes=NUM_CLASSES, batch_size=BATCH_SIZE, epochs=EPOCHS, log_file=LOG_FILE, save_dir=SAVE_DIR, model_name=MODEL_NAME)
