from pymarc import MARCReader, Record, Field

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
        record = AlephSequentialRecord(record_data)
        return record

class AlephSequentialRecord(Record):
    """A class for representing a MARC record from or for an Aleph system."""

    def __init__(self, data='',):
        self.leader = (' '*10) + '22' + (' '*8) + '4500'
        self.fields = list()
        self.pos = 0
        if len(data) > 0:
            self.decode_aleph(data)

    def decode_aleph(self, data):
        """decode_aleph() accepts a record in Aleph Sequential MARC format
        and works similarly to Record.decode_marc(), but also extracts the
        Aleph record ID and Aleph record format if available. Based on Tim
        Prettyman's MARC::File::AlephSeq Perl code."""
        self.aleph_id = data[0:9]
        lines = data.splitlines()
        for line in lines:
            tag = line[10:13]
            ind1 = line[13:14]
            ind2 = line[14:15]
            rest = line[18:]
            if tag == 'FMT':
                self.aleph_format = rest[:2]
            elif tag == 'LDR':
                self.leader = rest.replace('^', ' ') 
            elif tag < '010':
                if tag == '008': rest = rest.replace('^', ' ')
                self.add_field(Field(tag=tag, data=rest))
            else:
                subfields = list()
                subfield_data = rest.split('$$')
                subfield_data.pop(0)
                for subfield in subfield_data:
                    subfields.extend([subfield[0], subfield[1:]])
                self.add_field(Field(tag=tag, indicators=[ind1, ind2], 
                    subfields=subfields))

    def encode_aleph(self):
        """To be implemented"""
        raise NotImplementedError