from codeable_models import CClass, CBundle, add_links, CStereotype, CMetaclass, CEnum, CAttribute 
from metamodels.microservice_dfds_metamodel import * 
from plant_uml_renderer import PlantUMLGenerator 
plantuml_path = "../../plantuml.jar" 
output_directory = "." 
model_name = "spring-netflix-oss-microservices"
card_service = CClass(service, "card-service", stereotype_instances = [internal], tagged_values = {'Endpoints': "['/api/new-card', '/api/cards', '/api/card/{cardId}', '/api']", 'Port': 8080})
card_statement_composite = CClass(service, "card-statement-composite", stereotype_instances = [internal, circuit_breaker], tagged_values = {'Endpoints': "['/new-card', '/card/{cardId}', '/cards', '/statement/{statementId}', '/api/statement-by-card', '/api', '/statement', '/statements']", 'Port': 8080})
config_server = CClass(service, "config-server", stereotype_instances = [infrastructural, configuration_server], tagged_values = {'Port': 9090, 'Configuration Server': 'Spring Cloud Config'})
discovery_service = CClass(service, "discovery-service", stereotype_instances = [service_discovery, infrastructural], tagged_values = {'Service Discovery': 'Eureka', 'Port': 8761})
edge_server = CClass(service, "edge-server", stereotype_instances = [gateway, infrastructural, load_balancer], tagged_values = {'Port': 8765, 'Load Balancer': 'Ribbon', 'Gateway': 'Zuul'})
monitor_dashboard = CClass(service, "monitor-dashboard", stereotype_instances = [infrastructural, monitoring_dashboard], tagged_values = {'Port': 8179, 'Monitoring Dashboard': 'Hystrix', 'Endpoints': "['/']"})
statement_service = CClass(service, "statement-service", stereotype_instances = [internal], tagged_values = {'Endpoints': "['/api/statement/{statementId}', '/api/statements', '/api/statement', '/api']", 'Port': 8080})
turbine = CClass(service, "turbine", stereotype_instances = [infrastructural, monitoring_server], tagged_values = {'Port': 8989, 'Monitoring Server': 'Turbine'})
rabbitmq = CClass(service, "rabbitmq", stereotype_instances = [infrastructural, message_broker], tagged_values = {'Port': 5672, 'Message Broker': 'RabbitMQ'})
github_repository = CClass(external_component, "github-repository", stereotype_instances = [github_repository, entrypoint], tagged_values = {'URL': 'https://github.com/fernandoabcampos/microservices-config.git'})
user = CClass(external_component, "user", stereotype_instances = [user_stereotype, exitpoint, entrypoint])
add_links({github_repository: config_server}, stereotype_instances = [restful_http])
add_links({config_server: card_service}, stereotype_instances = [restful_http])
add_links({config_server: card_statement_composite}, stereotype_instances = [restful_http])
add_links({config_server: discovery_service}, stereotype_instances = [restful_http])
add_links({config_server: edge_server}, stereotype_instances = [restful_http])
add_links({config_server: monitor_dashboard}, stereotype_instances = [restful_http])
add_links({config_server: statement_service}, stereotype_instances = [restful_http])
add_links({config_server: turbine}, stereotype_instances = [restful_http])
add_links({statement_service: card_service}, stereotype_instances = [restful_http])
add_links({monitor: rabbitmq}, stereotype_instances = [restful_http])
add_links({turbine: rabbitmq}, stereotype_instances = [restful_http])
add_links({card_statement_composite: discovery_service}, stereotype_instances = [restful_http, circuit_breaker_link])
add_links({statement_service: discovery_service}, stereotype_instances = [restful_http])
add_links({card_service: discovery_service}, stereotype_instances = [restful_http])
add_links({turbine: discovery_service}, stereotype_instances = [restful_http])
add_links({monitor_dashboard: discovery_service}, stereotype_instances = [restful_http])
add_links({discovery_service: edge_server}, stereotype_instances = [restful_http])
add_links({user: edge_server}, stereotype_instances = [restful_http])
add_links({edge_server: user}, stereotype_instances = [restful_http])
add_links({edge_server: card_statement_composite}, stereotype_instances = [restful_http])
add_links({edge_server: statement_service}, stereotype_instances = [restful_http])
add_links({edge_server: card_service}, stereotype_instances = [restful_http])
add_links({turbine: monitor_dashboard}, stereotype_instances = [restful_http])
add_links({rabbitmq: turbine}, stereotype_instances = [restful_http])
model = CBundle(model_name, elements = rabbitmq.class_object.get_connected_elements())
def run():
    generator = PlantUMLGenerator()
    generator.plant_uml_jar_path = plantuml_path
    generator.directory = output_directory
    generator.object_model_renderer.left_to_right = True
    generator.generate_object_models(model_name, [model, {}])
    print(f"Generated models in {generator.directory!s}/" + model_name)
if __name__ == "__main__":
    run()