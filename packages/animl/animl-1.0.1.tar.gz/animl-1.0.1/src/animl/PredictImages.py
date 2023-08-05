from DetectMD import load_and_run_detector_batch
from PIL import Image
import numpy as np
from ImageCropGenerator import GenerateCropsFromFile


def predict_images(images, model, tf_file, confidence=0.5):
    if len(images) > 0:
        results = load_and_run_detector_batch(images, checkpoint_path="NA", confidence_threshold=confidence,
                                              checkpoint_frequency=-1, results=[], detector_file=tf_file)
        print(results)

        # Make a list of File names from the results
        # Make a list of bounding boxes
        bboxes = []
        filenames = []
        for dictionary in results:
            detections = dictionary['detections']
            if len(detections) > 0:
                detection_dictionary = detections[0]
                bboxes.append(detection_dictionary['bbox'])

                image = Image.open(dictionary['file'])
                image_path = f"image_{detection_dictionary['bbox']}.jpg"

                image.save(image_path)
                filenames.append(image_path)

        # Make bboxes into array
        bboxes = np.array(bboxes)

        # Create Generator
        if len(filenames) > 0:
            generator = GenerateCropsFromFile(filenames, bboxes)
            predictions = model.predict(generator)
            return predictions
