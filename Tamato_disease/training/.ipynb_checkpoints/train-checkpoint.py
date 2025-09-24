import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
from tensorflow.keras import models,layers
import matplotlib.pyplot as plt


# all images size already trained(256*256 dimension)
IMAGE_SIZE=256
BATCH_SIZE=32 #that is standard batch size

dataset=tf.keras.preprocessing.image_dataset_from_directory(
    "PlantVillage",
    shuffle=True,
    image_size=(IMAGE_SIZE,IMAGE_SIZE),
    batch_size=BATCH_SIZE
)


# folder name is your class name
class_names=dataset.class_names
print(class_names)


#141*32==(output of datase*batchsize)=len of dataset
print(len(dataset))

print()

for image_batch,label_batch in dataset.take(1):
    print(image_batch.shape)
    print(label_batch.numpy())
channels=3

print()
# show visualizarion of first image
plt.figure(figsize=(50,10))
for image_batch,label_batch in dataset.take(1):
    for i in range(4):
        ax=plt.subplot(3,4,i+1)

        plt.imshow(image_batch[i].numpy().astype('uint8'))
        plt.title(class_names[label_batch[i]])
        plt.axis('off')
        plt.show()


