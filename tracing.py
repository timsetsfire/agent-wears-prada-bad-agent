from phoenix.otel import register
from openinference.instrumentation.langchain import LangChainInstrumentor
import os
from opentelemetry import trace
import datarobot as dr 
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

client = dr.Client()
def _otlp_traces_endpoint(client_domain: str) -> str:
    """Resolve OTLP/HTTP trace URL for DataRobot (collector lives under /otel, not site root)."""
    if explicit := os.environ.get("OTEL_EXPORTER_OTLP_TRACES_ENDPOINT"):
        return explicit
    base = (os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT") or "").rstrip("/")
    if base:
        return base if base.endswith("/v1/traces") else f"{base}/v1/traces"
    return f"{client_domain.rstrip('/')}/otel/v1/traces"



def _parse_otlp_headers(raw: str | None) -> dict[str, str]:
    if not raw:
        return {}
    out: dict[str, str] = {}
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        name, sep, value = part.partition("=")
        if sep:
            out[name.strip()] = value.strip()
    return out

class Tracing(object):
    def __init__(self, project_name: str):    


        api_key = os.environ["DATAROBOT_API_TOKEN"]

        try:
            print("configuring tracing and metrics")
    
            # traces_endpoint = os.environ["OTEL_EXPORTED_OTLP_TRACES_ENDPOINT"]
            # traces_endpoint = _otlp_traces_endpoint(client.domain)
            traces_endpoint = "https://app.datarobot.com/otel/v1/traces"
            # otel_exporter_otlp_headers = dict([header.split("=") for header in os.environ["OTEL_EXPORTER_OTLP_HEADERS"].split(",")])
            # headers = {"Authorization": f"Bearer {api_key}", **otel_exporter_otlp_headers}
            headers = {
                "Authorization": f'Bearer {os.environ["DATAROBOT_MTS_API_TOKEN"]}',
                "X-DataRobot-Entity-Id": "deployment-6a0716bf12c55b0ff377422b",
                "X-DataRobot-Api_key": os.environ["DATAROBOT_MTS_API_TOKEN"],
            }
            
            # Set up tracing (your existing code)
            tracer_provider = register(
                project_name=project_name,
                set_global_tracer_provider=False,
                endpoint=traces_endpoint,
                headers=headers,
                auto_instrument=True
            )

            # tracer_provider.add_span_processor(BatchSpanProcessor(
            #     OTLPSpanExporter(
            #         endpoint="https://app.datarobot.com/otel/v1/traces",
            #         headers={
            #             "Authorization": f'Bearer {os.environ["DATAROBOT_MTS_API_TOKEN"]}',
            #             "X-DataRobot-Entity-Id": "deployment-6a0716bf12c55b0ff377422b",
            #             "X-DataRobot-Api_key": os.environ["DATAROBOT_MTS_API_TOKEN"],
            #         },
            #     )
            # ))

            trace.set_tracer_provider(tracer_provider)
            LangChainInstrumentor().instrument(tracer_provider=tracer_provider)

            print("tracing configured")
            tracing_configured = True
        except Exception as e:
            try:
                print("error:")
                print(e)
                print("====")
                print("likely running locally.  setting up tracing to land in phoenix app running on datarobot")
                api_key = os.environ["DATAROBOT_MTS_API_TOKEN"]
                tracer_provider = register(
                    # project_name=project_name,
                    set_global_tracer_provider=False,    
                    endpoint="https://app.datarobot.com/custom_applications/68811c3f85fa13cc3052cdfc/v1/traces",
                    headers = {"Authorization": f"Bearer {api_key}"},                
                    protocol="http/protobuf",
                    auto_instrument=True                    
                )
                trace.set_tracer_provider(tracer_provider)
                LangChainInstrumentor().instrument(tracer_provider=tracer_provider)
                print("tracing configured")
                tracing_configured = True
            except Exception as e:
                print(e)
                print("tracing is not available")  
                error = str(e)
                tracing_configured = False

# session_tracing = Tracing()