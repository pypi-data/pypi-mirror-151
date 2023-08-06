import click
from code_size_analyzer_client.client_wrapper import ClientWrapper
import json
from otel_extensions import init_telemetry_provider, TelemetryOptions, flush_telemetry_data


@click.command()
@click.option("--map_file", required=True, help="path to map file")
@click.option(
    "--stack_name", required=True, help="stack owner name (i.e. zigbee, matter)"
)
@click.option("--target_part", required=True, help="target part")
@click.option("--compiler", required=True, help="compiler name (gcc or iar)")
@click.option("--project_file", default=None, help="path to project file")
@click.option(
    "--service_url",
    default="https://code-size-analyzer.dev.silabs.net",
    help="service endpoint",
)
@click.option("--output_file", default=None, help="path to output json file (default is to stdout)")
@click.option("--verify_ssl", default=True, help="verify ssl certificate on server")
def main(map_file, stack_name, target_part, compiler, project_file, service_url, output_file, verify_ssl):
    init_telemetry_provider(TelemetryOptions(
        OTEL_SERVICE_NAME="Code Size Analyzer CLI",
    ))
    client_wrapper = ClientWrapper(server_url=service_url, verify_ssl=verify_ssl)
    r = client_wrapper.analyze_map_file(
        map_file, stack_name, target_part, compiler, project_file
    )
    j = json.dumps(r.to_dict(), indent=2)
    if output_file is not None:
        with open(output_file, "w") as f:
            f.write(j)
    else:
        print(j)
    flush_telemetry_data()

if __name__ == '__main__':
    main()