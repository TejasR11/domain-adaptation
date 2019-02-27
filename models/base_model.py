import keras
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D, Input
from keras.models import Model
from keras.callbacks import ReduceLROnPlateau, EarlyStopping, CSVLogger
from keras.optimizers import rmsprop
import os
from utils.config import *

class BaseModel():
    def __init__(self, loss='categorical_crossentropy'):
        self.model = None
        self.loss = loss
        self.opt = rmsprop(lr=10e-5, decay=1e-6)

    def _build(self, num_classes=NUM_CLASSES):
        inputs = Input(shape=(32, 32, 3))
        x = Flatten()(inputs)
        predictions = Dense(num_classes, activation='softmax')(x)
        self.model = Model(inputs=inputs, outputs=predictions)

    def _compile(self):
        if not self.model:
            raise Exception("Trying to compile model but it isn't built")
        self.model.compile(loss=self.loss, optimizer=self.opt, metrics=['accuracy'])

    def _fit(self, x_train, y_train, x_test=None, y_test=None, batch_size=BATCH_SIZE, epochs=EPOCHS, log_file=CNN_LOG_FILE):
        if not self.model:
            raise Exception("Trying to fit model but it isn't built")
        early_stopping = EarlyStopping(monitor='val_loss', min_delta=10e-4, patience=10, restore_best_weights=True, verbose=1)
        reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=10e-7, verbose=1)
        csv_logger = CSVLogger(log_file)
        self.model.fit(x_train, y_train,
            batch_size=batch_size,
            epochs=epochs,
            validation_data=(x_test, y_test),
            shuffle=True,
            callbacks=[reduce_lr, early_stopping, csv_logger],)

    def _save(self, save_dir=SAVE_DIR, model_name=CNN_MODEL_NAME):
        if not self.model:
            raise Exception("Trying to save model but it isn't built")
        if not os.path.isdir(save_dir):
            os.makedirs(save_dir)
        model_path = os.path.join(save_dir, model_name)
        self.model.save(model_path)
        print('Saved trained model at %s ' % model_path)

    def _evaluate(self, x_test, y_test):
        if not self.model:
            raise Exception("Trying to evaluate model but it isn't built")
        scores = self.model.evaluate(x_test, y_test, verbose=0)
        print('Test accuracy:', scores[1])

    def _run_all(self, x_train, x_test, y_train, y_test, num_classes=NUM_CLASSES, batch_size=BATCH_SIZE, epochs=EPOCHS, log_file=CNN_LOG_FILE, save_dir=SAVE_DIR, model_name=CNN_MODEL_NAME):
        self._build(num_classes=num_classes)
        self._compile()
        print(self.model.summary())
        self._fit(x_train, y_train, x_test, y_test, batch_size=batch_size, epochs=epochs, log_file=log_file)
        self._save(save_dir=save_dir, model_name=model_name)
        self._evaluate(x_test, y_test)

    def _load_weights(self, path):
        self.model.load_weights(path)

    def _load_and_evaluate(self, path, x_test, y_test, num_classes=NUM_CLASSES):
        self._build(num_classes)
        self._compile()
        self._load_weights(path)
        self._evaluate(x_test, y_test)
