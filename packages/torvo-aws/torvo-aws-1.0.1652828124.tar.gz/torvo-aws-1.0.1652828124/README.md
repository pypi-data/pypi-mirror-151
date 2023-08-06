
# Torvo AWS

An AWS module that provides simplified infrastructure as code.

* All resources should have predictable identifiers, this removes the need for additional state storage and maintenance.
* Actions should be primarily idempotent, this simplifies the amount of code required to manage the infrastructure.
* All functions relating to a resource use the same interface and only access the properties as needed, this minimises the complexity of managing properties.

## Usage

**Install**

```
pip install torvo-aws
```


**Import**

```
import aws
```

**Use**

```
aws.session.create()
```

**Notes**

* We only provide the latest version, don't pin to any specific version.
* For any missing details refer to [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
