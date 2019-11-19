from terraform.mapper.resource_mapper import ResourceMapper

class AWSS3Mapper(ResourceMapper):
    def __init__(self):
        super(AWSS3Mapper, self).__init__(["aws.Cloud", "aws.s3.Bucket"])
        self.attributes = {}

    def create_ci(self, tf_resource, folder, deployed):        
        if self.types_supported(tf_resource['type']):           
            self.attributes = tf_resource['attributes']            
            print("Creating CI of type 'aws.Cloud") 
            aws_id = "{0}/{1}".format(folder,"MyAWS")
            print aws_id
            aws_properties = {
                'accesskey':deployed.container.credentials['AWS_ACCESS_KEY_ID'],
                'accessSecret': deployed.container.credentials['AWS_SECRET_ACCESS_KEY']
                }

            s3_id = "{0}/{1}".format(aws_id,self.attributes['bucket_domain_name'])
            print s3_id
            s3_bucket_properties = {'bucketName':self.attributes['bucket'],'region':self.attributes['region']}    
            print s3_bucket_properties
            return [
                super(AWSS3Mapper, self)._create_ci("aws.Cloud", aws_id, aws_properties),
                super(AWSS3Mapper, self)._create_ci("aws.s3.Bucket", s3_id, s3_bucket_properties)                
            ]
        else:
            return None
    
    