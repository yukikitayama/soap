import requests
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString


# If prepare external XML file
XML = 'PATH_TO_XML_FILE'
# If SOAP submission requires authentication file
AUTHENTICATION_FILE = 'PATH_TO_AUTHENTICATION_FILE'


def format_xml_body():

    # There are several ways to format XML boday

    # 1. Make an string object which contains the entire XML
    xml_string = \
        '<?xml version="1.0" encoding="utf-8"?>' \
        '<soap:Envelope xmlns:soap="SOMETHING"' \
        '  <soap:Body>' \
        '    SOMETHING' \
        '  </soap:Body>' \
        '<soap:Envelope>'

    """
    Notice if you make string by 3 quotations way, any spaces counts.
    Above concatenate strings by \, 
    so spaces are only spaces typed in quotations
    For example,
    xml_string = '''
        Type something
    '''
    """

    # 2. Make an external XML file and read it by ElementTree
    tree = ET.parse(XML)
    root = tree.getroot()
    xml_string = ET.tostring(root, encoding='unicode', method='xml')

    # 3. Use ElementTree to make from scratch
    root = ET.Element('soap:Envelope')
    # Set name spaces
    root.set('xmlns:soap', 'SOME_VALUE')
    soap_body = ET.Element('soap:Body')
    # Add more...
    # element.text = 'VALUE' allows us to add text between opening and closing tags
    # element.append(another_element) allows us to add child tag to parent tag
    root.append(soap_body)
    # Finally convert the object to string
    xml_string = ET.tostring(root, encoding='utf-8', short_empty_elements=True)
    # If you wanna have a human readable XML
    xml_string = parseString(xml_string).toprettyxml(indent='  ')

    return xml_string


def main():

    # Format XML body
    xml_string = format_xml_body()

    # Send SOAP by requests
    r = requests.request(
        # Method needs to be POST even if you just wanna get data with no your data submitted
        # because we need to send the XML object
        method='POST',
        # Your counterparty should give your SOAP request URL
        url='ENDPOINT',
        # XML string needs to be passed to data argument
        data=xml_string,
        # Add more if you are required to specify something
        headers={
            'Content-Type': 'text/xml'
        },
        # If the counterparty requires you to add authentication file
        # to check whether you are authorized to submit something to
        # counterparty by SOAP
        cert=AUTHENTICATION_FILE,
        # If everything correct, skipping verification would aovid error
        verify=False
    )
    print(f'Status code: {r.status_code}')


if __name__ == '__main__':
    main()
