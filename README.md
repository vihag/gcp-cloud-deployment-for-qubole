# Cloud Deployment Manager: Qubole Deployment 

<h2>What is <a href="https://cloud.google.com/deployment-manager/">Cloud Deployment Manager</a>?</h2>
<p>
    Google Cloud Deployment Manager allows you to specify all the resources needed for your application in a declarative format using yaml. 
    You can also use Python or Jinja2 templates to parameterize the configuration and allow reuse of common deployment paradigms such as a load balanced, auto-scaled instance group. 
    Treat your configuration as code and perform repeatable deployments.
</p>

<h2>What is <a href="https://www.qubole.com/">Qubole</a>?</h2>
<p>
    Qubole is a Single platform for end-to-end big data processing
    It is the only cloud-native platform to deliver deep analytics, AI, and machine learning for your big data. 
    It provides easy-to-use end user tools such as SQL query tools, notebooks, and dashboards that leverage powerful open source engines. 
    Qubole provides a single, shared infrastructure that enables users to more efficiently conduct ETL, analytics, and AI/ML workloads 
    across best-of-breed open source engines including Apache Spark, TensorFlow, Presto, Airflow, Hadoop, Hive, and more.
</p>

<h2>What is the purpose of this project?</h2>
<p>
    When an organization or a customer wants to use Qubole on GCP, they need to integrate their GCP Project with Qubole. This includes
    
    * IAM permissions
        * Compute
        * Storage
        * Big Query
    * Dedicated networking components
        * VPC Network
        * Subnetworks
        * Firewall Rules
        * NAT Gateways
    * Hive Metastore
    
    That said, The purpose of this project is two-fold
    1. Create IAM Roles, Service Accounts and Policies that 
        i. Allow Qubole to Create Clusters and perform complete life cycle management
        ii. Allow the clusters to write audit data, command logs/results/resources onto Google Cloud Storage
        iii. Allow the clusters to read data from Big Query
    2. Create infrastructure dedicated for use by Qubole(hence isolating it from other resources)
        i. A dedicated VPC network with a public and private subnet
        ii. A bastion host for securing communications with Qubole
        iii. A NAT Gateway to secure outbound communications in the private subnet
        iv. Associated firewall rules to secure inter-component communications
        
    Additionally, the project also contains templates to spin up a Hive Metastore if the customer or organization does not already have one.
    The templates will do the following
    1. Create a Cloud SQL Instance (MySQL Gen 2) with a database configured as the Hive Metastore
    2. Create a GCE VM and run Cloud SQL Proxy on it, creating a proxy connection to the Cloud SQL instance
    3. Additionally, the templates will whitelist the private subnet and bastion host to be able to access the Cloud SQL Proxy
</p>       
        
