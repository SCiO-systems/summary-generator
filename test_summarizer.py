import copy
import unittest
import json
import summary_generator
from testcontainers.kafka import KafkaContainer
from confluent_kafka import Producer,Consumer
from dotenv import load_dotenv


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.text = """Observing the sources of data used to train the DL model at every paper, large datasets of images are mainly used, containing thousands of images in some cases, either real ones (e.g. (Mohanty et al., 2016; Reyes et al., 2015; Dyrmann et al., 2016a)), or synthetic produced by the authors (Rahnemoonfar and Sheppard, 2017; Dyrmann et al., 2016b). Some datasets originate from well-known and publicly-available datasets such as PlantVillage, LifeCLEF, MalayaKew, UC Merced and Flavia (see Appendix C), while others constitute sets of real images collected by the authors for their research needs (e.g. (Sladojevic et al., 2016; Bargoti and Underwood, 2016; Xinshao and Cheng, 2015; Sψrensen et al., 2017)). Papers dealing with land cover, crop type classification and yield estimation, as well as some papers related to weed detection employ a smaller number of images (e.g. tens of images), produced by UAV (Lu et al., 2017; Rebetez et al., 2016; Milioto et al., 2017), airborne (Chen et al., 2014; Luus et al., 2015) or satellitebased remote sensing (Kussul et al., 2017; Minh et al., 2017; Ienco et al., 2017; Ruίwurm and Kφrner, 2017). A particular paper investigating segmentation of root and soil uses images from X-ray tomography (Douarre et al., 2016). Moreover, some papers use text data, collected either from repositories (Kuwata and Shibasaki, 2015; Sehgal et al., 2017) or field sensors (Song et al., 2016; Demmers et al., 2010, 2012). In general, the more complicated the problem to be solved, the more data is required. For example, problems involving large number of classes to identify (Mohanty et al., 2016; Reyes et al., 2015; Xinshao and Cheng, 2015) and/or small Variation among the classes (Luus et al., 2015; Ruίwurm and Kφrner, 2017; Yalcin, 2017; Namin et al., 2017; Xinshao and Cheng, 2015), require large number of input images to train their models."""
        #  4.3. Data variation Variation between classes is necessary for the DL models to be able to differentiate features and characteristics, and perform accurate classifications.2 Hence, accuracy is positively correlated with variation among classes. Nineteen papers (47%) revealed some aspects of poor data variation. Luus et al. (2015) observed high relevance between some land cover classes (i.e. medium density and dense residential, buildings and storage tanks) while Ienco et al. (2017) found that tree crops, summer crops and truck farming were classes highly mixed. A confusion between maize and soybeans was evident in Kussul et al. (2017) and variation was low in botanically related crops, such as meadow, fallow, triticale, wheat, and rye (Ruίwurm and Kφrner, 2017). Moreover, some particular views of the plants (i.e. flowers and leaf scans) offer different classification accuracy than branches, stems and photos of the entire plant. A serious issue in plant phenology recognition is the fact that appearances change very gradually and it is challenging to distinguish images falling into the growing durations that are in the middle of two successive stages (Yalcin, 2017; Namin et al., 2017). A similar issue appears when assessing the quality of vegetative development (Minh et al., 2017). Furthermore, in the challenging problem of fruit counting, the models suffer from high occlusion, depth variation, and uncontrolled illumination, including high color similarity between fruit/foliage (Chen et al., 2017; Bargoti and Underwood, 2016). Finally, identification of weeds faces issues with respect to lighting, resolution, and soil type, and small variation between weeds and crops in shape, texture, color and position (i.e. overlapping) (Dyrmann et al., 2016a; Xinshao and Cheng, 2015; Dyrmann et al., 2017). In the large majority of the papers mentioned above (except from Minh et al. (2017)), this low variation has affected classification accuracy significantly, i.e. more than 5%. 4.4. Data pre-processing The large majority of related work (36 papers, 90%) involved some image pre-processing steps, before the image or particular characteristics/ features/statistics of the image were fed as an input to the DL model. The most common pre-processing procedure was image resize (16 papers), in most cases to a smaller size, in order to adapt to the requirements of the DL model. Sizes of 256Χ256, 128Χ128, 96Χ96 and 60Χ60 pixels were common. Image segmentation was also a popular practice (12 papers), either to increase the size of the dataset (Ienco et al., 2017; Rebetez et al., 2016; Yalcin, 2017) or to facilitate the learning process by highlighting regions of interest (Sladojevic et al., 2016; Mohanty et al., 2016; Grinblat et al., 2016; Sa et al., 2016; Dyrmann et al., 2016a; Potena et al., 2016) or to enable easier data annotation by experts and volunteers (Chen et al., 2017; Bargoti and Underwood, 2016). Background removal (Mohanty et al., 2016; McCool et al., 2017; Milioto et al., 2017), foreground pixel extraction (Lee et al., 2015) or non-green pixels removal based on NDVI masks (Dyrmann et al., 2016a; Potena et al., 2016) were also performed to reduce the datasets’ overall noise. Other operations involved the creation of bounding boxes (Chen et al., 2017; Sa et al., 2016; McCool et al., 2017; Milioto et al., 2017) to facilitate detection of weeds or counting of fruits. Some datasets were converted to grayscale (Santoni et al., 2015; Amara et al., 2017) or to the HSV color model (Luus et al., 2015; Lee et al., 2015). Furthermore, some papers used features extracted from the images as input to their models, such as shape and statistical features (Hall et al., 2015), histograms (Hall et al., 2015; Xinshao and Cheng, 2015; Rebetez et al., 2016), Principal Component Analysis (PCA) filters (Xinshao and Cheng, 2015), Wavelet transformations (Kuwata and Shibasaki, 2015) and Gray Level Co-occurrence Matrix (GLCM) features (Santoni et al., 2015). Satellite or aerial images involved a combination of pre-processing steps such as orthorectification (Lu et al., 2017; Minh et al., 2017) calibration and terrain correction (Kussul et al., 2017; Minh et al., 2017) and atmospheric correction (Ruίwurm and Kφrner, 2017). 4.5. Data augmentation It is worth-mentioning that some of the related work under study (15 papers, 37%) employed data augmentation techniques (Krizhevsky et al., 2012), to enlarge artificially their number of training images. This helps to improve the overall learning procedure and performance, and for generalization purposes, by means of feeding the model with varied data. This augmentation process is important for papers that possess only small datasets to train their DL models, such as (Bargoti and Underwood, 2016; Sladojevic et al., 2016; Sψrensen et al., 2017; Mortensen et al., 2016; Namin et al., 2017 and Chen et al., 2017). This process was especially important in papers where the authors trained their models using synthetic images and tested them on real ones (Rahnemoonfar and Sheppard, 2017 and Dyrmann et al., 2016b). In this case, data augmentation allowed their models to generalize and be able to adapt to the real-world problems more easily.

    def test_wrong_json_type(self):
        sample_json = []

        summarizer = summary_generator.CiGi_Summarizer(sample_json)
        self.assertEqual(summarizer.digest_input(), "not_dict", "JSON PROVIDED IS NOT OF CORRECT FORMAT")

    def test_missing_input_json_fields(self):
        sample_json = {
          "metadata_id": "12345",
          "text": "The input text to be summarized. It can be a long article, document, or any textual content.",
          "part": 2,
          "chapter": "Methods",
          "summary_length": 100,
          "word_count": 100,
          "language": "en",
          "algorithm": "LSA"
        }
        del sample_json['algorithm']
        del sample_json['language']
        summarizer = summary_generator.CiGi_Summarizer(sample_json)
        self.assertNotEqual(summarizer.digest_input(), [], "MISSING INPUT JSON FIELDS DETECTED")

    def test_empty_input_json_fields(self):
        sample_json = {
            "metadata_id": "12345",
            "text": "The input text to be summarized. It can be a long article, document, or any textual content.",
            "part": 2,
            "chapter": "Methods",
            "summary_length": 100,
            "word_count": 100,
            "language": "en",
            "algorithm": "LSA"
        }
        sample_json['part'] = None
        sample_json['chapter'] = ""
        summarizer = summary_generator.CiGi_Summarizer(sample_json)
        self.assertNotEqual(summarizer.digest_input(), [], "EMPTY INPUT JSON FIELDS DETECTED")

    def test_data_types_input_json_fields(self):
        sample_json = {
            "metadata_id": 12345,
            "text": "The input text to be summarized. It can be a long article, document, or any textual content.",
            "part": True,
            "chapter": {},
            "summary_length": 3.9,
            "word_count": "100",
            "language": ["en"],
            "algorithm": "LSA"
        }

        summarizer = summary_generator.CiGi_Summarizer(sample_json)
        self.assertNotEqual(summarizer.digest_input(), {}, "WRONG DATA TYPES INPUT JSON FIELDS DETECTED")

    # def test_model_initialization(self):
    #     sample_json = {
    #           "metadata_id": "12345",
    #           "text": "The input text to be summarized. It can be a long article, document, or any textual content.",
    #           "part": 2,
    #           "chapter": "Methods",
    #           "summary_length": 100,
    #           "word_count": 100,
    #           "language": "en",
    #           "algorithm": "LSA"
    #         }
    #     summarizer = summary_generator.CiGi_Summarizer(sample_json)
    #     summarizer.digest_input()
    #     self.assertEqual(summarizer.initialize_summarizer().startswith("cuda"), True, "MODEL IS NOT USING CUDA")
    
    def test_summary_length(self):
        sample_json = {
            "metadata_id": "12345",
            "text": self.text,
            "part": 2,
            "chapter": "Methods",
            "summary_length": 100,
            "word_count": 100,
            "language": "en",
            "algorithm": "LSA"
        }
        summarizer = summary_generator.CiGi_Summarizer(sample_json)
        summarizer.digest_input()
        summarizer.initialize_summarizer()
        summary = summarizer.summarize()
        summary_length = len(summary.split(" "))
        self.assertGreaterEqual(summary_length, sample_json["summary_length"]-50, "SUMMARY LENGTH BELOW LOWER LIMIT")
        self.assertLessEqual(summary_length, sample_json["summary_length"]+50, "SUMMARY LENGTH ABOVE UPPER LIMIT")

    def test_kafka_produce(self):
        sample_json = {
            "metadata_id": "12345",
            "text": self.text,
            "part": 2,
            "chapter": "Methods",
            "summary_length": 100,
            "word_count": 100,
            "language": "en",
            "algorithm": "LSA"
        }
        summarizer = summary_generator.CiGi_Summarizer(sample_json)
        summarizer.digest_input()
        summarizer.initialize_summarizer()
        summarizer.summarize()
        summarizer_output = json.dumps(summarizer.output_data)

        with KafkaContainer(image='confluentinc/cp-kafka:7.5.0') as kafka_container:
            bootstrap_server = kafka_container.get_bootstrap_server()

            # print("**************************************************************")
            # print("**************************************************************")
            # print(bootstrap_server)
            # print("**************************************************************")
            # print("**************************************************************")
            config = {
                'bootstrap.servers': bootstrap_server
            }
            topic = "kafka_test"

            def delivery_callback(err, msg):
                if err:
                    print('ERROR: Message failed delivery: {}'.format(err))
                    print("Failed to deliver message: %s" % (str(msg)))
                else:
                    if msg.value() == None:
                        print("Produced event to topic {topic}: key = {key:12} value = {value:12}".format(
                            topic=msg.topic(), key=msg.key().decode('utf-8'), value=""))
                    else:
                        print("Produced event to topic {topic}: key = {key:12} value = {value:12}".format(
                            topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))

            # Create Producer instance
            producer = Producer(config)
            producer.produce(topic, key="kafka_produce_test", value=summarizer_output, callback=delivery_callback)

            producer.flush()

            config = {
                'bootstrap.servers': bootstrap_server,
                'group.id': 'python_example_group_1',
                'auto.offset.reset': 'earliest'}
            # Create Consumer instance
            consumer = Consumer(config)
            consumer.subscribe([topic])

            # Poll for new messages from Kafka and print them.
            try:
                while True:
                    msg = consumer.poll(1.0)
                    if msg is None:
                        # Initial message consumption may take up to
                        # `session.timeout.ms` for the consumer group to
                        # rebalance and start consuming
                        print("Waiting...")
                    elif msg.error():
                        print("ERROR: %s".format(msg.error()))
                    else:
                        # Extract the (optional) key and value, and print.
                        if msg.value() == None:
                            print("Consumed event to topic {topic}: key = {key:12} value = {value:12}".format(
                                topic=msg.topic(), key=msg.key().decode('utf-8'), value=""))
                        else:
                            print("Consumed event to topic {topic}: key = {key:12} value = {value:12}".format(
                                topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))

                            consumed_data = json.loads(msg.value())
                            print(consumed_data)
                            self.assertIsInstance(consumed_data, dict, "ERROR IN RECEIVED JSON")
                            break
            except KeyboardInterrupt:
                pass
            finally:
                # Leave group and commit final offsets
                consumer.close()



if __name__ == '__main__':
    unittest.main()
