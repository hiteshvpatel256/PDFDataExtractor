class CommonVoterData:
    def __init__(self):
        self.jila_parishad_name = ""
        self.jila_parishad_ward_no = ""
        self.nagar_parishad_name = ""
        self.nagar_parishad_ward_no = ""
        self.nagar_parishad_ward_name = ""
        self.nagar_parishad_bhag_no = ""

        self.panchayat_samiti_name = ""
        self.panchayat_samiti_ward_no = ""
        self.gram_panchayat = ""
        self.gram_panchayat_ward_no = ""
        self.polling_booth_details = ""
        self.vidhansabha_no = ""
        self.vidhansabha_name = ""
        self.village = ""
        self.sub_district = ""
        self.district = ""
        self.publication_date = ""

    def __repr__(self):
        return "cvdata jila_parishad_name:% s jila_parishad_ward_no:% s nagar_parishad_name:% s nagar_parishad_ward_no:% s nagar_parishad_ward_name:% s nagar_parishad_bhag_no:% s panchayat_samiti_name:% s panchayat_samiti_ward_no:% s gram_panchayat:% s gram_panchayat_ward_no:% s polling_booth_details:% s vidhansabha_no:% s vidhansabha_name:% s village:% s sub_district:% s district:% s publication_date:% s" % (self.jila_parishad_name, self.jila_parishad_ward_no, self.nagar_parishad_name, self.nagar_parishad_ward_no, self.nagar_parishad_ward_name, self.nagar_parishad_bhag_no, self.panchayat_samiti_name, self.panchayat_samiti_ward_no, self.gram_panchayat, self.gram_panchayat_ward_no, self.polling_booth_details, self.vidhansabha_no, self.vidhansabha_name, self.village, self.sub_district, self.district, self.publication_date)


class VoterData:
    def __init__(self):
        self.page_no = 0
        self.sr_no = ""
        self.voter_name = ""
        self.relative_name = ""
        self.relation = ""
        self.voter_id = ""
        self.house_no = ""
        self.age = ""
        self.gender = ""
        self.sub_section = ""
        self.status = ""
        self.error = ""

    def __repr__(self):
        return "Test page_no:% s sr_no:% s voter_name:% s relative_name:% s relation:% s voter_id:% s house_no:% s age:% s gender:% s sub_section:% s status:% s error:% s" % (self.page_no, self.sr_no, self.voter_name, self.relative_name, self.relation, self.voter_id, self.house_no, self.age, self.gender, self.sub_section, self.status, self.error)
