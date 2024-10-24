import dns.resolver

# Set the IP address of the local DNS server and a public DNS server
local_host_ip = '127.0.0.1'  # localhost
real_name_server = '8.8.8.8'  # Google's public DNS server

# Create a list of domain names to query
domainList = ['example.com.', 'safebank.com.', 'google.com.', 'nyu.edu.', 'legitsite.com.']

# Define a function to query the local DNS server for records of a given domain name
def query_local_dns_server(domain, question_type):
    try:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [local_host_ip]
        answers = resolver.resolve(domain, question_type)
        
        if question_type == 'MX':
            # For MX records, return string in format: "preference exchange"
            if len(answers) > 0:
                # Get first record's preference and exchange
                rdata = answers[0]
                return f"{rdata.preference} {rdata.exchange.to_text()}"
            return "No MX records found"
        else:
            # For A records and others
            return answers[0].to_text()
    except dns.resolver.NXDOMAIN:
        return "Domain not found"
    except dns.resolver.NoAnswer:
        return "No answer"
    except Exception as e:
        return f"Error: {str(e)}"

# Define a function to query a public DNS server for records of a given domain name
def query_dns_server(domain, question_type):
    try:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [real_name_server]
        answers = resolver.resolve(domain, question_type)
        
        if question_type == 'MX':
            # For MX records, return string in format: "preference exchange"
            if len(answers) > 0:
                # Get first record's preference and exchange
                rdata = answers[0]
                return f"{rdata.preference} {rdata.exchange.to_text()}"
            return "No MX records found"
        else:
            # For A records and others
            return answers[0].to_text()
    except dns.resolver.NXDOMAIN:
        return "Domain not found"
    except dns.resolver.NoAnswer:
        return "No answer"
    except Exception as e:
        return f"Error: {str(e)}"

# Define a function to compare the results from the local and public DNS servers
def compare_dns_servers(domainList, question_type):
    for domain_name in domainList:
        local_result = query_local_dns_server(domain_name, question_type)
        public_result = query_dns_server(domain_name, question_type)
        if local_result != public_result:
            return False
    return True    

# Define a function to print the results from querying both DNS servers
def local_external_DNS_output(question_type):    
    print("Local DNS Server")
    for domain_name in domainList:
        result = query_local_dns_server(domain_name, question_type)
        print(f"{domain_name} -> {result}")
            
    print("\nPublic DNS Server")
    for domain_name in domainList:
        result = query_dns_server(domain_name, question_type)
        print(f"{domain_name} -> {result}")

def exfiltrate_info(domain, question_type):
    data = query_local_dns_server(domain, question_type)
    return data

if __name__ == '__main__':
    question_type = 'MX'
    
    # Test specific domains from the error message
    test_domains = ['example.com.', 'nyu.edu.', 'apache.org.']
    for domain in test_domains:
        result = query_dns_server(domain, question_type)
        print(f"{domain}  resolved! {result}")
