import boto3

textractmodule = boto3.client('textract', aws_access_key_id='AKIAUN7YZP4UUMN4EPUN', aws_secret_access_key='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', region_name= "us-east-2")
#LINE/WORD
def extract_text(response, extract_by = "LINE"):
    line_text = []
    for block in response['Blocks']:
        if block['BlockType'] == extract_by:
            line_text.append(block['Text'])
    return " ".join(line_text)

#1. PLAINTEXT detection from documents:
# fileKey in form of userNAme/filename.jpg -> format string " "
def textract(fileKey):
    response = textractmodule.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': 'note-translator-data',
                'Name': fileKey
            }
        })
    return response
