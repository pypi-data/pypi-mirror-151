from ast import arg
from re import sub
import unittest
import os
from urllib.request import urlopen
from subprocess import Popen, PIPE, STDOUT

# print(process)

class ImageSegmentationTestCase(unittest.TestCase):
    def setUp(self) -> None:
        api_script = 'api.py'
        with open(api_script, 'r') as f:
            self.api_code = f.read()
        self.user_id = os.environ['USER_ID']


    def test_netcat(self):
        number_calls = os.environ['NETCAT_CALLS']
        self.assertGreater(number_calls, 0, 'You should have called netcat server to listen port 8080 at least once')
    
    def test_print_image_name(self):
        self.assertIn('print(image_name)', self.api_code, 'You should print the image name in the api.py file. If you have, make sure it has the right syntax')

    def test_decoding_image(self):
        self.assertIn('decode_image(image)', self.api_code, 'You should call the decode_image on the image in the api.py file. If you have, make sure it has the right syntax')
    
    def test_save_to_s3(self):
        bucket_name = self.user_id + '-data'
        self.assertIn(bucket_name, self.api_code, 'You are not using the right name for your bucket. The name of the bucket should look like an id followed by -data. Something like xxxx-xxxxx-xxxx-xxxx-data')
        number_occurrences = self.api_code.count('save_image_to_s3')
        self.assertGreater(number_occurrences, 1, 'You should have called the "save_image_to_s3" function in the api.py file. If you have, make sure it has the right syntax')

    def test_check_images_in_s3(self):
        number_input_images = os.environ['NUMBER_INPUT_IMAGES']
        self.assertGreater(number_input_images, 0, 'You should have uploaded at least one image to S3. If you have, make sure you have the right number of images in your bucket')

    # def test_presence_readme(self):
    #     self.assertIn('api.py', os.listdir('.'), 'You should have a README.md file in your project folder')
    #     with open('README.md', 'r') as f:
    #         readme = f.read()
    #     documentation = urlopen("https://aicore-files.s3.amazonaws.com/api.py")
    #     tdata = str(documentation.read(), 'utf-8')

if __name__ == '__main__':

    unittest.main(verbosity=2)
    