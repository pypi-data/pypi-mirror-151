from typing import List, Union
import requests, json
from ddd_objects.infrastructure.ao import exception_class_dec
from ddd_objects.infrastructure.repository_impl import error_factory
from ddd_objects.domain.exception import return_codes
from .do import LogRecordDO

class LogController:
    def __init__(self, ip: str=None, port: int=None) -> None:
        if port is None:
            port = 8080
        if ip is None:
            ip = 'log-control-svc.system-service.svc.cluster.local'
        self.url = f"http://{ip}:{port}"

    def _check_error(self, status_code, info):
        if status_code>299:
            if isinstance(info['detail'], str):
                return_code = return_codes['OTHER_CODE']
                error_info = info['detail']
            else:
                return_code = info['detail']['return_code']
                error_info = info['detail']['error_info']
            raise error_factory.make(return_code)(error_info)

    @exception_class_dec(max_try=1)
    def add_record(self, record: LogRecordDO, timeout=30):
        data = json.dumps(record.to_json())
        response=requests.post(f'{self.url}/record', data=data, timeout=timeout)
        info = json.loads(response.text)
        self._check_error(response.status_code, info)
        return True

class Logger:
    def __init__(
        self, domain, location, labels=None, 
        controller_ip=None, controller_port=None
    ) -> None:
        self.domain = domain
        self.location = location
        if labels is None:
            labels = ['default']
        self.labels = labels
        self.controller = LogController(controller_ip, controller_port)

    def _send_record(
        self, 
        content, 
        record_type, 
        domain=None, 
        location=None, 
        labels=None, 
        life_time=600,
        datetime = None
    ):
        if domain is None:
            domain = self.domain
        if location is None:
            location = self.location
        if labels is None:
            labels = labels
        record = LogRecordDO(
            log_type = record_type,
            log_domain = domain,
            log_location = location,
            log_inhalt = content,
            log_label = labels,
            log_datetime = datetime,
            _life_time = life_time
        )
        self.controller.add_record(record)

    def info(
        self, 
        content, 
        domain=None, 
        location=None, 
        labels=None, 
        life_time=600,
        datetime = None
    ):
        self._send_record(content, 'info', domain, location, labels, life_time, datetime)

    def error(
        self, 
        content, 
        domain=None, 
        location=None, 
        labels=None, 
        life_time=600,
        datetime = None
    ):
        self._send_record(content, 'error', domain, location, labels, life_time, datetime)

