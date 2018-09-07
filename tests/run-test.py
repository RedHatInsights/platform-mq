#!/usr/bin/env python

import json
import sh
import sys
import time
import argparse


def oc(*args, **kwargs):
    return sh.oc(*args, **kwargs)


def run_test(config, args):
    for k, v in ((k, getattr(config, k)) for k in vars(config)):
        if getattr(config, k) and k not in ("namespace", "silent", "rate"):
            args.extend(["-p", "%s=%s" % (k, v)])

    if config.namespace:
        args.extend(["-n", config.namespace])

    rendered_template = oc(*args)
    print(oc(rendered_template, "create", "-f", "-"))


def delete_jobs(job_names):
    print("Deleting jobs...")
    for job_name in job_names:
        oc("delete", "job", job_name)
    print("Jobs deleted")


def report_back(pod_name, config, job_names):
    if config.silent:
        print("Pod %s created" % pod_name)
    else:
        try:
            print("Press ^C to stop tailing log and delete jobs")
            print("Waiting for message queue test to start...")
            while True:
                try:
                    oc("logs", "-f", pod_name, _out=sys.stdout)
                except sh.ErrorReturnCode_1:
                    time.sleep(1)
                else:
                    break
        except KeyboardInterrupt:
            delete_jobs(job_names)
            sys.exit()


def get_pod(pattern, job_names):
    pod_name = None
    while pod_name is None:
        time.sleep(0.1)
        pods = json.loads(str(oc("get", "pod", "-o", "json")))
        for pod in pods["items"]:
            job_name = pod["metadata"]["labels"].get("job-name")
            if job_name in job_names:
                pod_name = pod["metadata"]["name"]
                if pod_name.startswith(pattern):
                    return pod_name


def main():
    parser = argparse.ArgumentParser(description="MQ functionality tester")
    parser.add_argument("--count", type=int, default=100)
    parser.add_argument("--rate", type=int, default=100)
    parser.add_argument("--servers", required=True)
    parser.add_argument("-n", "--namespace")
    parser.add_argument("-s", "--silent", action="store_true", default=False)
    config = parser.parse_args()

    job_names = ["producer-test-job", "consumer-test-job"]

    args = ["process", "producer-test-template", "-p", "rate=%s" % config.rate]
    run_test(config, args)

    pod_name = get_pod("producer-test", job_names)
    report_back(pod_name, config, job_names)  # Producer run

    args = ["process", "consumer-test-template"]
    run_test(config, args)

    pod_name = get_pod("consumer-test", job_names)
    report_back(pod_name, config, job_names)  # Consumer run

    delete_jobs(job_names)


if __name__ == "__main__":
    main()
