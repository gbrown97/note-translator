import boto3

textractmodule = boto3.client('textract', aws_access_key_id='', aws_secret_access_key='', region_name= "")
#LINE/WORD
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
            'Bucket': 'note-translator-data',
            'Name': "note.jpg"
        }
    })
