import argparse
from typing import Dict, List, Union

import telegram
import telegram.ext

from webster.plugins import amazon
from webster.utils import scrapper, slug_utils, telegram_utils

parser = argparse.ArgumentParser()
parser.add_argument('--token')

TOKEN = ""

JOB_COUNTER = 0


class AmazonListingCheckerContext(object):
    KEY_PREFIX = "amazon_listing"

    def __init__(self, chat_id: Union[str, int], *args: List[str]):
        self.chat_id = chat_id
        self.search_term: str = args[0]
        self.title_match: str = args[1] if len(args) >= 2 else None
        self.publisher_match: str = args[2] if len(args) >= 3 else None

    def generate_job_key(self):
        globals()['JOB_COUNTER'] += 1
        return slug_utils.make_key(
            f"{self.KEY_PREFIX}_{JOB_COUNTER}_{self.search_term}"
            f"_{self.title_match}_{self.publisher_match}")

    @staticmethod
    def reverse_key(key: str) -> str:
        return (key.replace(
            AmazonListingCheckerContext.KEY_PREFIX, '')
                .strip('_')
                .replace('_', ' '))


def check_amazon_products(bot: telegram.Bot, job: telegram.ext.Job):
    context: AmazonListingCheckerContext = job.context

    url = amazon.listing_generate_amazon_search_url(context.search_term)
    page = scrapper.get_page(url)
    products = amazon.listing_get_products(page)
    products = amazon.listing_filter_products(
        products, context.title_match, context.publisher_match)

    if products:
        bot.send_message(
            context.chat_id,
            f"Found {len(products)} product(s) matching title "
            f"[{context.title_match}] "
            f"and publisher [{context.publisher_match}]")
        for product_name, product_details in products.items():
            bot.send_message(
                context.chat_id,
                f"{product_name}: {product_details['link']}"
            )


def start_amazon_listing_checker(bot: telegram.Bot, update: telegram.Update,
                                 args: List, job_queue: telegram.ext.JobQueue,
                                 chat_data: Dict):
    args = telegram_utils.parse_args(args)

    context = AmazonListingCheckerContext(update.message.chat_id, *args)

    job = job_queue.run_repeating(check_amazon_products, 300,
                                  context=context)

    chat_data[context.generate_job_key()] = job

    bot.send_message(
        context.chat_id,
        f"Starting Amazon listing checker for {context.search_term}!")


def stop_amazon_listing_checker(bot: telegram.Bot, update: telegram.Update,
                                args: List, job_queue: telegram.ext.JobQueue,
                                chat_data: Dict):
    job_id = int(args[0])

    for data_key in chat_data.keys():
        if data_key.startswith(
                f'{AmazonListingCheckerContext.KEY_PREFIX}_{job_id}_'):
            job_key = data_key
            break
    else:
        job_key = None

    if job_key:
        job: telegram.ext.Job = chat_data[job_key]
        job.schedule_removal()
        del chat_data[job_key]

        bot.send_message(
            update.message.chat_id,
            f"Stopping Amazon listing checker for Job #{job_id}!")
    else:
        bot.send_message(update.message.chat_id, f"No job with ID {job_id}")


def list_amazon_listing_checker_jobs(bot: telegram.Bot,
                                     update: telegram.Update, args: List,
                                     job_queue: telegram.ext.JobQueue,
                                     chat_data: Dict):
    jobs = []
    for data_key in chat_data.keys():
        if AmazonListingCheckerContext.KEY_PREFIX in data_key:
            jobs.append(AmazonListingCheckerContext.reverse_key(data_key))

    if jobs:
        message = ("Found these jobs running:\n\n" +
                   "\n".join(jobs) +
                   "\nStop any of them with `/stop`")

        bot.send_message(update.message.chat_id, message)
    else:
        bot.send_message(update.message.chat_id, "No running jobs.")


def waddup(bot: telegram.Bot, update: telegram.Update):
    bot.send_message(update.message.chat_id, "It's datboi!")


def error_handler(bot: telegram.Bot, update: telegram.Update, error):
    print(f'Update {update} caused error {error}')


def main():
    updater = telegram.ext.Updater(TOKEN)

    dispatch = updater.dispatcher

    dispatch.add_handler(
        telegram.ext.CommandHandler(
            "start", start_amazon_listing_checker, pass_args=True,
            pass_job_queue=True,
            pass_chat_data=True))
    dispatch.add_handler(
        telegram.ext.CommandHandler(
            "stop", stop_amazon_listing_checker, pass_args=True,
            pass_job_queue=True,
            pass_chat_data=True))
    dispatch.add_handler(
        telegram.ext.CommandHandler(
            "list", list_amazon_listing_checker_jobs, pass_args=True,
            pass_job_queue=True,
            pass_chat_data=True))
    dispatch.add_handler(
        telegram.ext.CommandHandler("waddup", waddup))

    dispatch.add_error_handler(error_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    args = parser.parse_args()
    TOKEN = args.token
    main()
