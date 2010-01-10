from pymarc import MARCReader, Record, Field
from recordparser import MARCRecordObject, _tags

class AlephSequentialReader(MARCReader):
    """
    An iterator class for reading a file of MARC records in Aleph Sequential
    format, which subclasses pymarc's MARCReader. Based on Tim Prettyman's
    MARC::File::AlephSeq Perl code.
    
    """
    def __init__(self, marc_target):
        super(AlephSequentialReader, self).__init__(marc_target)

    def next(self):
        """
        To support iteration.
        """
        record_data = ''
        line = self.file_handle.readline()
        if not line:
            raise StopIteration
        key = line[0:9]
        current_key = key
        
        while key == current_key:
            record_data += line
            position = self.file_handle.tell()
            line = self.file_handle.readline()
            key = line[0:9]
        
        self.file_handle.seek(position)
        record = Record()
        for recordln in record_data.splitlines():
            tag = recordln[10:13]
            ind1 = recordln[13:14]
            ind2 = recordln[14:15]
            rest = recordln[18:]
            #if tag == 'FMT': pass
            if tag == 'LDR':
                record.leader = rest.replace('^', ' ') 
            elif tag < '010' and tag.isdigit():
                if tag == '008': rest = rest.replace('^', ' ')
                record.add_field(Field(tag=tag, data=rest))
            else:
                subfields = list()
                subfield_data = rest.split('$$')
                subfield_data.pop(0)
                for subfield in subfield_data:
                    subfields.extend([subfield[0], subfield[1:]])
                record.add_field(Field(tag=tag, indicators=[ind1, ind2], 
                    subfields=subfields))
        return record