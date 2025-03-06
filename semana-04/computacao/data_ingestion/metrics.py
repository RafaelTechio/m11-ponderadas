from prometheus_client import start_http_server, Counter, Histogram
import time


class MetricsPrometheus:

    def __init__(self):
        self.REQUEST_COUNT = Counter("app_requests_total", "Total de requisições")
        self.supabase_storage_accesses = Counter('supabase_storage_access_total', 'Número total de acessos ao Supabase Storage')
        self.request_duration = Histogram('supabase_storage_request_duration_seconds', 'Duração das requisições ao Supabase Storage')

    def star_server(self):
        start_http_server(8000)
