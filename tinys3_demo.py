import tinys3

# DOESN'T WORK WITH LARGE FILES
s3AK = os.environ['S3_ACCESS_KEY']
s3SK = os.environ['S3_SECRET_KEY']

vids = list(glob.iglob('videos/*.mp4'))

conn = tinys3.Connection(s3AK, s3SK, tls=True)
with open(vids[1], 'rb') as f:
    conn.upload(vids[1].split('/')[1], f, 'obama-weekly-addresses')
