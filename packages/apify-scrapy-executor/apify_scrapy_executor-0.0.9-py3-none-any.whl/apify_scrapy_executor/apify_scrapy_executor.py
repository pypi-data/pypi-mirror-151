import os

from apify_client import ApifyClient

from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.signalmanager import dispatcher


def _upload_to_apify_dataset(items, dataset_id):
    """
    Upload results to Apify certain dataset
    :param items: results of scrapy run
    :param dataset_id: id of the dataset to be uploaded
    """
    try:
        client = ApifyClient(os.environ['APIFY_TOKEN'])
        default_dataset_client = client.dataset(dataset_id)
        default_dataset_client.push_items(items)
    except Exception as e:
        print(f'Could not push items to dataset: {e}')


class SpiderExecutor:
    def __init__(self, spider_class):
        """
        Initialize SpiderExecutor
        :param spider_class: class of the Spider
        """
        self.spider = spider_class

    def run(self, dataset_id: str, args_dict):
        """
        Runs spider class. Before run arguments are added. After run results are uploaded to dataset
        :param dataset_id: Dataset to upload results
        :param args_dict: dictionary of arguments
        :return:
        """
        result = []
        process = CrawlerProcess(get_project_settings())
        client = ApifyClient(os.environ['APIFY_TOKEN'])
        default_dataset_client = client.dataset(dataset_id)

        # defines each item to save to the result
        def crawler_results(signal, sender, item, response, spider):
            default_dataset_client.push_items(item)
            result.append(item)

        dispatcher.connect(crawler_results, signal=signals.item_scraped)

        # adds arguments
        for key in args_dict:
            setattr(self.spider, key, args_dict[key])

        # starts the crawling
        process.crawl(self.spider, args=args_dict)
        process.start()

        # uploads to dataset
        # _upload_to_apify_dataset(result, dataset_id)
