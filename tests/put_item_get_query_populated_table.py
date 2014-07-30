import json
import random
import string
import locust
from gevent import GreenletExit
from locust.events import EventHook
from locust import task
import sys
import config as cfg

MIN_WAIT = cfg.MIN_WAIT
MAX_WAIT = cfg.MAX_WAIT
IS_FIRST_RUN = cfg.IS_FIRST_RUN

table_3_fields_no_lsi_list = []
table_3_fields_1_lsi_list = []
table_10_fields_5_lsi_list = []

key_3_fields_no_lsi_list = []
key_3_fields_1_lsi_list = []
key_10_fields_5_lsi_list = []


class UserBehavior(locust.TaskSet):

    def on_start(self):
        self.load_table_list()

    def on_stop(self):
        pass

    def run(self, *args, **kwargs):
        try:
            super(UserBehavior, self).run(args, kwargs)
        except GreenletExit:
            if hasattr(self, "on_stop"):
                self.on_stop()
            raise

    def random_name(self, length):
        return ''.join(random.choice(string.lowercase + string.digits)
                       for i in range(length))

    def load_table_list(self):
        global table_3_fields_no_lsi_list
        global table_3_fields_1_lsi_list
        global table_10_fields_5_lsi_list

        with open(cfg.TABLE_LIST) as table_list_file:
            table_list = json.load(table_list_file)
            table_3_fields_no_lsi_list = table_list['table_3_fields_no_lsi']
            table_3_fields_1_lsi_list = table_list['table_3_fields_1_lsi']
            table_10_fields_5_lsi_list = table_list['table_10_fields_5_lsi']

    @task(10)
    def put_item_3_fields_no_lsi(self):
        table_name = random.choice(table_3_fields_no_lsi_list)
        req_url = ('/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables/' + table_name + '/put_item')
        subject_key = self.random_name(20)
        post_by = self.random_name(20)
        resp = self.client.post(req_url,
                                cfg.PUT_ITEM_3_FIELDS_NO_LSI_RQ % (subject_key, post_by),
                                headers=cfg.req_headers,
                                name="put_item_3_fields_no_lsi")
        if resp.status_code == 200:
            key_3_fields_no_lsi_list.append(
                {"Subject": subject_key, "LastPostedBy": post_by})

    @task(10)
    def get_item_3_fields_no_lsi(self):
        table_name = random.choice(table_3_fields_no_lsi_list)
        req_url = ('/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables/' + table_name + '/get_item')
        if len(key_3_fields_no_lsi_list) > 0:
            attribute_key = random.choice(key_3_fields_no_lsi_list)
            subject_key = attribute_key["Subject"]
            self.client.post(req_url, cfg.GET_ITEM_3_FIELDS_NO_LSI_RQ % subject_key, headers=cfg.req_headers, name="get_item")


    @task(10)
    def put_item_3_fields_1_lsi(self):
        table_name = random.choice(table_3_fields_1_lsi_list)
        req_url = ('/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables/' + table_name + '/put_item')
        subject_key = self.random_name(20)
        post_by = self.random_name(20)

        resp = self.client.post(req_url,
                                cfg.PUT_ITEM_3_FIELDS_1_LSI_RQ % (subject_key, post_by),
                                headers=cfg.req_headers,
                                name="put_item_3_fields_1_lsi")
        if resp.status_code == 200:
            key_3_fields_1_lsi_list.append({"Subject": subject_key, "LastPostedBy": post_by})

    @task(10)
    def get_item_3_fields_1_lsi(self):
        table_name = random.choice(table_3_fields_1_lsi_list)
        req_url = ('/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables/' + table_name + '/get_item')
        if len(key_3_fields_1_lsi_list) > 0:
            attribute_key = random.choice(key_3_fields_1_lsi_list)
            subject_key = attribute_key["Subject"]
            self.client.post(req_url, cfg.GET_ITEM_3_FIELDS_1_LSI_RQ % subject_key, headers=cfg.req_headers, name="get_item")

    @task(10)
    def put_item_10_fields_5_lsi(self):
        table_name = random.choice(table_10_fields_5_lsi_list)
        req_url = ('/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables/' + table_name + '/put_item')
        subject_key = self.random_name(20)
        post_by = self.random_name(20)
        addtional_field_1 = self.random_name(20)
        addtional_field_2 = self.random_name(20)
        addtional_field_3 = self.random_name(20)
        addtional_field_4 = self.random_name(20)
        addtional_field_5 = self.random_name(20)
        addtional_field_6 = self.random_name(20)
        addtional_field_7 = self.random_name(20)

        resp = self.client.post(req_url,
                                cfg.PUT_ITEM_10_FIELDS_5_LSI_RQ % (subject_key, post_by,
                                addtional_field_1, addtional_field_2, addtional_field_3,
                                addtional_field_4, addtional_field_5, addtional_field_6,
                                addtional_field_7),
                                headers=cfg.req_headers,
                                name="put_item_10_fields_5_lsi")
        if resp.status_code == 200:
            key_10_fields_5_lsi_list.append(
                {"Subject": subject_key,
                 "LastPostedBy": post_by,
                 "AdditionalField1": addtional_field_1,
                 "AdditionalField2": addtional_field_2,
                 "AdditionalField3": addtional_field_3,
                 "AdditionalField4": addtional_field_4})

    @task(10)
    def get_item_10_fields_5_lsi(self):
        table_name = random.choice(table_10_fields_5_lsi_list)
        req_url = ('/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables/' + table_name + '/get_item')
        if len(key_10_fields_5_lsi_list) > 0:
            attribute_key = random.choice(key_10_fields_5_lsi_list)
            subject_key = attribute_key["Subject"]
            self.client.post(req_url, cfg.GET_ITEM_10_FIELDS_5_LSI_RQ % subject_key, headers=cfg.req_headers, name="get_item")

    @task(1)
    def query_3_fields_no_lsi_1(self):
        table_name = random.choice(table_3_fields_no_lsi_list)
        req_url = ('/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables/' + table_name + '/query')
        self.client.post(req_url, cfg.QUERY_3_FIELDS_NO_LSI_RQ1, headers=cfg.req_headers, name="query_hash_only")

    @task(1)
    def query_3_fields_1_lsi_1(self):
        table_name = random.choice(table_3_fields_1_lsi_list)
        req_url = ('/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables/' + table_name + '/query')
        self.client.post(req_url, cfg.QUERY_3_FIELDS_1_LSI_RQ1, headers=cfg.req_headers, name="query_hash_only")

    @task(5)
    def query_3_fields_1_lsi_2(self):
        table_name = random.choice(table_3_fields_1_lsi_list)
        req_url = ('/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables/' + table_name + '/query')
        if len(key_3_fields_1_lsi_list) > 0:
            attribute_key = random.choice(key_3_fields_1_lsi_list)
            post_by = attribute_key["LastPostedBy"]
            self.client.post(req_url, cfg.QUERY_3_FIELDS_1_LSI_RQ2 % post_by, headers=cfg.req_headers, name="query_hash_range")

    @task(1)
    def query_10_fields_5_lsi_1(self):
        table_name = random.choice(table_10_fields_5_lsi_list)
        req_url = ('/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables/' + table_name + '/query')
        self.client.post(req_url, cfg.QUERY_10_FIELDS_5_LSI_RQ1, headers=cfg.req_headers, name="query_hash_only")

    @task(5)
    def query_10_fields_5_lsi_2(self):
        table_name = random.choice(table_10_fields_5_lsi_list)
        req_url = ('/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables/' + table_name + '/query')
        if len(key_10_fields_5_lsi_list) > 0:
            attribute_key = random.choice(key_10_fields_5_lsi_list)
            post_by = attribute_key["LastPostedBy"]
            self.client.post(req_url, cfg.QUERY_10_FIELDS_5_LSI_RQ2 % post_by, headers=cfg.req_headers, name="query_hash_range")

    @task(5)
    def query_10_fields_5_lsi_3(self):
        table_name = random.choice(table_10_fields_5_lsi_list)
        req_url = ('/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables/' + table_name + '/query')
        if len(key_10_fields_5_lsi_list) > 0:
            attribute_key = random.choice(key_10_fields_5_lsi_list)
            addtional_field_1 = attribute_key["AdditionalField1"]
            self.client.post(req_url, cfg.QUERY_10_FIELDS_5_LSI_RQ3 % addtional_field_1, headers=cfg.req_headers, name="query_hash_range")

    @task(5)
    def query_10_fields_5_lsi_4(self):
        table_name = random.choice(table_10_fields_5_lsi_list)
        req_url = ('/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables/' + table_name + '/query')
        if len(key_10_fields_5_lsi_list) > 0:
            attribute_key = random.choice(key_10_fields_5_lsi_list)
            addtional_field_2 = attribute_key["AdditionalField2"]
            self.client.post(req_url, cfg.QUERY_10_FIELDS_5_LSI_RQ4 % addtional_field_2, headers=cfg.req_headers, name="query_hash_range")

    @task(5)
    def query_10_fields_5_lsi_5(self):
        table_name = random.choice(table_10_fields_5_lsi_list)
        req_url = ('/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables/' + table_name + '/query')
        if len(key_10_fields_5_lsi_list) > 0:
            attribute_key = random.choice(key_10_fields_5_lsi_list)
            addtional_field_3 = attribute_key["AdditionalField3"]
            self.client.post(req_url, cfg.QUERY_10_FIELDS_5_LSI_RQ5 % addtional_field_3, headers=cfg.req_headers, name="query_hash_range")

    @task(5)
    def query_10_fields_5_lsi_6(self):
        table_name = random.choice(table_10_fields_5_lsi_list)
        req_url = ('/v1/' +
                   cfg.PROJECT_ID +
                   '/data/tables/' + table_name + '/query')
        if len(key_10_fields_5_lsi_list) > 0:
            attribute_key = random.choice(key_10_fields_5_lsi_list)
            addtional_field_4 = attribute_key["AdditionalField4"]
            self.client.post(req_url, cfg.QUERY_10_FIELDS_5_LSI_RQ6 % addtional_field_4, headers=cfg.req_headers, name="query_hash_range")



class MagnetoDBUser(locust.HttpLocust):
    task_set = UserBehavior
    min_wait = MIN_WAIT
    max_wait = MAX_WAIT


# Master code
def on_slave_report(client_id, data):
    global IS_FIRST_RUN
    runner = locust.runners.locust_runner

    if IS_FIRST_RUN and runner.slave_count == cfg.SLAVE_COUNT:
        runner.start_hatching(cfg.LOCUST_COUNT, cfg.HATCH_RATE)
        IS_FIRST_RUN = False

    num_rq = sum([val.num_requests for val in
                  runner.request_stats.itervalues()])
    if runner.num_requests and num_rq >= runner.num_requests:
        raise KeyboardInterrupt()


locust.events.slave_report += on_slave_report

def main(host, cmd):
    if cmd == "start":
        print "Initializing ..."

    elif cmd == "end":
        print "Clean up ..."

    else:
        print "Invalid command, exiting ..."
    print ("Done.")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage: %s host_url start|end" % sys.argv[0]
        sys.exit(-1)
    main(sys.argv[1], sys.argv[2])