from .verify import get_errors_fails, mark_incomplete, mark_complete
import os

task1_id = '6cb98012-99d5-4dab-82c7-3ba61f1e9aac' # Check out the requests users are sending to your system
task2_id = 'f65ab939-e4a3-4090-aa60-66ed53991941' # Run the API
task3_id = 'c8d2e785-04c2-4b3d-8c5c-0e93cd6631a9' # Decode the image
task4_id = '32699ae4-5d65-48ea-9411-1077cb4a4bbc' # Save the input image to the cloud
task5_id = '19b54de2-c555-472c-9124-9db33834f23d' # Take a look at some of the images in S3

# test_netcat(self):
# test_print_image_name(self):
# test_decoding_image(self):
# test_save_to_s3(self):
# test_check_images_in_s3(self):


if 'milestone_1_p1.txt' in os.listdir('.'):
    errors = get_errors_fails('milestone_1_p1.txt')
    print(errors)

    # If there are no errors, mark everything as complete
    if len(errors) == 0:
        mark_complete(task1_id)
        mark_complete(task2_id)
        mark_complete(task3_id)
        mark_complete(task4_id)
        mark_complete(task5_id)

    # Check if hangman_solution.py is in the repo
    elif 'test_netcat' in errors:
        # mark_incomplete(task2_id, message='There is no hangman_solution.py file inside the hangman folder')
        mark_incomplete(task1_id)
        mark_incomplete(task2_id)
        mark_incomplete(task3_id)
        mark_incomplete(task4_id)
        mark_incomplete(task5_id)
        print(errors['test_netcat'])
    # Check if they are identical
    elif 'test_print_image_name' in errors:
        mark_complete(task1_id)
        mark_incomplete(task2_id)
        mark_incomplete(task3_id)
        mark_incomplete(task4_id)
        mark_incomplete(task5_id)
        print(errors['test_print_image_name'])
    elif 'test_decoding_image' in errors:
        mark_complete(task1_id)
        mark_complete(task2_id)
        mark_incomplete(task3_id)
        mark_incomplete(task4_id)
        mark_incomplete(task5_id)
        print(errors['test_decoding_image'])
    elif 'test_save_to_s3' in errors:
        mark_complete(task1_id)
        mark_complete(task2_id)
        mark_complete(task3_id)
        mark_incomplete(task4_id)
        mark_incomplete(task5_id)
        print(errors['test_save_to_s3'])
    elif 'test_check_images_in_s3' in errors:
        mark_complete(task1_id)
        mark_complete(task2_id)
        mark_complete(task3_id)
        mark_complete(task4_id)
        mark_incomplete(task5_id)
        print(errors['test_check_images_in_s3'])

else:
    mark_incomplete(task1_id)
    mark_incomplete(task2_id)
    mark_incomplete(task3_id)
    print('milestone_1_p2.txt is not in the directory')