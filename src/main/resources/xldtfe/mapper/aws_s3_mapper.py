#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from terraform.mapper.resource_mapper import ResourceMapper

class AWSS3Mapper(ResourceMapper):
    def __init__(self):
        super(AWSS3Mapper, self).__init__(["aws.Cloud", "aws.s3.Bucket"])
        self.attributes = {}

    def accepted_type(self):
        return 'aws_s3_bucket'

    def create_ci(self, tf_resource, folder, deployed):
        if not self.types_supported(tf_resource['type']):
            return None
        self.attributes = tf_resource['attributes']
        print("Creating CI of type 'aws.Cloud")
        aws_id = "{0}/{1}".format(folder,"MyAWS")
        print(aws_id)
        if deployed.container.type == 'terraformEnterprise.AwsProvider':
            aws_properties = {
                'accesskey':deployed.container.accesskey,
                'accessSecret': deployed.container.accessSecret
                }
        else:
            aws_properties = {
                'accesskey':deployed.container.credentials['AWS_ACCESS_KEY_ID'],
                'accessSecret': deployed.container.credentials['AWS_SECRET_ACCESS_KEY']
                }

        s3_id = "{0}/{1}".format(aws_id,self.attributes['bucket_domain_name'])
        #print s3_id
        s3_bucket_properties = {'bucketName':self.attributes['bucket'],'region':self.attributes['region']}
        #print s3_bucket_properties
        return [
            super(AWSS3Mapper, self)._create_ci("aws.Cloud", aws_id, aws_properties),
            super(AWSS3Mapper, self)._create_ci("aws.s3.Bucket", s3_id, s3_bucket_properties)                
        ]
        
    
    
