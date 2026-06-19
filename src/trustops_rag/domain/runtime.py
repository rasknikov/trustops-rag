from dataclasses import dataclass

@dataclass
class RuntimeConfig:
    environment: str
    api_enabled: bool
    worker_enabled: bool
    observability_enabled: bool
    version: str

@dataclass
class RuntimeStatus:
    mode: str
    services_ready: bool
    system_state: str
    runtime_label: str

def validate_runtime_config(runtime_config: RuntimeConfig) -> None:
    if not runtime_config.environment.strip():
        raise ValueError("Environment cannot be empty.")
    
    if not runtime_config.version.strip():
        raise ValueError("Version cannot be empty.")
    
    if runtime_config.worker_enabled and not runtime_config.api_enabled:
        raise ValueError("Worker cannot be enabled when API is disabled.")
    
def determine_runtime_mode(runtime_config: RuntimeConfig) -> str:
    if runtime_config.api_enabled and runtime_config.worker_enabled and runtime_config.observability_enabled:
        return "full"
    return "partial"
    
def determine_services_ready(runtime_config: RuntimeConfig) -> bool:
    if runtime_config.api_enabled and runtime_config.worker_enabled and runtime_config.observability_enabled:
        return True
    elif runtime_config.api_enabled and runtime_config.worker_enabled:
        return True
    return False


def evaluate_runtime(runtime_config: RuntimeConfig) -> RuntimeStatus:
    validate_runtime_config(runtime_config)

    mode = determine_runtime_mode(runtime_config)
    services_ready = determine_services_ready(runtime_config)

    if mode == "full" and services_ready:
        system_state="normal"
    else:
        system_state="degraded"

    runtime_label=f"{runtime_config.environment}:{runtime_config.version}:{mode}"
        
    return RuntimeStatus(
        mode=mode,
        services_ready=services_ready,
        system_state=system_state,
        runtime_label=runtime_label
    )