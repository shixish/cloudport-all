import django.dispatch

job_done = django.dispatch.Signal(providing_args=["event"])
job_start = django.dispatch.Signal(providing_args=["event"])