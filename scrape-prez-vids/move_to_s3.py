import boto
from boto.s3.connection import S3Connection, Location
import os
import glob
import math
from filechunkio import FileChunkIO

class awsS3(object):
    def __init__(self, bucket_name='obama-weekly-addresses'):
        # set env variable AWS_CREDENTIAL_FILE
        # http://stackoverflow.com/questions/5396932/why-are-no-amazon-s3-authentication-handlers-ready
        self.conn = boto.connect_s3()
        self.bucket = conn.get_bucket(bucket_name)
        bucket_location = self.bucket.get_location()
        if bucket_location: # fix from https://github.com/boto/boto/issues/2207#issuecomment-60682869
            self.conn = boto.s3.connect_to_region(bucket_location)
            self.bucket = conn.get_bucket(bucket_name)

    def upload_big_file(self, source_path, verbose=True):
        source_size = os.path.getsize(source_path)
        mp = self.bucket.initiate_multipart_upload(os.path.basename(source_path))
        chunk_size = 52428800
        chunk_count = int(math.ceil(source_size / float(chunk_size)))

        if verbose:
            print 'chunk_count:', chunk_count

        for i in range(chunk_count):
            if verbose:
                print 'on chunk:', i
            offset = chunk_size * i
            bytes = min(chunk_size, source_size - offset)
            with FileChunkIO(source_path, 'r', offset=offset, bytes=bytes) as fp:
                mp.upload_part_from_file(fp, part_num=i + 1)

        mp.complete_upload()

    def get_all_files(self):
        # get all files in bucket
        for key in self.bucket.list():
            print key.name.encode('utf-8')

if __name__ == "__main__":
    vids = list(glob.iglob('videos/*.mp4'))
    source_path = vids[1]
