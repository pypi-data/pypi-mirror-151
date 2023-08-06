import json
import threading
from collections import defaultdict

import requests
import client
import random

from random import sample
from datetime import datetime
from users import User

API_KEY = 'a9f7060efb0e8d8dbc6d03d772c0aa86dec99aef'

def worker(task):
    c = client.Client(url='https://develop.dev.heartex.com/', api_key='2a82e39f447fba3362ac836a54b3c52c0a2cf1cc')
    p = c.get_project(490)
    print(f"Starting import {task}")
    data = json.load(open(r"C:\Users\Pagocmb\Downloads\100images-with-preds.json"))
    p.import_tasks(data)
    print(f"End of import {task}")


def main():
    for task in range(5):
        t = threading.Thread(target=worker, args=(task,))
        t.start()


def load_and_save(filename=r"C:\Users\Pagocmb\Downloads\project-19-at-2022-01-04-16-11-60e46bbf.json"):
    with open(filename, mode='r') as f:
        data = json.load(f)

    for each in data:
        url = each['data'][list(each['data'].keys())[0]]
        r = requests.get(url)
        each['data'][list(each['data'].keys())[0]] = r.text

    with open(filename + ".json", mode='w') as f:
        json.dump(data, f)


def test_export_with_files():
    c = client.Client(url='http://127.0.0.1:8080/', api_key='a9f7060efb0e8d8dbc6d03d772c0aa86dec99aef')
    p = c.get_project(32)
    t = p.export_tasks_with_download(export_type="CONLL2003")

USERS = defaultdict(int)
def assign(users, tasks_ids):
    print(f"{users} {tasks_ids}")
    USERS[users[0].id] += len(tasks_ids)


def test_assigning():
    c = client.Client(url='http://127.0.0.1:8000/', api_key='a9f7060efb0e8d8dbc6d03d772c0aa86dec99aef')
    p = c.get_project(32)
    u = c.get_users()
    u = [us for us in u if us.id in [1, 2]]
    p.assign_annotators_by_sampling(users=u)


def test_export():
    c = client.Client(url='https://develop.dev.heartex.com/', api_key='2a82e39f447fba3362ac836a54b3c52c0a2cf1cc')
    p = c.get_project(553)
    print(p.exports())
    print(p.create_export(title=122, task_filter_options={}, interpolate_key_frames=True))
    print(p.download_export_snapshot(153))


def test_assigning_view():
    c = client.Client(url="https://develop.dev.heartex.com/", api_key='2a82e39f447fba3362ac836a54b3c52c0a2cf1cc')
    p = c.get_project(578)
    u = p.get_members()
    u = [us.id for us in u]
    print(p.assign_annotators_by_sampling(users=u, overlap=1))


def test_uploaded_files():
    api_key = 'a9f7060efb0e8d8dbc6d03d772c0aa86dec99aef'
    c = client.Client(url="http://127.0.0.1:8080/", api_key=api_key)
    p = c.get_project(40)
    p.get_files_from_tasks({}, get_tasks=True)


def test_create_prediction():
    api_key = "a9f7060efb0e8d8dbc6d03d772c0aa86dec99aef"
    c = client.Client(url="http://127.0.0.1:8080/", api_key=api_key)
    p = c.get_project(43)
    result = [
        {
          "type": "labels",
          "value": {'end': '/div[1]/div[1]',
                    'text': 'Chinese',
                    'start': '/div[0]/div[0]',
                    'endOffset': 17,
                    'startOffset': 10,
                    'htmllabels': ['served_region']
                    },
          "origin": "manual",
          "to_name": "text",
          "from_name": "label"
        },
        {
            "type": "labels",
            "value": {'end': '/div[1]/div[1]',
                      'text': 'Chinese',
                      'start': '/div[0]/div[0]',
                      'endOffset': 17,
                      'startOffset': 10,
                      'htmllabels': ['served_region']
                      },
            "origin": "manual",
            "to_name": "text",
            "from_name": "label"
        }
      ]
    p.create_prediction(task_id=489211, result=result, score=0.33)


def test_DEV_1503():
    api_key = "c418b9993c5b4df5c72ad2b3ddfce09b8e7beb50"
    c = client.Client(url="https://develop.dev.heartex.com//", api_key=api_key)
    p = c.get_project(498)
    t = p.get_tasks(only_ids=True, selected_ids=[455021, 455022, 455023])
    print(t)


def test_DEV_1740():
    api_key = '79c174be8764046ff82f4f19ec7e85bfc596f7df'
    c = client.Client(url="https://dev-1740-fix.dev.heartex.com/", api_key=api_key)
    p = c.get_project(15)
    tasks = p.get_tasks(only_ids=True)
    tasks = sample(tasks, 50)
    start_date = int(datetime.now().timestamp())
    for id in tasks:
        p.get_task(task_id=id)
    end_date = int(datetime.now().timestamp())
    return end_date-start_date


def dev_test_DEV_1740():
    api_key = 'c418b9993c5b4df5c72ad2b3ddfce09b8e7beb50'
    c = client.Client(url="https://develop.dev.heartex.com/", api_key=api_key)
    p = c.get_project(531)
    tasks = p.get_tasks(only_ids=True)
    tasks = sample(tasks, 20)
    start_date = int(datetime.now().timestamp())
    for id in tasks:
        p.get_task(task_id=id)
    end_date = int(datetime.now().timestamp())
    return end_date-start_date


def stage_test_DEV_1740():
    api_key = 'deb1aa60589acb32abd354713b3b93847b3e52b6'
    c = client.Client(url="https://stage-21.heartex.ai/", api_key=api_key)
    p = c.get_project(20)
    tasks = p.get_tasks(only_ids=True)
    tasks = sample(tasks, 20)
    start_date = int(datetime.now().timestamp())
    for id in tasks:
        p.get_task(task_id=id)
    end_date = int(datetime.now().timestamp())
    return end_date-start_date


def test_labels_api():
    api_key = 'a9f7060efb0e8d8dbc6d03d772c0aa86dec99aef'
    c = client.Client(url="http://localhost:8000/", api_key=api_key)
    p = c.get_project(54)

    # list current labels from project
    labels = p.get_labels()
    print(labels)
    # create new label
    for i in range(9, 10):
        data = {"title": f'NewLabel_{i}',
                "value": [f'NewLabel_{i} for Taxonomy'],
                "approved": True,
                "from_name": f"Test_{i}",
                "project": 54}
        label_new = p.create_labels([data])

    # list current labels from project
    labels = p.get_labels()
    # grab labels to be merged
    label_1, label_2 = labels[0], labels[1]
    # rename labels
    p.bulk_update_labels(label_2.id, label_new[0]['id'])

    # remove old labels
    label_1.delete()
    label_2.delete()
    # list current labels from project
    labels = p.get_labels()
    print(labels)


def parallel_import(target=None, num=100, para=True):
    for task in range(num):
        if para:
            t = threading.Thread(target=target, args=(task,))
            t.start()
        else:
            target(task)


def check_assignement():
    c = client.Client(url='http://127.0.0.1:8000/', api_key='a9f7060efb0e8d8dbc6d03d772c0aa86dec99aef')
    p = c.get_project(21)
    users = p.get_members()
    task_ids = p.get_tasks(only_ids=True)
    p.assign_annotators(users=users, tasks_ids=task_ids)


def test_DEV_():
    import random
    foo = [21]
    api_key = 'a9f7060efb0e8d8dbc6d03d772c0aa86dec99aef'
    c = client.Client(url="http://127.0.0.1:8080/", api_key=api_key)
    start_date = float(datetime.now().timestamp())
    p = c.get_project(random.choice(foo))
    t = p.get_paginated_tasks(filters={
        "conjunction": "and",
        "items": [
            {
                "filter": "filter:tasks:total_annotations",
                "operator": "greater",
                "value": 2,
                "type": "Number"
            }
        ]
    }, page=random.randint(1, 30), page_size=30)
    end_date = float(datetime.now().timestamp())
    return end_date-start_date


def test_workspace_project():
    api_key = 'a9f7060efb0e8d8dbc6d03d772c0aa86dec99aef'
    c = client.Client(url="http://127.0.0.1:8000/", api_key=api_key)
    #p = c.get_project(21)
    workspaces = c.get_workspaces()
    for w in workspaces:
        p = w.get_projects()
        tasks = p[0].get_tasks(only_ids=True)
        print(tasks)


def test_DEV_1992():
    foo = [21]
    api_key = 'a9f7060efb0e8d8dbc6d03d772c0aa86dec99aef'
    c = client.Client(url="http://127.0.0.1:8000/", api_key=api_key)
    start_date = float(datetime.now().timestamp())
    p = c.get_project(random.choice(foo))
    end_date = float(datetime.now().timestamp())
    return end_date-start_date


def get_median(n):
    s = 0
    for i in range(n):
        s += test_DEV_1992()
    return s / n


def test_DEV_2083():
    api_key = 'a9f7060efb0e8d8dbc6d03d772c0aa86dec99aef'
    c = client.Client(url="http://127.0.0.1:8000/", api_key=api_key)
    p = c.get_project(80)
    p.set_params(control_weights={"Test": 1})


def worker_create_annotations(task):
    c = client.Client(url='http://127.0.0.1:8080/', api_key=API_KEY)
    p = c.get_project(88)
    print(f"Starting import {task}")
    p.create_annotation(task_id=494633, data={
        "lead_time": 7.669,
        "result": [
            {
                "value": {
                    "choices": [
                        "Negative"
                    ]
                },
                "id": "pMvMbhKVaA",
                "from_name": "sentiment",
                "to_name": "text",
                "type": "choices",
                "origin": "manual"
            }
        ],
        "draft_id": 0,
        "parent_prediction": None,
        "parent_annotation": None,
        "project": "88"
    })
    print(f"End of import {task}")


def worker_import(task):
    c = client.Client(url='http://dev-2075.dev.heartex.com/', api_key='34f21fd2038773e542e644295127dea3fc398ee9')
    p = c.get_project(18)
    print(f"Starting import {task}")
    data = json.load(open(r"C:\projects\Heartex\TestData\exports\export_91.json"))
    p.import_tasks(data)
    print(f"End of import {task}")


def worker_dashboard(task):
    c = client.Client(url='http://127.0.0.1:8000/', api_key='a9f7060efb0e8d8dbc6d03d772c0aa86dec99aef')
    foo = [21, 8, 84, 85, 47, 46, 7, 9, 91]
    p = c.get_project(random.choice(foo))
    print(f"Starting getting dashboard {task} and {p.id}")
    p.get_dashboard()
    print(f"End of import {task}")


def test_assigning():
    c = client.Client(url='http://127.0.0.1:8000/', api_key='a9f7060efb0e8d8dbc6d03d772c0aa86dec99aef')
    p = c.get_project(114)
    u = c.get_users()
    #u = [us for us in u if us.id in [1, 2]]
    u = u[:8]
    from project import AssignmentSamplingMethod
    return p._assign_by_sampling(users=u,
                                    assign_function=assign,
                                    view_id=None,
                                    method=AssignmentSamplingMethod.RANDOM,
                                    fraction=0.995,
                                    overlap=1)

test_assigning()
print(USERS)
