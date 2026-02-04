import math

def mmc_queue_simulation(arrival_rate, service_rate, servers):
    """
    M/M/c queue model simulation using Erlang C formula
    arrival_rate (λ): Average number of patients arriving per hour
    service_rate (μ): Average number of patients one server can handle per hour
    servers (c): Number of servers/doctors available
    
    Returns:
        Dictionary with queue performance metrics
    """
    
    if servers <= 0 or service_rate <= 0:
        return {
            'utilization': 0,
            'avg_wait_time': 0,
            'avg_queue_length': 0,
            'avg_patients_in_system': 0,
            'avg_time_in_system': 0
        }
    
    utilization = arrival_rate / (servers * service_rate)
    
    if utilization >= 1:
        return {
            'utilization': round(utilization, 3),
            'avg_wait_time': float('inf'),
            'avg_queue_length': float('inf'),
            'avg_patients_in_system': float('inf'),
            'avg_time_in_system': float('inf')
        }
    
    traffic_intensity = arrival_rate / service_rate
    
    sum_terms = sum(
        (traffic_intensity ** k) / math.factorial(k)
        for k in range(servers)
    )
    
    last_term = (traffic_intensity ** servers) / (
        math.factorial(servers) * (1 - utilization)
    )
    
    p0 = 1 / (sum_terms + last_term)
    
    erlang_c = (
        (traffic_intensity ** servers) / math.factorial(servers)
    ) * (servers * service_rate / (servers * service_rate - arrival_rate)) * p0
    
    avg_wait = erlang_c / (servers * service_rate - arrival_rate)
    avg_queue = arrival_rate * avg_wait
    
    avg_time_in_system = avg_wait + (1 / service_rate)
    avg_patients_in_system = avg_queue + traffic_intensity
    
    return {
        'utilization': round(utilization, 3),
        'avg_wait_time': round(avg_wait, 2),
        'avg_queue_length': round(avg_queue, 2),
        'avg_patients_in_system': round(avg_patients_in_system, 2),
        'avg_time_in_system': round(avg_time_in_system, 2),
        'erlang_c': round(erlang_c, 3)
    }

def calculate_probability_no_wait(arrival_rate, service_rate, servers):
    """
    Calculate probability that a patient doesn't have to wait (using Erlang C)
    """
    if servers <= 0 or service_rate <= 0:
        return 0
        
    utilization = arrival_rate / (servers * service_rate)
    
    if utilization >= 1:
        return 0
    
    traffic_intensity = arrival_rate / service_rate
    
    sum_terms = sum(
        (traffic_intensity ** k) / math.factorial(k)
        for k in range(servers)
    )
    
    last_term = (traffic_intensity ** servers) / (
        math.factorial(servers) * (1 - utilization)
    )
    
    p0 = 1 / (sum_terms + last_term)
    
    erlang_c = (
        (traffic_intensity ** servers) / math.factorial(servers)
    ) * (servers * service_rate / (servers * service_rate - arrival_rate)) * p0
    
    return round(1 - erlang_c, 3)