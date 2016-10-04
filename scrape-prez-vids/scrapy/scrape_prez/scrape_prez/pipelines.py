# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# also http://stackoverflow.com/questions/18081997/scrapy-customize-image-pipeline-with-renaming-defualt-image-name
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem
import scrapy
import os
import shutil
from scrapy.utils.project import get_project_settings

class ScrapePrezPipeline(object):
    def process_item(self, item, spider):
        return item

class PrezVideoPipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        #print(item)
        for file_url in item['file_urls']:
            print('downloading:', file_url)
            #item['files']['path'] = item['breed']
            yield scrapy.Request(file_url)

    # from: http://stackoverflow.com/questions/28007995/how-to-download-scrapy-images-in-a-dyanmic-folder-based-on
    '''
    def item_completed(self, results, item, info):
        for result in [x for ok, x in results if ok]:
            path = result['path']
            #folder = item['breed'][0]
            filename = item['speechTitle'] + '.mp4'

            # http://doc.scrapy.org/en/latest/topics/practices.html#run-scrapy-from-a-script
            settings = get_project_settings()
            storage = settings.get('FILES_STORE')

            target_path = os.path.join(storage, os.path.basename(filename))
            path = os.path.join(storage, path)

            # If path doesn't exist, it will be created
            #if not os.path.exists(os.path.join(storage, folder)):
            #    os.makedirs(os.path.join(storage, folder))

            shutil.move(path, target_path)
            print('saving to:' + str(target_path))

        if self.FILES_RESULT_FIELD in item.fields:
            item[self.FILES_RESULT_FIELD] = [x for ok, x in results if ok]
        return item
    '''
