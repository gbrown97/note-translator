import boto3
#from trp import Document

textractmodule = boto3.client('textract')
#PAGE/LINE/WORD
def extract_text(response, extract_by = "LINE"):
    line_text = []
    for block in response['Blocks']:
        if block['BlockType'] == extract_by:
            line_text.append(block['Text'])
    return line_text

#1. PLAINTEXT detection from documents:
response = textractmodule.detect_document_text(
    Document={
        'S3Object': {
            'Bucket': bucket,
            'Name': "input.JPG"
        }
    })
#doc = trp.Document(response)