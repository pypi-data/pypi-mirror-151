# Requirements
   - terraform v1.1.4+
   - ansible 2.10.7+
   - python3  3.8.5+

# Purpose

Provisions an instance on using terraform and calls ansible playbooks specified in 
the yaml config file. See `config.yaml.sample`, the `aws` directory for sample terraform 
script and `stage.yaml` for sample ansible playbook. 

```
python3 -m pip install . 
cp ./config.yaml.sample config.yaml   # Modify as needed ssh keys, ...

# Usage
go-deploy -h

# Dry run
go-deploy -init -c config.yml -w workspace -d aws -dry-run -verbose

# Deploy 
go-deploy -init -c config.yml -w workspace -d aws -verbose

# Tear Dow
terraform -chdir=aws destroy    # Enter yes when prompted.
```
