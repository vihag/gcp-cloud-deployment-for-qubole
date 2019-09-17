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
    
    That said, The purpose of this project is two-fold,
    Using the DRY principle promoted by GCP Cloud Deployment Manager, create re-usable, customizable modules that
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

<h2>How does the integration look like?</h2>
<p>
    <img src="./readme_files/qubole_gcp_integration.png" title="Qubole GCP Integration Reference Architecture">
</p>

<h2>How to use the project?</h2>
<p>
    All the templates are python templates in the py_templates folder. Each template has detailed documentation on its purpose in life and its use to the Qubole deployment
    The deployment configurations are in the configurations folder.
</p>

        There are 3 modules
        1. The account_integration module
            i. Setup a custom compute role with minimum compute permissions
            ii. Setup a custom storage role with minimum storage permissions
            iii. Setup a service account that will act as the Compute Service Account
            iv. Setup a service account that will act as the Instance Service Account
            v. Authorize the Qubole Service Account to be able to use the Compute Service Account
            vi. Authorize the Compute Service Account to be able to use the Instance Service Account
            vii. Authorize the Service Accounts to be able to read Big Query Datasets
            viii. Create a Cloud Storage Bucket which will be the account's Default Location
        2. The network_infrastructure module
            i. Setup a VPC Network with a public and private subnet
            ii. Setup a Bastion host in the public subnet and whitelist Qubole ingress to it
            iii. Setup a Cloud NAT to allow clusters spun up in the private subnet access to the internet
        3. The hive_metastore module
            i. Setup a Cloud SQL Instance hosting the Hive Metastore, exposed via a Cloud SQL Proxy Service
            ii. Peer the Cloud SQL Proxy VPC to the Qubole Dedicated VPC for secure access
            iii. Whitelist Bastion ingress and private subnet ingress to the Cloud SQL Proxy Service
            iv. Setup Private IP connection between the SQL proxy and the Cloud SQL instance for maximum security and performance
    
    
        Deploy the modules as follows
        1. Navigate to the qubole-deployment folder
        2. Navigate to the account_integration folder
            2.1 Edit the yaml file to change any variables you wish
            2.2 Run 'sudo gcloud --verbosity=warning deployment-manager deployments create deployment-qubole-account-integration --config account_integration.yaml'
        3. Navigate to the network_infrastructure folder
            3.1 Edit the yaml file to change any variables you wish
            3.2 Run 'sudo gcloud --verbosity=warning deployment-manager deployments create deployment-qubole-network-integration --config network_integration.yaml'
        4. Navigate to the hive_metastore folder
            4.1 Edit the yaml file to change any variables you wish. Some of the variables will depend on the output of Step 3
            4.2 Run 'sudo gcloud --verbosity=warning deployment-manager deployments create deployment-qubole-hive-metastore-integration --config hive_metastore_integration.yaml'

<p>That's all folks</p>