# Coding challenge - Duane Bailey

## Infrastructure

The infrastructure challenge is found in the infrastructure directory.

The first thing that came to my mind is using S3 fronted by cloudfront. It's hard to beat the scale; TLS termination and redirecting from HTTP comes more or less for free; configuration is quite simple. That said, this clearly ignored the spirit of the challenge, so I came up with the next-simplest option: using nginx behind a load balancer. The load balancer can handle TLS termination, and the instance just needs to worry about a) serving the actual static file and b) redirecting from http to https. Both of these are trivially managed with nginx itself. You can find the running code at https://http-demo.duane.cc

### How to build the image

1. Install packer.
2. Authenticate with AWS by setting AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY to a IAM role with full ec2, route53, and acm access. (This was just the easiest to configure; normally I'd want to narrowly enumerate the entitlements of the user in question.)
3. Change directory to `infrastructure/packer` and run `packer build http-demo.pkr.hcl` to launch the instance and build the AMI.
4. Copy AMI to `infraustructure/terraform/config.tf` under the `aws_instance.demo-instance` resource.

### How to deploy the image

1. Install terraform.
2. Change directory to `infrastructure/terraform`.
3. Run `terraform plan -out=changes.tfplan`.
4. Assuming all goes well, run `terraform apply changes.tfplan`

### How to verify server works as expected

Run `infrastructure/verify-deploy.sh`. It should print out:

```
redirect verified
index verified
```

As to automatiing this--you'd probably want to hook this up to the deploy part of the CI/CD pipeline driving the deployment, or as close to deploy time as the deploy process allows. That seems to be a outside the concerns of this exercise, so I'll leave this to the imagination of the reader.

## Coding challenge

You can run the challenge with python 3. It expects input on stdin. The included sample input in the problem can be tried with `python credit_card_validate.py <sample_input.txt` in the coding directory.

Alternatively, you can invoke all the test samples (including the ones in `sample_input.txt`) by running:

```bash
python -c 'from coding.credit_card_validate import verify_test_samples; verify_test_samples()'
```

## Questions? Concerns?

You can reach me at the email used to commit this file.